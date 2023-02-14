from flask import Blueprint, render_template
import Config.General.General_Config as Config
from twilio.rest import Client
import time

Entry_Points = Blueprint('Entry_Points', __name__)

#EXAMPLE
#http://d350-92-70-48-114.ngrok.io/Entry_Points/V/Jop/+31638475605

@Entry_Points.route('/<Method>/<Name>/<Number>',  methods=['GET', 'POST'])
def Entry(Method, Name, Number):
    print("In voice initial entry point")
    print(Number)
    print(Method)

    # client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
    # call = client.calls.create(
    #                             record = True,
    #                             recording_status_callback  = Config.BASE_URL + "/" + Config.RECORDING_URL,
    #                             recording_status_callback_event="completed",
    #                             url= Config.BASE_URL+"/"+Config.STARTING_URL_VOICE ,
    #                             to=Config.TO,
    #                             from_=Config.FROM
    #                         )
    # print(call.sid)
    # return "Test1"




    if(Method == "-h" or Method == "-help"):
        print("Python3 Call.py [METHOD] [NAME] [NUMBER]")
        print("METHOD -> D(ial_Initial)/V(oice_Initial)/D(ail_)C(allback)/V(oice_)C(allback)")
        print("NAME -> STRING")
        print("NUMBER -> +316XXXXXXXX")
# print("FILE_TO_WRITE_ATTENDANCE -> XXX.txt")
        exit()

    if (Method == "" or Number == ""):
        print("ERROR Too few arguments")
        exit()

    if ("/" in Method):
        print("ERROR Too many arguments")
        exit()

    METHOD = Method
    NAME = Name
    NUMBER = Number

    client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)

    if(METHOD == "D" or METHOD == "Dail_Initial"):
        URL = Config.STARTING_URL_DIAL

    elif(METHOD == "DC" or METHOD == "Dail_Callback"):
        URL = Config.STARTING_URL_DIAL_CALLBACK

    elif(METHOD == "V" or METHOD == "Voice_Initial"):
        URL = Config.STARTING_URL_VOICE 

    elif(METHOD == "VC" or METHOD == "Voice_Callback"):
        URL = Config.STARTING_URL_VOICE_CALLBACK
    else:
        print("ERROR WRONG METHOD, METHOD = ", METHOD)
        exit()

    print("Calling " + NAME +  " on number: " + NUMBER + " with " + METHOD + " method")

    print("recording_status_callback = " +Config.BASE_URL+ "/" +Config.RECORDING_URL)
    print("recording_status_callback_event=completed")
    print("url=" +Config.BASE_URL+ "/" + URL)
    print("to="  + NUMBER)
    print("from_="  +Config.FROM)

    call = client.calls.create(
                        # url='https://b3b6-46-145-146-153.ngrok.io/voice',
                            record = True,
                            recording_status_callback  = Config.BASE_URL + "/" + Config.RECORDING_URL,
                            recording_status_callback_event="completed",
                            url= Config.BASE_URL+ "/" +URL,
                            to=NUMBER,
                            from_=Config.FROM
                        )

    print(call.sid)

    with open("Attendance/" + time.strftime("%Y-%m-%d") + ".txt", "a") as fo:
                fo.write(NAME + " : ")
    return render_template('succes.html')
