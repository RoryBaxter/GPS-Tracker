# Arrays to store the data from the file
times = []
lats = []
lons = []

# Place all of the file data into the arrays
with open('gps_log.txt', 'r') as file:
    # Iterate through every line and append to correct array
    count = 0
    for index, line in enumerate(file):
	if count == 0:
		times.append(line.strip("\n"))
	elif count == 1:
		lats.append(line.strip("\n"))
	else:
		lons.append(line.strip("\n"))
	count = (count+1)%3

# Header info
gpx_file = '<?xml version="1.0" encoding="UTF-8"?>\n'
gpx_file += '<gpx creator="Raspberry Pi GPS" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd" version="1.1" xmlns="http://www.topografix.com/GPX/1/1">\n'
# Metadata about run
gpx_file += '\t<metadata>\n'
gpx_file += '\t\t<time>' + times[0] + '</time>\n'
gpx_file += '\t</metadata>\n'

# Header for the trek segment
gpx_file += '\t<trk>\n'
gpx_file += '\t\t<trkseg>\n'
# Adding all the points
for i in range(len(times)):
    gpx_file += '\t\t\t<trkpt lat="' + lats[i] + '" lon="' + lons[i] + '">\n'
    gpx_file += '\t\t\t\t<time>' + times[i] + '</time>\n'
    gpx_file += '\t\t\t</trkpt>\n'
#Footer for trek segment
gpx_file += '\t\t</trkseg>\n'
gpx_file += '\t<trk>\n'
gpx_file += '</gpx>'

with open('gps_log.gpx', 'w+') as file:
    file.write(gpx_file)
