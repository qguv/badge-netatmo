import os
cd = os.chdir
ls = os.listdir
pwd = os.getcwd
rm = os.remove

def cat(filename):
    with open(filename, 'r') as f:
        print(f.read())

def tree(d):
    try:
        sds = os.listdir(d)
    except OSError:
        print(d)
    else:
        if sds:
            for sd in sds:
                tree(d.rstrip('/') + '/' + sd)
        else:
            print(d.rstrip('/') + '/')

def cp(src, dest):
    with open(src, 'r') as f_src:
        with open(dest, 'w') as f_dest:
            f_dest.write(f_src.read())
