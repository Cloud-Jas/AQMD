#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Requires pyserial. Install via:
# pip install pyserial

from __future__ import print_function
from serial import Serial, EIGHTBITS, STOPBITS_ONE, PARITY_NONE
import time, struct
import string 
import pynmea2
import json
import uuid

from azure.iot.device import IoTHubDeviceClient, Message

port = "/dev/ttyUSB0" # Set this to your serial port.
baudrate = 9600

gpsPort="/dev/ttyAMA0"
gpsBaudrate= 9600


device_client= IoTHubDeviceClient.create_from_connection_string("YOUR_CONNECTION_STRING")

device_client.connect()

MSG_PAYLOAD= '{{"pm_25": {pm_25},"pm_10": {pm_10},"lat": {lat},"lng": {lng}}}'
# Prepare serial connection.
ser = Serial(port, baudrate=baudrate, bytesize=EIGHTBITS, parity=PARITY_NONE, stopbits=STOPBITS_ONE)
ser.flushInput()

HEADER_BYTE = b"\xAA"
COMMANDER_BYTE = b"\xC0"
TAIL_BYTE = b"\xAB"

byte, previousbyte = b"\x00", b"\x00"

while True:
    previousbyte = byte
    byte = ser.read(size=1)
    #print(byte)
    
    # We got a valid packet header.
    if previousbyte == HEADER_BYTE and byte == COMMANDER_BYTE:
        packet = ser.read(size=8) # Read 8 more bytes
        #print(packet)
        
        # Decode the packet - little endian, 2 shorts for pm2.5 and pm10, 2 ID bytes, checksum.
        readings = struct.unpack('<HHcccc', packet)
        
        # Measurements.
        pm_25 = readings[0]/10.0
        pm_10 = readings[1]/10.0

        #gps
        gpsSer= Serial(gpsPort,9600,timeout=0.5)
        dataout= pynmea2.NMEAStreamReader()
        
        newdata= gpsSer.readline().decode('utf-8',errors='ignore')
        lat=0
        lng=0
        print(newdata)
        # ID
        id = packet[4:6]
        
        # Prepare checksums.
        checksum = readings[4][0]
        calculated_checksum = sum(packet[:6]) & 0xFF
        checksum_verified = (calculated_checksum == checksum)
        
        # Message tail.
        tail = readings[5]
        if tail == TAIL_BYTE and checksum_verified:
            #print("PM 2.5:", pm_25, "μg/m^3  PM 10:", pm_10, "μg/m^3")
            if newdata[0:6] == "$GPRMC":
                newmsg= pynmea2.parse(newdata)
                lat= newmsg.latitude
                lng=newmsg.longitude
                payload= MSG_PAYLOAD.format(pm_25=pm_25, pm_10=pm_10, lat=lat, lng=lng)
                msg= Message(payload)
                msg.message_id= uuid.uuid4()
                msg.content_encoding= "utf-8"
                msg.custom_properties["deviceId"]= "ola"
                msg.content_type= "application/json"
                print("sending message: {}".format(msg))
                device_client.send_message(msg)
                time.sleep(2)
                print("PM 2.5:", pm_25, "µg/m³  PM 10:", pm_10, "µg/m³  ID:", bytes(id).hex())
            
            
