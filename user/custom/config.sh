#!/usr/bin/env bash

#
# update klipper.bin on make1
#

set -e

this_dir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )

make_host="make_print@make1"
klipper_unit="make_klipper-wanhao_d6.service"
klipper_data="/home/make_print/wanhao_d6/klip/data"
klipper_repo="/home/make_print/wanhao_d6/klip/repo"


#echo "### this_dir=$this_dir"

echo "### service stop"
ssh $make_host "sudo systemctl stop $klipper_unit"

echo "### repo update"
ssh $make_host "cd $klipper_repo; git reset --hard"
ssh $make_host "cd $klipper_repo; git clean -f -d"
ssh $make_host "cd $klipper_repo; git pull"

echo "### build clean"
ssh $make_host "cd $klipper_repo; make distclean"

echo "### publish config.cfg"
scp "$this_dir/config.cfg"  "$make_host:$klipper_repo/.config"

# board mode = normal ::
# Bus 001 Device 007: ID 1d50:614e OpenMoko, Inc. lpc1768

# board mode = bootloader ::
# Bus 001 Device 005: ID 1d50:6015 OpenMoko, Inc. Smoothieboard

echo "### build reflash"
#FLASH_DEVICE="1d50:6015"
#FLASH_DEVICE="/dev/ttyACM0"
FLASH_DEVICE="/dev/serial/by-id/usb-Klipper_lpc1768_16100006262006AF566E6E58C32000F5-if00"
ssh $make_host "cd $klipper_repo ; make flash FLASH_DEVICE=$FLASH_DEVICE"

#
#
#
