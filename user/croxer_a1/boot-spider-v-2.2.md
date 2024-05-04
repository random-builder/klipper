
### common

https://github.com/FYSETC/FYSETC-SPIDER/tree/main/bootloader

linux setup:
* use USB-1.0 "black" USB ports, NOT USB-2.0 "blue" ports (need for virt-box ???)

board setup
* turn off 24v
* USB power jumper: USB-vs-24V -> U5V (upper joint)
* BOOT mode jumper: connect +3.3V -> BT0
* press reset on board
* verify lsusb: 0483:df11 STMicroelectronics STM Device in DFU Mode

### method 1

https://www.st.com/en/development-tools/stm32cubeprog.html#get-software

windows setup:
* windows 7 prop
* cube-prog version 2.5.0

### method 2

procedure:
* invoke boot-spider-v-2.2.py
* BOOT mode jumper: disconnect +3.3V XX BT0
* build klipper.bin
* put on FAT32 SD card: klipper.bin -> firmware.bin
* insert SD card
* press reset on board
* observe "flash" led blinking for 1...2 seconds
* verify lsusb: 0483:5741 STMicroelectronics stm32f446xx
* verify ls -las /dev/serial/by-id/: usb-Klipper_stm32f446xx_180023000A50563046363120-if00
