#
#
#

#
# /klipper/scripts/flash_usb.py
#

import os

repo_root = os.popen("git rev-parse --show-toplevel").readline().strip()

os.chdir(repo_root)

os.system("dfu-util --list")

# os.system(f"sudo dfu-util -p 5-1.2 -R -a 0 -s 0x8008000:leave -D out/klipper.bin")

