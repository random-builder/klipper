#
# method 2
# https://github.com/FYSETC/FYSETC-SPIDER/tree/main/bootloader
#

# commit:
# 2022-09-02
# 9ecfded226fadac1e8e5fc8256e445516d1f6be2

# commit:
# 2021-06-23
# 41821e4607760fd1965f7fd529badf2a888d84b7
# git restore -s 41821e4607760fd1965f7fd529badf2a888d84b7 -- Bootloader_FYSETC_SPIDER.hex

import os

os.system("dfu-util --list")

"""
### OUTPUT ###
Found DFU: [0483:df11] ver=2200, devnum=48, cfg=1, intf=0, path="5-1.2", alt=3, name="@Device Feature/0xFFFF0000/01*004 e", serial="STM32FxSTM32"
Found DFU: [0483:df11] ver=2200, devnum=48, cfg=1, intf=0, path="5-1.2", alt=2, name="@OTP Memory /0x1FFF7800/01*512 e,01*016 e", serial="STM32FxSTM32"
Found DFU: [0483:df11] ver=2200, devnum=48, cfg=1, intf=0, path="5-1.2", alt=1, name="@Option Bytes  /0x1FFFC000/01*016 e", serial="STM32FxSTM32"
Found DFU: [0483:df11] ver=2200, devnum=48, cfg=1, intf=0, path="5-1.2", alt=0, name="@Internal Flash  /0x08000000/04*016Kg,01*064Kg,03*128Kg", serial="STM32FxSTM32"
"""

os.system("wget https://github.com/FYSETC/FYSETC-SPIDER/raw/main/bootloader/Bootloader_FYSETC_SPIDER.hex -O Bootloader_FYSETC_SPIDER.hex")

os.system("objcopy --input-target=ihex --output-target=binary Bootloader_FYSETC_SPIDER.hex Bootloader_FYSETC_SPIDER.bin")

os.system("dfu-util -a 0 -s 0x08000000:mass-erase:force -D Bootloader_FYSETC_SPIDER.bin")

"""
### OUTPUT ###
Erase       [=========================] 100%        16860 bytes
Erase    done.
Download    [=========================] 100%        16860 bytes
Download done.
"""

#
#
#
