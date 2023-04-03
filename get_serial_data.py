import serial
from time import sleep
import gmplot
import datetime

port = "COM3"
ser = serial.Serial(port, 9600, timeout=0)
port_temp = "COM2"
ser_temp = serial.Serial(port_temp, 9600, timeout=5)
all_data = []
temperature = []

def convert(data):
    """
    @dev convert to degrees
    @param data float number of type XXXX.XXXX
    @return float degree value
    """
    degrees = int(data/100)
    minutes = int(data - degrees * 100) / 60
    seconds = (data - int(data)) / 360
    return (degrees + minutes + seconds)

# N, E - "-"
# S, W - "+"
def get_gprmc(splitted_data):
    """
    @dev get GPRMS format data and process it
    @param splitted by ',' GPRMS string
    @return enum of longitude and latitude
    """
    splitted_data[3] = convert(float(splitted_data[3]))
    splitted_data[5] = convert(float(splitted_data[5]))
    if splitted_data[4] == 'N':
        splitted_data[3] = -1 * float(splitted_data[3])
    if splitted_data[6] == 'E':
        splitted_data[5] = -1 * float(splitted_data[5])
    return (splitted_data[3], splitted_data[5])

def get_gpgga(splitted_data):
    """
    @dev get GPGGS format data and process it
    @param splitted by ',' GPGGA string
    @return enum of longitude and latitude
    """
    splitted_data[2] = convert(float(splitted_data[2]))
    splitted_data[4] = convert(float(splitted_data[4]))
    if splitted_data[3] == 'N':
        splitted_data[2] = -1 * float(splitted_data[2])
    if splitted_data[5] == 'E':
        splitted_data[4] = -1 * float(splitted_data[4])
    return (splitted_data[2], splitted_data[4])

while True:
    all_data.append(ser.readline().decode())
    temperature.append(ser_temp.readline().decode())
    print(temperature)
    
    size = len(all_data)-1
    if all_data[size] == '':
        all_data.pop()
        temperature.pop()
        continue
    new_data = all_data[size]
    if "GPRMC" in new_data:
        all_data[size] = get_gprmc(new_data.split(','))

    elif "GPGGA" in new_data:
        all_data[size] = get_gpgga(new_data.split(','))
    else: 
        all_data.pop()
        temperature.pop()
        continue
    print(all_data[size][0], all_data[size][1])

    gmap3 = gmplot.GoogleMapPlotter(all_data[size][0], all_data[size][1], 14)
    for i in range(size+1):
        gmap3.marker(all_data[size][0], all_data[size][1] + 20 - i/100, '#FF0000', size=40, 
                    title=("t = " + temperature[i] + ', ' + str(datetime.datetime.now()) + 
                    " " + str(all_data[size][0]) + ', ' + str(all_data[size][1] - i/100)))

    gmap3.draw( "map_data\\map.html" )

ser.close()
ser_temp.close()

# import codecs

# with open('data.hex', 'ba+') as f: 
#     f.write(bytes(codecs.encode(b'$GPRMC,080655.00,A,4546.40891,N,12639.65641,E,1.045,328.42,170809,,,A*60', 'hex')))