
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

reset solution:
* after firmware flash: re-connect usb cable
