#!/usr/bin/python3

import os
import re

base_path = "/sys/bus/usb/devices"

def get_tty(serial_number, sub_dev=0):
    device = None
    dev_path = ""
    for d in os.listdir(base_path):
        try:
            dev_path = os.path.join(base_path, d)
            sn_file = open(os.path.join(dev_path, "serial"), "r")
            sn = sn_file.readline().strip()
            sn_file.close()
            if sn == serial_number:
                device = d
                break
        except OSError:
            continue

    if not device:
        return None

    p = re.compile(r"tty.+[0-9]$")
    s = re.compile(device + ":1." + str(sub_dev))
    tty = None
    for d in os.listdir(dev_path):
        if not s.match(d):
            continue
        sub_dev_path = os.path.join(dev_path, d)
        for root, dirs, _ in os.walk(sub_dev_path):
            for f in dirs:
                if p.match(f):
                    tty = os.path.join("/dev", f)
                    break
            if tty:
                break
        if tty:
            break

    return tty

def get_sn(tty=None):
    serial_numbers = []
    for d in os.listdir(base_path):
        try:
            dev_path = os.path.join(base_path, d)
            sn_file = open(os.path.join(dev_path, "serial"), "r")
            sn = sn_file.readline().strip()
            sn_file.close()
            serial_numbers.append(sn)
        except OSError:
            continue

    ttys = [get_tty(s) for s in serial_numbers]
    
    return [{serial_numbers[i]: ttys[i]} \
            for i in range(0, len(ttys)) if ttys[i] != None]


if __name__ == "__main__":
    print(get_tty("A400D61R"))
    print(get_sn())
