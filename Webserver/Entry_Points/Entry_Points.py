from flask import Blueprint, render_template
import Config.General.General_Config as Config
from Functions.General import Print_Log
from twilio.rest import Client
import time

Entry_Points = Blueprint('Entry_Points', __name__)

#EXAMPLE
#http://d350-92-70-48-114.ngrok.io/Entry_Points/V/Jop/+31638475605

@Entry_Points.route('/<Method>/<Name>/<Number>',  methods=['GET', 'POST'])
def Entry(Method, Name, Number):
    Print_Log("In voice initial entry point")
    Print_Log(Number)
    Print_Log(Method)

    # client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
    # call = client.calls.create(
    #                             record = True,
    #                             recording_status_callback  = Config.BASE_URL + "/" + Config.RECORDING_URL,
    #                             recording_status_callback_event="completed",
    #                             url= Config.BASE_URL+"/"+Config.STARTING_URL_VOICE ,
    #                             to=Config.TO,
    #                             from_=Config.FROM
    #                         )
    # Print_Log(call.sid)
    # return "Test1"




    if(Method == "-h" or Method == "-help"):
        Print_Log("Python3 Call.py [METHOD] [NAME] [NUMBER]")
        Print_Log("METHOD -> D(ial_Initial)/V(oice_Initial)/D(ail_)C(allback)/V(oice_)C(allback)")
        Print_Log("NAME -> STRING")
        Print_Log("NUMBER -> +316XXXXXXXX")
# Print_Log("FILE_TO_WRITE_ATTENDANCE -> XXX.txt")
        exit()

    if (Method == "" or Number == ""):
        Print_Log("ERROR Too few arguments")
        exit()

    if ("/" in Method):
        Print_Log("ERROR Too many arguments")
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
        Print_Log("ERROR WRONG METHOD, METHOD = ", METHOD)
        exit()

    Print_Log("Calling " + NAME +  " on number: " + NUMBER + " with " + METHOD + " method")

    Print_Log("recording_status_callback = " +Config.BASE_URL+ "/" +Config.RECORDING_URL)
    Print_Log("recording_status_callback_event=completed")
    Print_Log("url=" +Config.BASE_URL+ "/" + URL)
    Print_Log("to="  + NUMBER)
    Print_Log("from_="  +Config.FROM)

    call = client.calls.create(
                        # url='https://b3b6-46-145-146-153.ngrok.io/voice',
                            record = True,
                            recording_status_callback  = Config.BASE_URL + "/" + Config.RECORDING_URL,
                            recording_status_callback_event="completed",
                            url= Config.BASE_URL+ "/" +URL,
                            to=NUMBER,
                            from_=Config.FROM
                        )

    Print_Log(call.sid)

    with open("Attendance/" + time.strftime("%Y-%m-%d") + ".txt", "a") as fo:
                fo.write(NAME + " : ")
    return render_template('succes.html')
