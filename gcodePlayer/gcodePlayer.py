#!/bin/python
import serial;
import io;

_serial=serial.Serial();

# Open a serial port
def openPort():
	global _serial;
	_serial = serial.Serial('/dev/ttyUSB0', 9600, timeout=1);
	return _serial.isOpen();

# read file, skip empty lines
def readGCode(fileName):
	gcode = [];
	f = open(fileName,'r');
	for line in f:
		# Skip empty lines
		lin = line.strip();
		if len(lin) <= 1:
			continue;
		if lin[0]=='#':
			continue;
		lin = lin + '\n';

		# add to gcode repository
		gcode.append(lin);		
	return gcode;

# Main program
def main():
	global _serial;
	fileName='/home/pyro/output/output_0003.nc';
	print 'Opening serial port';
	if openPort()==False:
		print 'Port could not be opened!';
		return -1;
	
	# Read GCode
	gCode = readGCode(fileName);
	#print gCode;

	# send gcode to serial interface	
	for code in gCode:
		_serial.write(code);
		print code;

		while True:
			out = _serial.readline();
			if len(out)>0:
				break;

		print 'Result:' + out + '...';
		print '--------------';

	# Transfer completed
	print "${fileName} transfered to plotter";
	_serial.close();

	return 0;
		


if __name__ == "__main__":
    main()
