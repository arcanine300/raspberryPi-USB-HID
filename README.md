# PICO USB Human Interface Device Emulation
Circuit Python script using [AdaFruit USB HID](https://github.com/adafruit/Adafruit_CircuitPython_HID) library to emulate USB device functionality, can be used to implement software macros that execute at the hardware level. Currently configured to create mouse input that is identical in USB reporting to a common office mouse.

## USB PID / VID Spoofing
The project implements product and vendor ID spoofing to prevent device detection / fingerprinting from AntiCheat software.

## USB Report Descriptor Spoofing
By extracting USB report descriptor hex dump from a [Logitech LX3 Mouse](http://cdn.cnetcontent.com/18/53/18537558-49bb-46a3-a483-1ea19771a155.pdf) and using a [USB Descriptor and Request Parser](https://eleccelerator.com/usbdescreqparser/) tool, the raspberry pi pico will have the identical report descriptor of the USB HID device.
