#!/usr/bin/python3
# SPDX-License-Identifier: MIT
# TODO multiple ttys from one usb dev

import os
import re


base_path = "/sys/bus/usb/devices"


def _get_tty(device, sub_dev=0):
    dev_path = os.path.join(base_path, device)
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


def get_tty_mappings():
    serial_numbers = []
    ttys = []
    for d in os.listdir(base_path):
        try:
            dev_path = os.path.join(base_path, d)
            sn_file = open(os.path.join(dev_path, "serial"), "r")
            sn = sn_file.readline().strip()
            sn_file.close()
            serial_numbers.append(sn)
            ttys.append(_get_tty(d))
        except OSError:
            continue

    return [{serial_numbers[i]: ttys[i]} \
            for i in range(0, len(ttys)) if ttys[i] != None]


if __name__ == "__main__":
    print(get_tty_mappings())
