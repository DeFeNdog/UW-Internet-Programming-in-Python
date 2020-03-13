import serial

ser = serial.Serial()
ser.baudrate = 115200
ser.bytesize = 8
ser.stopbits = 1
ser.port = '/dev/cu.SLAB_USBtoUART'
ser.open()
