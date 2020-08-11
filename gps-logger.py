import serial
import time
import string
import pynmea2

AVG_RATE = 4

# Connect to the GPS unit
PORT = "/dev/ttyAMA0"
ser = serial.Serial(PORT, baudrate=9600, timeout=0.5)

# Buffers for storing lat and lon
lat_buffer = []
lon_buffer = []

# Generate file name based on unix time  when started
FILE_NAME = "gps-" + str(time.time()) + ".txt"

while True:
	# Read data
	dataout = pynmea2.NMEAStreamReader()
	newdata = ser.readline()

	# If the data is valid, process
	if newdata[0:6] == "$GPRMC":
		newmsg = pynmea2.parse(newdata)

		# Load new values into a buffer
		lat_buffer.append(newmsg.latitude)
		lon_buffer.append(newmsg.longitude)

		#Once the buffer is full, sum then averager then clear
		if len(lat_buffer) == AVG_RATE:
			# Average the values in the buffer
			lat = str(sum(lat_buffer)/AVG_RATE).split(".")
			lon = str(sum(lon_buffer)/AVG_RATE).split(".")

			# Round the lat and lng to 5 decimal places
			lat[1] = lat[1][:5]
			lon[1] = lon[1][:5]

			# Write the data to a file
			with open(FILE_NAME, "a+") as file:
				file.write(str(time.time()))
				file.write("\n")
				file.write(".".join(lat))
				file.write("\n")
				file.write(".".join(lon))
				file.write("\n")

			# Reset the buffers
			lat_buffer = []
			lon_buffer = []
