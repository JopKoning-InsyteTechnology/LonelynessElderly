import os, sys
import Config.General.General_Config as Config
from twilio.rest import Client

#TODO: test this file
NUMBER_OF_ARGUMENTS = 4

def Call(Method, Name, Number):
    if(Method == "-h" or Method == "-help"):
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

    METHOD = Method
    NAME = Name
    NUMBER = Number

    client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)

    if(METHOD == "D" or METHOD == "DIAL"):
        URL = Config.STARTING_URL_DIAL

    elif(METHOD == "DC" or METHOD == "DAIL_CALLBACK"):
        URL = Config.STARTING_URL_DIAL_CALLBACK

    elif(METHOD == "V" or METHOD == "VOICE"):
        URL = Config.STARTING_URL_VOICE 

    elif(METHOD == "VC" or METHOD == "VOICE_CALLBACK"):
        URL = Config.STARTING_URL_VOICE_CALLBACK
    else:
        print("ERROR WRONG METHOD, METHOD = ", METHOD)
        exit()

    print("Calling " + NAME +  " on number: " + NUMBER + " with " + METHOD + " method")

    print("recording_status_callback = " + Config.BASE_URL+ Config.RECORDING_URL)
    print("recording_status_callback_event=completed")
    print("url=" +Config.BASE_URL+URL)
    print("to=" + NUMBER)
    print("from_=" + Config.FROM)

    call = client.calls.create(
                        # url='https://b3b6-46-145-146-153.ngrok.io/voice',
                            record = True,
                            recording_status_callback  = Config.BASE_URL + Config.RECORDING_URL,
                            recording_status_callback_event="completed",
                            url= Config.BASE_URL+URL,
                            to=NUMBER,
                            from_=Config.FROM
                        )

    print(call.sid)
    # with open("Attendance/activity1", "a") as fo:
    #             fo.write(NAME + " : ")
    return

Call(sys.argv[1], sys.argv[2], sys.argv[3])