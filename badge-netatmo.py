from . import mparse
from . import murequests
from . import secrets

import badge
import buttons
import display
import easywifi
import utime

URL_ROOT = "https://api.netatmo.com/"
URL_AUTH = URL_ROOT + "oauth2/token"
URL_HOMES = URL_ROOT + "api/homesdata"
URL_HOME = URL_ROOT + "syncapi/v1/homestatus"
UPDATE_INTERVAL = 30000 # ms
BUTTON_TIMEOUT = 300 # ms

DATA_HEADERS = {"Content-Type": "application/json;charset=utf-8"}
AUTH_HEADERS = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}

def show(text, speed='normal'):
    if speed == 'slow':
        display.drawFill(0x000000)
        display.flush()
    display.drawFill(0xFFFFFF)
    display.drawText(0, 0, text, 0x000000, "PermanentMarker36")
    if speed == 'fast':
        display.flush(display.FLAG_LUT_FASTEST)
    else:
        display.flush()

def await_network():
    while True:
        easywifi.enable()
        if easywifi.state:
            break
        show('No internet!')
        badge.eink_busy_wait()
        show('Checking connection...', speed='fast')

def get_access_token():
    params = {
        "grant_type": "password",
        "client_id": secrets.CLIENT_ID,
        "client_secret": secrets.CLIENT_SECRET,
        "username": secrets.USERNAME,
        "password": secrets.PASSWORD,
        "scope": "read_thermostat write_thermostat",
    }
    params = mparse.urlencode(params)
    res = murequests.post(URL_AUTH, data=params, headers=AUTH_HEADERS).json()
    # TODO refresh_token, expires_in
    return res['access_token']

def get_home(access_token):
    """returned dict has id & name"""
    params = {"access_token": access_token}
    res = murequests.post(URL_HOMES, json=params, headers=DATA_HEADERS).json()
    return res['body']['homes'][0]

def get_room(access_token, home_id):
    params = {"access_token": access_token, 'home_id': home_id}
    res = murequests.post(URL_HOME, json=params, headers=DATA_HEADERS).json()
    return res['body']['home']['rooms'][0]

def init():
    await_network()
    show("Searching...")

    # TODO
    #buttons.attach(buttons.BTN_UP, increase_set_temp)
    #buttons.attach(buttons.BTN_DOWN, decrease_set_temp)
    #buttons.attach(buttons.BTN_LEFT, increase_override_time)
    #buttons.attach(buttons.BTN_RIGHT, decrease_override_time)

def update():
    access_token = get_access_token()
    home = get_home(access_token)
    room = get_room(access_token, home['id'])
    measured = room['therm_measured_temperature']
    setpoint = room['therm_setpoint_temperature']
    show('{}\ntemp: {:.1f} C\nset: {:.1f} C'.format(home['name'], measured, setpoint), speed='slow')

last_update = 0
last_button = 0
def loop():
    global last_update
    global last_button
    while True:
        now = utime.ticks_ms()
        if now - last_update > UPDATE_INTERVAL:
            last_update = utime.ticks_ms()
            update()
        if now - last_button > BUTTON_TIMEOUT and last_button != 0:
            last_button = 0 # only handle button press once
            last_update = now - UPDATE_INTERVAL + 2000 # force update in 2s
            update()

print("DEBUG: imported as {}".format(__name__))
if __name__ == "netatmo":
    init()
    update()
    loop()
