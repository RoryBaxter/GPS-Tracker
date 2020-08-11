# Arrays to store the data from the file
times = []
lats = []
lons = []

# Place all of the file data into the arrays
with open('gps_log.txt', 'r') as file:
    # Count number of lines
    lines = 1
    for i, l in enumerate(file):
        lines += 1
    
    # If the file is not empty, add data from file
    if lines != 1:
        for i in range(lines//3):
            times.append(file.readline())
            lats.append(file.readline())
            lons.append(file.readline())

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