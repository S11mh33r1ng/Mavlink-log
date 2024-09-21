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
time_str = ""
lat = ""
lon = ""
alt = ""
hdop = ""
vdop = ""
h_acc = ""
v_acc = ""
n_sats = ""

csv_file = 'autopilot_data.csv'
        
def send_data_to_csv(csv_writer, csv_data):
    try:
        print(csv_data)
        writer.writerow(csv_data)
    except KeyboardInterrupt:
        print("Interrupted...")

while not connected:
    try:
        master = mavutil.mavlink_connection("/dev/ttyACM1", baud=115200)
        print("Attempting connection")
        if master.wait_heartbeat:
            connected = True
            print("Connected")
            break
    except:
        time.sleep(1)
        print("Waiting for connection")

try:
    with open(csv_file,'a', newline='')as file:
        writer = csv.writer(file)
        if not header_done:
            writer.writerow(['Date', 'Time', 'Latitude', "Longitude", "Altitude(m)", "HDOP", "VDOP", "H_Acc(m)", "V_Acc(m)", "Number of sats"])
            header_done = True
        
        while True:
                msg = master.recv_match()
                if not msg:
                    continue
                if msg.get_type() == 'GPS_RAW_INT':
                    gps_message = msg.to_dict()
                    lat = str(gps_message["lat"] /1e7)
                    lon = str(gps_message["lon"] /1e7)
                    alt = str(gps_message["alt"] /1000)
                    hdop = str(gps_message["eph"] /100)
                    vdop = str(gps_message["epv"] / 100)
                    h_acc = str(gps_message["h_acc"] /1000)
                    v_acc = str(gps_message["v_acc"] /1000)
                    n_sats = str(gps_message["satellites_visible"])
                if msg.get_type() == 'SYSTEM_TIME':
                    time_message = msg.to_dict()
                    time_usec = time_message["time_unix_usec"]
                    time_sec = time_usec/1e6
                    date_time = datetime.datetime.fromtimestamp(time_sec)
                    date = str(date_time.strftime('%d.%m.%Y'))
                    time = str(date_time.strftime('%H:%M:%S'))
                data = [date, time, lat, lon, alt, hdop, vdop, h_acc, v_acc, n_sats]
                send_data_to_csv(writer, data)
except:
    print("Script interrupted. Closing file...")