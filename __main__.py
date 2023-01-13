# Download the helper library from https://www.twilio.com/docs/python/install
#!/usr/bin/env python

import os, sys
from Webserver import Credentials as CRD
from twilio.rest import Client

NUMBER_OF_ARGUMENTS = 4

if(sys.argv[1] == "-h" or sys.argv[1] == "-help"):
    print("Python3 Call.py [METHOD] [NAME] [NUMBER]")
    print("METHOD -> D(IAL)/V(OICE)")
    print("NAME -> STRING")
    print("NUMBER -> +316XXXXXXXX")
   # print("FILE_TO_WRITE_ATTENDANCE -> XXX.txt")
    exit()

if(len(sys.argv) < NUMBER_OF_ARGUMENTS):
    print("ERROR Too few arguments")
    exit()

if(len(sys.argv) > NUMBER_OF_ARGUMENTS):
    print("ERROR Many few arguments")
    exit()

METHOD = sys.argv[1]
NAME = sys.argv[2]
NUMBER = sys.argv[3]

client = Client(CRD.Config["TWILIO_ACCOUNT_SID"], CRD.Config["TWILIO_AUTH_TOKEN"])

if(METHOD == "D" or METHOD == "DIAL"):
    URL = CRD.Config["STARTING_URL_DIAL"]

elif(METHOD == "DC" or METHOD == "DAIL_CALLBACK"):
    URL = CRD.Config["STARTING_URL_DIAL_CALLBACK"]

elif(METHOD == "V" or METHOD == "VOICE"):
    URL = CRD.Config["STARTING_URL_VOICE"]

elif(METHOD == "VC" or METHOD == "VOICE_CALLBACK"):
    URL = CRD.Config["STARTING_URL_VOICE_CALLBACK"]
else:
    print("ERROR WRONG METHOD, METHOD = ", METHOD)

    exit()

print("Calling " + NAME +  " on number: " + NUMBER + " with " + METHOD + " method")

print("recording_status_callback = " + CRD.Config["BASE_URL"]+CRD.Config["RECORDING_URL"])
print("recording_status_callback_event=completed")
print("url=" + CRD.Config["BASE_URL"]+URL)
print("to=" + NUMBER)
print("from_=" + CRD.Config["FROM"])

call = client.calls.create(
                       # url='https://b3b6-46-145-146-153.ngrok.io/voice',
                        record = True,
                        recording_status_callback  = CRD.Config["BASE_URL"]+CRD.Config["RECORDING_URL"],
                        recording_status_callback_event="completed",
                        url=CRD.Config["BASE_URL"]+URL,
                        to=NUMBER,
                        from_=CRD.Config["FROM"]
                    )

print(call.sid)
with open("Attendance/activity1", "a") as fo:
            fo.write(NAME + " : ")



