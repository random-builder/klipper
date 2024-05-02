#!/usr/bin/env python

#
# update klipper service on make host
#

import time

from anylib import *

print_report("publish printer.cfg")
invoke_ssh_exec(f"dirname {target_printer} | xargs mkdir -p")
invoke_ssh_copy(f"{source_printer}", f"{make_host}:{target_printer}")

print_report("service unit restart")
invoke_ssh_exec(f"sudo systemctl stop {klipper_unit}")
invoke_ssh_exec(f"rm -rf {target_service_log}")
invoke_ssh_exec(f"sudo systemctl start {klipper_unit}")

print_report("retrieve printer status")
time.sleep(1.5)
invoke_ssh_copy(f"{make_host}:{target_service_log}", f"{source_service_log}")
invoke_plain(f"cat {source_service_log} | grep 'Loaded MCU'")

#
#
#
