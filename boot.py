import supervisor
import board, digitalio
import storage, usb_midi, usb_cdc, usb_hid

button = digitalio.DigitalInOut(board.GP1)
button.pull = digitalio.Pull.UP

# Disable devices if button is not pressed.
if button.value:
   storage.disable_usb_drive()

'''LX3
 05 01 09 02 A1 01 09 01 A1 00 05 09 19 01 29 08
 15 00 25 01 95 08 75 01 81 02 95 00 81 03 05 01
 09 30 09 31 09 38 15 81 25 7F 75 08 95 03 81 06
 05 0C 0A 38 02 95 01 81 06 C0 C0
'''
LX3_Report = bytes((
   0x05, 0x01,        # Usage Page (Generic Desktop Ctrls)
   0x09, 0x02,        # Usage (Mouse)
   0xA1, 0x01,        # Collection (Application)
   0x09, 0x01,        #   Usage (Pointer)
   0xA1, 0x00,        #   Collection (Physical)
   0x05, 0x09,        #     Usage Page (Button)
   0x19, 0x01,        #     Usage Minimum (0x01)
   0x29, 0x08,        #     Usage Maximum (0x08)
   0x15, 0x00,        #     Logical Minimum (0)
   0x25, 0x01,        #     Logical Maximum (1)
   0x95, 0x08,        #     Report Count (8)
   0x75, 0x01,        #     Report Size (1)
   0x81, 0x02,        #     Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
   0x95, 0x00,        #     Report Count (0)
   0x81, 0x03,        #     Input (Const,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
   0x05, 0x01,        #     Usage Page (Generic Desktop Ctrls)
   0x09, 0x30,        #     Usage (X)
   0x09, 0x31,        #     Usage (Y)
   0x09, 0x38,        #     Usage (Wheel)
   0x15, 0x81,        #     Logical Minimum (-127)
   0x25, 0x7F,        #     Logical Maximum (127)
   0x75, 0x08,        #     Report Size (8)
   0x95, 0x03,        #     Report Count (3)
   0x81, 0x06,        #     Input (Data,Var,Rel,No Wrap,Linear,Preferred State,No Null Position)
   0x05, 0x0C,        #     Usage Page (Consumer)
   0x0A, 0x38, 0x02,  #     Usage (AC Pan)
   0x95, 0x01,        #     Report Count (1)
   0x81, 0x06,        #     Input (Data,Var,Rel,No Wrap,Linear,Preferred State,No Null Position)
   0xC0,              #   End Collection
   0xC0,              # End Collection
                      # 59 bytes
))

LX3Device = usb_hid.Device(
    report_descriptor=LX3_Report,
    usage_page=0x1,
    usage=0x02,  
    report_ids=(0, ),
    in_report_lengths=(5, ),
    out_report_lengths=(0, ),
)

supervisor.set_usb_identification("Logitech", "USB-PS/2 Optical Mouse", 1133, 49220)
usb_midi.disable()
usb_cdc.enable(console=False, data=False)
usb_hid.enable((LX3Device,), 0)
usb_hid.set_interface_name("USB-PS/2 Optical Mouse")