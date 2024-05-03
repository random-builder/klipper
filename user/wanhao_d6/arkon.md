
### folder

this is dedicated printer folder

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

no reset symptom:
* bad reset: solo green led is on
* good reset: every green led is on 

### work flow

* use work3
* use printer power on or off
* connect board usb to dell usb-row 2 or 3 -- usb-row 1 will fail

* invoke arkon.py -- makes symlink, verifies config, verifies build
* notice output: "version: {commit}"

* invoke config.py -- publish config, makes remote build and flash
* notice output: "version: {commit}"
 
* re-connect lpc176x to "blue usb" -- ensure board reset after flash

* invoke printer.py -- publish printer, makes remote service restart 
* notice output: "Loaded MCU ... commands ( {commit} ... )"

* make octopring reconnect http://make1:5001
* notice output: FIRMWARE_VERSION:{commit}
 
* confirm {commit} output is consistent
