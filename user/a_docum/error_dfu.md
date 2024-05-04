
### dfu-util: can't detach

happens on stm32f446

output:
	Resetting USB to switch back to Run-Time mode
error result:
	dfu-util: can't detach

https://github.com/candle-usb/candleLight_fw/issues/64
	workaround : needs dfu-util 0.10 which adds a ":leave" command 
	$ dfu-util -S "002A002A4250431420363230", -a 0 -s 0x08000000:leave


### error resetting after download

happens on LPC1768

output:
	Resetting USB to switch back to runtime mode
	Done!
error result:	
	error resetting after download (LIBUSB_ERROR_NO_DEVICE)	
