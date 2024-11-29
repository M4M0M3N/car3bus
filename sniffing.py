'''
script per testare la lettura da parte del rasp sulla linea canbus
'''

import can

bus = can.interface.Bus(channel='can0', bustype='socketcan')

while True:
	message = bus.recv()
	print(f"Received CAN frame: {message}")
