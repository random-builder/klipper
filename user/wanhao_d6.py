#!/usr/bin/env python

import os  # @UnusedImport

from a_code.any_lib import *  # @UnusedWildImport

profile_dir = __file__.replace(".py", "")
profile_name = os.path.basename(__file__).replace(".py", "")

klipper_bean = KlipperBean(
    profile_name=profile_name,
    profile_dir=profile_dir,
    flash_device_id="usb-Klipper_lpc1768_16100006262006AF566E6E58C32000F5-if00",
)

klipper_bean.perform_main_work()

#
#
#
