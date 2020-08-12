import serial
import string
import pynmea2
from datetime import datetime

# Data handling constants
AVG_RATE = 4
PRECISION = 7

# Buffers for storing lat and lon
lat_buffer = []
lon_buffer = []

# Generate file or clean if already exists
FILE_NAME = "gps_log.txt"
open(FILE_NAME, "w").close()

# Connect to the GPS unit
PORT = "/dev/ttyAMA0"
ser = serial.Serial(PORT, baudrate=9600, timeout=0.5)

while True:
	# Read data
	dataout = pynmea2.NMEAStreamReader()
	newdata = ser.readline()

	# If the data is valid, process
	if newdata[0:6] == "$GPRMC":
		newmsg = pynmea2.parse(newdata)

		# Load new values into a buffer if they are non-zero
		if newmsg.latitude != 0:
			lat_buffer.append(newmsg.latitude)
			lon_buffer.append(newmsg.longitude)

		#Once the buffer is full, sum then averager then clear
		if len(lat_buffer) == AVG_RATE:
			# Average the values in the buffer
			lat = str(sum(lat_buffer)/AVG_RATE).split(".")
			lon = str(sum(lon_buffer)/AVG_RATE).split(".")

			# Round the lat and lng to the required precision
			lat[1] = lat[1][:PRECISION]
			lon[1] = lon[1][:PRECISION]

			# Write the data to a file
			with open(FILE_NAME, "a+") as file:
				file.write(datetime.now().isoformat().split(".")[0])
				file.write("\n")
				file.write(".".join(lat))
				file.write("\n")
				file.write(".".join(lon))
				file.write("\n")

			# Reset the buffers
			lat_buffer = []
			lon_buffer = []
