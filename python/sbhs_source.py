#/usr/bin/env python

from gnuradio import gr
import serial
import threading
import time
import numpy
import os
import sys

# Hardware addresses for Single Board Heater System components
FAN = 253
HEATER = 254
TEMPERATURE = 255

class sbhs_source(gr.hier_block2, threading.Thread):
	
	def __init__(self, sample_rate, fan_value, heater_value):    
		gr.hier_block2.__init__(self, 'sbhs_source', gr.io_signature(0,0,0), gr.io_signature(1,1,gr.sizeof_float))
	
		self.search_device()		
		self.initialize_device()

		self.set_sample_rate(sample_rate)
		self.set_fan_speed(fan_value)
		self.set_heater_temperature(heater_value)

		message_source = gr.message_source(gr.sizeof_int,1)
		self._msgq = message_source.msgq()
		self.connect(message_source, self)

		threading.Thread.__init__(self)
		self.setDaemon(True)
		self.start()
        
	def run(self):
		while True:
			time.sleep(1.0/self._sample_rate)
			temp = self.get_temperature()
			self._msgq.insert_tail(temp)
	
	def search_device(self):
		f=open("sbhs_shell.sh","w")
		f.write("#!/bin/sh\n")
		f.write("for udi in `hal-find-by-capability --capability serial | sort` \n")
		f.write("do\n")
		f.write("parent=`hal-get-property --udi ${udi} --key 'info.parent'`\n")
		f.write("device=`hal-get-property --udi ${udi} --key 'linux.device_file'`\n")
		f.write("vendor=`hal-get-property --udi ${parent} --key 'usb.vendor_id'`\n")
		f.write("product=`hal-get-property --udi ${parent} --key 'usb.product_id'`\n")
		f.write("printf '%s\n%.4x:%.4x\\n' ")
		f.write("${device} ${vendor} ${product}\n")
		f.write("done\n")
		f.close()

		os.system("sh sbhs_shell.sh > sbhs_temp")

		index=0
		flag=0
		self._sbhs_device=""
		tty=list(xrange(10))
		dev_id=list(xrange(10))
		f=open('sbhs_temp','r')
		for line in f:
			if flag==0:
				flag=1
				tty[index]=line.strip()
			else:
				flag=0
				dev_id[index]=line.strip()
				index=index+1
		f.close()

		flag=0
		for i in range(index):
			if dev_id[i]=="0403:6001":
				flag=1
				self._sbhs_device=tty[i]
				break

		if flag==0:
			print "SBHS Device Not Connected"
			sys.exit()
		else:
			print "SBHS Device Found %s" %(self._sbhs_device)	

	
	def initialize_device(self):
		self._SBHS = serial.Serial(self._sbhs_device, 9600)
		self._SBHS.open()

	def set_sample_rate(self,sample_rate):
		self._sample_rate = sample_rate

	def set_fan_speed(self,fan_value):
		self._fan_value = fan_value
		print "Setting Fan Speed: %d" %(fan_value)
        	self.write_to_sbhs(FAN, self._fan_value)

	def set_heater_temperature(self,heater_value):
		self._heater_value = heater_value
		print "Setting Heater Temperature: %d" %(heater_value)
        	self.write_to_sbhs(HEATER, self._heater_value)

	def write_to_sbhs(self, address, value):
		self._SBHS.write(chr(address))
		self._SBHS.write(chr(value))

	def get_temperature(self):
		self._SBHS.write(chr(TEMPERATURE))
		temp_val = map(ord, self._SBHS.read(2)) #reads in hexadecimal
		temp_string = str(temp_val[0]) + str(temp_val[1])	
		arr = numpy.array(float(temp_string), numpy.float32)
		print "Temperature Read: %s" %(arr)
		return gr.message_from_string(arr.tostring(), 0, gr.sizeof_float, 1)


