#!/usr/bin/env bash

#
# build and flash mcu firmware
#

#
# note: "make flash" needs dfu-util
# note: skr/smoothie needs initial manual flash via sd-disk
#

#set -e

readonly this_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
readonly base_dir="$( cd "$this_dir/../.." && pwd)"

echo "### base_dir=$base_dir"
echo "### this_dir=$this_dir"

function install_firmware() {
    
    local name=$1
    local path=$2
    
    local config="${this_dir}/board-${name}.cfg"
    local output="${base_dir}/out-${name}/"
    
    # use default only when unset
    local menu_word=${MENU_WORD-menuconfig}

    echo "### build firmware: $name"
    make PYTHON=python3 KCONFIG_CONFIG=${config} OUT=${output} $menu_word all
    
    if [ ! -e "$path" ] ; then
      echo "no device, skip flash: $name"
      return 0
    fi    

    echo "### flash firmware: $name"
    make PYTHON=python3 KCONFIG_CONFIG=${config} OUT=${output} flash FLASH_DEVICE=${path} 
    # note: "no sudo" flash fails for skr-v-1.3 ### NOSUDO=1

}

cd "$base_dir"

#
# original ID: 0483:5740 STMicroelectronics Virtual COM Port
# user set ID: 0483:5741 STMicroelectronics stm32f446xx
# https://github.com/FYSETC/FYSETC-SPIDER/blob/main/hardware/Spider%20V1.0C%20SCH.pdf
#
readonly MCU_1="spider-v-2.2"
readonly DEV_1="/dev/serial/by-id/usb-Klipper_stm32f446xx_180023000A50563046363120-if00"

#
# original ID: 0483:5740 STMicroelectronics Virtual COM Port
# user set ID: 0483:5742 STMicroelectronics stm32f446xx
# https://github.com/bigtreetech/BIGTREETECH-OCTOPUS-V1.0/blob/master/Hardware/BIGTREETECH%20Octopus.pdf
#
readonly MCU_2="octopus-v-1.1"
readonly DEV_2="/dev/serial/by-id/usb-Klipper_stm32f446xx_12002E000F5053424E363620-if00"

#
# original ID: 1d50:6015 OpenMoko, Inc. Smoothieboard
# user set ID: no change
# https://github.com/bigtreetech/BIGTREETECH-SKR-V1.3/blob/master/BTT%20SKR%20V1.3/hardware/SKR-V1.3-SCH.pdf
#
readonly MCU_3="skr-v-1.3"
readonly DEV_3="/dev/serial/by-id/usb-Klipper_lpc1768_0D50FF1502942EAF8D89515BC62000F5-if00"

#
# original ID: 2341:0010 Arduino SA Mega 2560 (CDC ACM)
# user set ID: no change
# https://3dprint.wiki/reprap/wanhao/duplicator6/major_components/motherboard
#
readonly MCU_4="wd6-v-1.5"
readonly DEV_4="/dev/serial/by-id/usb-Arduino__www.arduino.cc__Arduino_Mega_2560_55639313433351504171-if00"

install_firmware ${MCU_1} ${DEV_1}
install_firmware ${MCU_2} ${DEV_2}
install_firmware ${MCU_3} ${DEV_3}
#install_firmware ${MCU_4} ${DEV_4}
