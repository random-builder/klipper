#!/usr/bin/env python

import os  # @UnusedImport

from a_code.any_lib import *  # @UnusedWildImport

profile_dir = __file__.replace(".py", "")
profile_name = os.path.basename(__file__).replace(".py", "")

# https://docs.vorondesign.com/build/software/spider_klipper.html
spider_bean = KlipperBean(
    profile_name=profile_name,
    profile_dir=profile_dir,
    firmware_file="firmware-spider-v-2.2.cfg",
    # 0483:5741 STMicroelectronics stm32f446xx
    flash_device_id="usb-Klipper_stm32f446xx_180023000A50563046363120-if00",
)

spider_bean.perform_test_work()

#
#
#
