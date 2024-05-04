#!/usr/bin/env python

import os  # @UnusedImport

from a_code.any_lib import *  # @UnusedWildImport

profile_dir = __file__.replace(".py", "")
profile_name = os.path.basename(__file__).replace(".py", "")

# https://docs.vorondesign.com/build/software/spider_klipper.html
spider_bean = KlipperBean(
    profile_dir=profile_dir,
    profile_name=profile_name,
    firmware_file="firmware-spider-v-2.2.cfg",
    # 0483:5741 STMicroelectronics stm32f446xx
    flash_device_id="usb-Klipper_stm32f446xx_180023000A50563046363120-if00",
)

# https://docs.vorondesign.com/build/software/octopus_klipper.html
octopus_bean = KlipperBean(
    profile_dir=profile_dir,
    profile_name=profile_name,
    firmware_file="firmware-octopus-v-1.1.cfg",
    # 0483:5742 STMicroelectronics stm32f446xx
    flash_device_id="usb-Klipper_stm32f446xx_12002E000F5053424E363620-if00",
)

# note:
# * need to use usb-2.0 @ work3
skr_bean = KlipperBean(
    profile_dir=profile_dir,
    profile_name=profile_name,
    firmware_file="firmware-skr-v-1.3.cfg",
    # 1d50:6015 OpenMoko, Inc. Smoothieboard
    flash_device_id="usb-Klipper_lpc1768_0D50FF1502942EAF8D89515BC62000F5-if00",
)

# spider_bean.perform_test_work()
# octopus_bean.perform_test_work()
skr_bean.perform_test_work()

#
#
#
