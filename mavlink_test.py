import time
import sys
import csv
import datetime

from pymavlink import mavutil

connected = False
gps_input = False
time_input = False
header_done = False
date = ""
time = ""
lat = ""
lon = ""
alt = ""
hdop = ""
h_acc = ""
n_sats = ""

csv_file = 'autopilot_data.csv'
        
def send_data_to_csv(csv_data):
    try:
        with open(csv_file,'w', newline='')as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Time', 'Latitude', "Longitude", "Altitude(m)", "HDOP", "H_Acc(m)", "Number of sats"])
            print(csv_data)
            writer.writerow(csv_data)
    except KeyboardInterrupt:
        print("Closing file...")
    finally:
        print("File closed")

while not connected:
    try:
        master = mavutil.mavlink_connection("/dev/ttyACM1", baud=115200)
        print("leidsin")
        if master.wait_heartbeat:
            connected = True
            print("ühendatud")
            break
    except:
        time.sleep(1)
        print("ootan")

while True:
        msg = master.recv_match()
        if not msg:
            continue
        if msg.get_type() == 'GPS_RAW_INT':
            #print("\n\n*****Got message: %s*****" % msg.get_type())
            #print("Message: %s" % msg)
            gps_message = msg.to_dict()
            lat = str(gps_message["lat"] /1e7)
            lon = str(gps_message["lon"] /1e7)
            alt = str(gps_message["alt"] /1000)
            hdop = str(gps_message["eph"] /100)
            h_acc = str(gps_message["h_acc"] /1000)
            n_sats = str(gps_message["satellites_visible"])
            #print(lat, lon, alt, hdop, h_acc, n_sats)
        if msg.get_type() == 'SYSTEM_TIME':
            #print("\n\n*****Got message: %s*****" % msg.get_type())
            #print("Message: %s" % msg)
            time_message = msg.to_dict()
            time_usec = time_message["time_unix_usec"]
            time_sec = time_usec/1e6
            date_time = datetime.datetime.fromtimestamp(time_sec)
            date = str(date_time.strftime('%d.%m.%Y'))
            time = str(date_time.strftime('%H:%M:%S'))
            #print(date, time)
        data = [date, time, lat, lon, alt, hdop, h_acc, n_sats]
        #print(data)
        send_data_to_csv(data)
            #exctract_data(time_message)