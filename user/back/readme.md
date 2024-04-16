
### profile: custom1

* update to latest klipper repo @ 2023-10-01
* continue to use octopi
* verify works OK


--- original profile ---

### custom printer

repo
* git@github.com:random-builder/klipper.git
* https://github.com/random-builder/klipper.git

### board port

#### ls -las /dev/ttyA*

// marlin/klipper
- 0 crw-rw---- 1 root dialout 166,  0 May 30 19:17 /dev/ttyACM0

#### lsusb

// default marlin:
- Bus 001 Device 004: ID 1d50:6029 OpenMoko, Inc.

// default klipper:
- Bus 001 Device 008: ID 1d50:614e OpenMoko, Inc.

#### ls /dev/serial/by-id/*

// default marlin:
- /dev/serial/by-id/usb-marlinfw.org_Marlin_USB_Device_06001016AF062026586E6E56F50020C3-if00

// default klipper:
- /dev/serial/by-id/usb-Klipper_lpc1768_16100006262006AF566E6E58C32000F5-if00

### klipper setup

ssh octopi1

cd /home/pi
git clone https://github.com/random-builder/klipper.git
/home/pi/klipper/scripts/install-octopi.sh

cd /home/pi/klipper
make menuconfig

cd /home/pi/klipper
diff .config user/custom/config.cfg

sudo service klipper stop

ls -las /dev/ttyACM0
make flash FLASH_DEVICE=/dev/ttyACM0

sudo service klipper start

sudo systemctl enable klipper

### repo fetch

cd /home/pi/klipper
git fetch
git reset --hard origin/custom

cd /home/pi/klipper
cp user/custom/printer.cfg ~/printer.cfg
