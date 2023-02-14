# Flask Imports
from flask import Blueprint, request

# Twilio Imports
from twilio.twiml.voice_response import VoiceResponse

# Configuration Imports
import Config.General.General_Config as Config

# Import Functions
from Functions.General import  Play, Redirect, Logger, Listen, ClassifyDailInput, GatherDailInput, ClassifyDailInputSimple

# from GlobalVariables import Voice_Initial, LastMessage
import GlobalVariables

import time

Dail_Call_Callback = Blueprint('Dail_Call_Callback', __name__,
    static_folder='static')


Task_URL = "/" + Dail_Call_Callback.name

Errors = 0

Host = "DAIL_CALL_INITIAL"

Default_ListenTime_Begin = 2
Default_ListenTime_Silence = 1.5

@Dail_Call_Callback.route('/Start', methods=['GET', 'POST'])
def list():
    return "Test1"

@Dail_Call_Callback.route("/Dail", methods=['GET', 'POST'])
def Dail():
        print(Task_URL)
        Logger(Host,"in /Dail", "INFO")
        return Redirect(Task_URL + "/Listen_For_Hello")

@Dail_Call_Callback.route("/Listen_For_Hello", methods=['GET', 'POST'])
def Listen_For_Hello():
        return Listen(1,1,Task_URL + "/Listen_For_Hello", Task_URL + "/Play_Greeting_Message") 

@Dail_Call_Callback.route("/Play_Greeting_Message", methods=['GET', 'POST'])
def Play_Greeting_Message():
        Logger(Host,"in /Play_Greeting_Message", "INFO")
        return Play(GlobalVariables.Dail_Callback.Welcome_Message, Task_URL + "/Play_Explain_Message")

@Dail_Call_Callback.route("/Play_Explain_Message", methods=['GET', 'POST'])
def Play_Explain_Message():
        Logger(Host,"in /Play_Explain_Message", "INFO")        
        return Play(GlobalVariables.Dail_Callback.Callback_Explaination_Message, Task_URL + "/Listen_For_Answer")

@Dail_Call_Callback.route("/Listen_For_Answer", methods=['GET', 'POST'])
def Listen_For_Answer():
        return GatherDailInput(Task_URL + "/Classify_Answer", Task_URL + "/No_Input")

@Dail_Call_Callback.route("/No_Input", methods=['GET', 'POST'])
def No_Input():
    global Errors
    if Errors >= 3:
        return Redirect(Task_URL + "/Finalize")
    Errors += 1

    return Play(GlobalVariables.Dail_Callback.Check_Unclear_Message, Task_URL + "/Play_Explain_Message")
    return Redirect("/Play_Explain_Message")

@Dail_Call_Callback.route("/Classify_Answer", methods=['GET', 'POST'])
def Classify_Answer():
    return ClassifyDailInput(request, Task_URL + "/Finalize", Task_URL + "/Play_Additional_Message", Task_URL + "/Play_Additional_Message", Task_URL + "/Play_Additional_Message")

@Dail_Call_Callback.route("/Play_Additional_Message", methods=['GET', 'POST'])
def Play_Additional_Message():
        Logger(Host,"in /Play_Explain_Message", "INFO")        
        return Play(GlobalVariables.Dail_Callback.Callback_Aditional_Message, Task_URL + "/Finalize")

@Dail_Call_Callback.route("/Finalize", methods=['GET', 'POST'])
def Finalize():
    Logger(Host,"in /Finalize/", "INFO")
    with open("Attendance/" + time.strftime("%Y-%m-%d") + ".txt", "a") as fo:
        fo.write("Dail_Call_Callback OK" + "\n")    
    return Play(GlobalVariables.Dail_Callback.Callback_Finalize_Yes_Message,Task_URL+ "/Hangup")

@Dail_Call_Callback.route("/Hangup", methods=['GET', 'POST'])
def Hangup():
    return str(VoiceResponse())
