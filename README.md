# netatmo

sha2017 badge client for a netatmo thermostat

## flashing

- install python3 and pipenv
- create an app [here](https://dev.netatmo.com/apps)
- update `secrets.py` with the credentials from above
- run `./flash`

## tools

- run `./term` to get a serial terminal; use Ctrl-`A` `K` `Y` to get out
- the `./flash` script installs convenient aliases for the on-badge python interpretes; use them by typing `from aliases import *`

## troubleshooting

- if you get "SyntaxError: invalid syntax" really close to a python triple-single-quote (`'''`) operator, use a triple-double-quote (`"""`) instead
