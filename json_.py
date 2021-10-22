import json
import paho.mqtt.client as paho  		    #mqtt library
import os
import readsms
from datetime import datetime

ACCESS_TOKEN=   os.getenv('TOKEN')
broker =        'iot.beeline.kz'
port =          11883
topic   =       'v1/gateway/telemetry'

string_sms1  = '3500001138363932343430343134363635383606001C015DC42BF33030303030303031363338303030303031012041000000000205981A00060000030000E16F01A9'
string_sms2  = '4000001138363932343430343134363635383706001C015DC42BF33030303030303031363338303030303031012041000000000205981A00060000030000E16F01A9'

dict_buff       =   {}
list_with_data  =   []
json_buff       =   {}

def parse_and_create_dict(string_sms):
    dict_data = {
        "Frame type":           string_sms[0:2],
        "Encryption marker":    string_sms[2:4],
        "Frame ID":             string_sms[4:8],
        "IMEI":                 string_sms[8:38],
        "FW":                   string_sms[38:44],
        "HW":                   string_sms[44:46],
        "Manufacture date":     string_sms[46:54],
        "Account ID":           string_sms[54:70],
        "Qualifier code":       string_sms[70:72],
        "Contact ID event code":string_sms[72:78],
        "Contact ID partition": string_sms[78:82],
        "Contact ID zone code": string_sms[82:88],
        "Format Number: packet version number":     string_sms[88:90],
        "Battery voltage open circuit":             string_sms[90:94],
        "Battery voltage under load":               string_sms[94:98],
        "Internal resistance":                      string_sms[98:102],
        "Battery level":                            string_sms[102:104],
        "Temperature voltage":                      string_sms[104:108],
        "Temperature degrees":                      string_sms[108:110],
        "CO level voltage":                         string_sms[110:114],
        "CO level ppm":                             string_sms[114:118],
        "GSM level":                                string_sms[118:120],
        "Time from start":                          string_sms[120:128],
        "Restart: 0x01 iki 0x09":                   string_sms[128:130],
        "CRC8":                                     string_sms[130:132]
        }
    return dict(dict_data)

def on_publish(client,userdata,result):
    pass

def init_client():
    client1 =               paho.Client()                    
    client1.on_publish =    on_publish
    client1.username_pw_set(ACCESS_TOKEN)
    client1.connect(broker,port,60)
    return client1

# START
client1     =   init_client()
dict_buff   = parse_and_create_dict(string_sms2)
list_with_data.append(dict_buff)   
json_buff[dict_buff.get('IMEI')] = list_with_data
json_send   = json.dumps(json_buff,indent=2)

client1.publish(topic,json_send)
