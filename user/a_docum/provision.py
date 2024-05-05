#!/usr/bin/env python

import os

# NOTE: remember to freeze
# /etc/pacman.conf
# [options]
# IgnorePkg = arm-none-eabi-newlib dfu-util


#
# Link error with newlib 4.3.0 on ARMv7
# https://klipper.discourse.group/t/link-error-with-newlib-4-3-0-on-armv7/6820
#
def provision_arm_lib():
    arm_lib_package = "arm-none-eabi-newlib-4.2.0.20211231-1-any.pkg.tar.zst"
    arm_lib_url = f"https://archive.archlinux.org/packages/a/arm-none-eabi-newlib/{arm_lib_package}"
    os.system(f"wget {arm_lib_url} --output-document={arm_lib_package} --no-clobber")
    os.system(f"sudo pacman --upgrade {arm_lib_package} --noconfirm --overwrite '*'")


#
# dfu-util: different versions, different problems
#
def provision_dfu_util():

    # LPC1768: works, no error
    # STM32F4: works, error: "dfu-util: can't detach"
    dfu_util_package = "dfu-util-0.9-3-x86_64.pkg.tar.zst"

    # LPC1768: TODO
    # STM32F4: TODO
    # dfu_util_package = "dfu-util-0.10-3-x86_64.pkg.tar.zst"

    dfu_util_url = f"https://archive.archlinux.org/packages/d/dfu-util/{dfu_util_package}"
    os.system(f"wget {dfu_util_url} --output-document={dfu_util_package} --no-clobber")
    os.system(f"sudo pacman --upgrade {dfu_util_package} --noconfirm --overwrite '*'")


provision_arm_lib()
provision_dfu_util()

#
#
#
