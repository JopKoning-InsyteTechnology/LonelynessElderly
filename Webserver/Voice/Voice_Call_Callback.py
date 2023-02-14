# Flask Imports
from flask import Blueprint, request

# Twilio Imports
from twilio.twiml.voice_response import VoiceResponse

# Configuration Imports
import Config.General.General_Config as Config

# Import Functions
from Functions.General import Listen, Play, Redirect, Classify, Logger

# from GlobalVariables import Voice_Initial, LastMessage
import GlobalVariables

import time


Voice_Call_Callback = Blueprint('Voice_Call_Callback', __name__,
    static_folder='static')

Task_URL = "/" + Voice_Call_Callback.name
Host = "VOICE_CALL_CALLBACK"

Default_ListenTime_Begin = 1.5
Default_ListenTime_Silence = 1.5

@Voice_Call_Callback.route('/Start', methods=['GET', 'POST'])
def list():
    return "Test1"

@Voice_Call_Callback.route("/Voice", methods=['GET', 'POST'])
def Voice():
        print(Task_URL)
        Logger(Host,"in /Voice", "INFO")
        return Redirect(Task_URL + "/Listen_For_Hello")

@Voice_Call_Callback.route("/Listen_For_Hello", methods=['GET', 'POST'])
def Listen_For_Hello():
        return Listen(1,1,Task_URL + "/Listen_For_Hello", Task_URL + "/Play_Greeting_Message") 

@Voice_Call_Callback.route("/Play_Greeting_Message", methods=['GET', 'POST'])
def Play_Greeting_Message():
        Logger(Host,"in /Play_Greeting_Message", "INFO")
        return Play(GlobalVariables.Voice_Callback.Welcome_Message, Task_URL + "/Play_Explain_Message")

@Voice_Call_Callback.route("/Play_Explain_Message", methods=['GET', 'POST'])
def Play_Explain_Message():
        Logger(Host,"in /Play_Explain_Message", "INFO")        
        return Play(GlobalVariables.Voice_Callback.Voice_Callback_Explaination_Message, Task_URL + "/Listen_For_Answer")

@Voice_Call_Callback.route("/Listen_For_Answer", methods=['GET', 'POST'])
def Listen_For_Answer():
        return Listen(Default_ListenTime_Begin,Default_ListenTime_Silence,Task_URL + "/Listen_For_Answer", Task_URL + "/Classify_Answer")

@Voice_Call_Callback.route("/Classify_Answer", methods=['GET', 'POST'])
def Classify_Answer():
    Logger(Host,"in /Classify_Answer", "INFO")
    
    Classification = Classify(GlobalVariables.LastMessage)

    print(GlobalVariables.LastMessage)
    print(Classification)

    if(Classification == "Yes"):
        return Redirect(Task_URL + "/Finalize")
    
    else:
        return Redirect(Task_URL + "/Play_Additional_Message")

@Voice_Call_Callback.route("/Play_Additional_Message", methods=['GET', 'POST'])
def Play_Additional_Message():
        Logger(Host,"in /Play_Explain_Message", "INFO")        
        return Play(GlobalVariables.Voice_Callback.Voice_Callback_Aditional_Message, Task_URL + "/Finalize")

@Voice_Call_Callback.route("/Finalize", methods=['GET', 'POST'])
def Finalize():
    with open("Attendance/" + time.strftime("%Y-%m-%d") + ".txt", "a") as fo:
        fo.write("Voice_Call_Callback OK" + "\n")

    Logger(Host,"in /Finalize/", "INFO")
    return Play(GlobalVariables.Voice_Callback.Voice_Callback_Finalize_Yes_Message,Task_URL+ "/Hangup")

@Voice_Call_Callback.route("/Hangup", methods=['GET', 'POST'])
def Hangup():
    return str(VoiceResponse())