
### board

using custom lpc176x

manual:
	/home/user0/Print3d/smooth/mks/
	valid scheme: "MKS SBASE 2019 V1.3_002 SCH.pdf"

critical:
* board has +5V on-board power disabled
* reason: provide stable usb klipper connection  	 
* reason: eliminate usb bus reset during nut power switch
* side effect: needs manual board reset after firmware flash  	 

### work flow

* use work3
* use console
* use printer power off
* connect board usb to pc "blue usb" -- "black usb" will fail

* invoke arkon.sh -- makes symlink, verifies config, verifies build
* notice output: "version: {commit}"

* invoke config.sh -- publish config, makes remote build and flash
* notice output: "version: {commit}"
 
* re-connect lpc176x to "blue usb" -- ensure board reset after flash

* invoke printer.sh -- publish printer, makes remote service restart 
* notice output: "Loaded MCU ... commands ( {commit} ... )"

* make octopring reconnect http://make1:5001
* notice output: FIRMWARE_VERSION:{commit}
 
* confirm {commit} output is consistent
