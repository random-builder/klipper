#!/usr/bin/env python

#
# update klipper firmware on make host
#

from anylib import *

print_report("service stop")
invoke_ssh_exec(f"sudo systemctl stop {klipper_unit}")

print_report("repo update")
invoke_ssh_exec(f"cd {klipper_repo} ; git reset --hard")
invoke_ssh_exec(f"cd {klipper_repo} ; git clean -f -d")
invoke_ssh_exec(f"cd {klipper_repo} ; git pull")

print_report("remove build")
invoke_ssh_exec(f"cd {klipper_repo} ; make distclean")

print_report("publish config")
invoke_ssh_copy(f"{source_config}", f"{make_host}:{target_config}")

print_report("build and flash")
# FLASH_DEVICE="1d50:6015"
# FLASH_DEVICE="/dev/ttyACM0"
FLASH_DEVICE = "/dev/serial/by-id/usb-Klipper_lpc1768_16100006262006AF566E6E58C32000F5-if00"
invoke_ssh_exec(f"cd {klipper_repo} ; make flash FLASH_DEVICE={FLASH_DEVICE}")

#
#
#
