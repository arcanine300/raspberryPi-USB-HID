import usb_hid
import time, random
import board, digitalio
from adafruit_hid.mouse import Mouse, find_device

class LX3Mouse(Mouse):
	def __init__(self, devices):
		self._mouse_device = find_device(devices, usage_page=0x1, usage=0x02)
		try:
			self._mouse_device.send_report(b'\0' * 5)
		except ValueError:
			print("LX3Mouse Device Found | ERROR: did not accept a 5-byte report, check boot.py")

		self.report = bytearray(5)

	def press(self, buttons: int, wButtons: int = 0):
	    self.report[0] |= buttons 
	    self.report[4] = wButtons 
	    self._send_no_move()

	def release(self, buttons: int, wButtons: int = 0):
	    self.report[0] &= ~buttons
	    self.report[4] = 0
	    self._send_no_move()

	def release_all(self):
	    self.report[0] = 0
	    self.report[4] = 0
	    self._send_no_move()

	def click(self, buttons: int, wButtons: int = 0):
	    self.press(buttons, wButtons)
	    self.release(buttons, wButtons)

	def move(self, x = 0, y = 0, wheel = 0):
	    while x != 0 or y != 0 or wheel != 0: 
	        partial_x = self._limit(x)
	        partial_y = self._limit(y)
	        partial_wheel = self._limit(wheel)
	        self.report[1] = partial_x & 0xFF
	        self.report[2] = partial_y & 0xFF
	        self.report[3] = partial_wheel & 0xFF
	        self._mouse_device.send_report(self.report)
	        x -= partial_x
	        y -= partial_y
	        wheel -= partial_wheel

	def _send_no_move(self):
	    self.report[1] = 0
	    self.report[2] = 0
	    self.report[3] = 0
	    self._mouse_device.send_report(self.report)

	@staticmethod
	def _limit(dist):
	    return min(127, max(-127, dist))


LEFT_WHEEL_BUTTON = 255
RIGHT_WHEEL_BUTTON = 1
mouse = LX3Mouse(usb_hid.devices) #Mouse(usb_hid.devices)
while True:
	#mouse.move(random.randint(-2, 2), random.randint(-2, 2))
	time.sleep(random.uniform(0.06, 0.09))
