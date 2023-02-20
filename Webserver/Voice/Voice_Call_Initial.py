# Flask Imports
from flask import Blueprint, request

# Twilio Imports
from twilio.twiml.voice_response import VoiceResponse

# Configuration Imports
import Config.General.General_Config as Config

# Import Functions
from Functions.General import Listen, Play, Redirect, Classify, Logger, Print_Log

# from GlobalVariables import Voice_Initial, LastMessage
import GlobalVariables

import requests, time


Default_ListenTime_Begin = 1.5
Default_ListenTime_Silence = 1.5


Voice_Call_Initial = Blueprint('Voice_Call_Initial', __name__,
    static_folder='static')

Task_URL = "/" + Voice_Call_Initial.name

Host = "VOICE_CALL_INITIAL"
## Get the complete URL to this blueprint file
#
Errors = 0

@Voice_Call_Initial.route('/Start', methods=['GET', 'POST'])
def list():
    return "Test1"


@Voice_Call_Initial.route("/Voice", methods=['GET', 'POST'])
def Voice():
        Print_Log(Task_URL)
        Logger(Host,"in /Voice", "INFO")
        # Print_Log(request.url_root)
        # Print_Log(request.url_rule)
        # Print_Log(request.url_rule.rule)
        # Print_Log(Voice_Call_Initial.name)

        return Redirect(Task_URL + "/Listen_For_Hello")

@Voice_Call_Initial.route("/Listen_For_Hello", methods=['GET', 'POST'])
def Listen_For_Hello():
        return Listen(1,1,Task_URL + "/Listen_For_Hello", Task_URL + "/Play_Greeting_Message") 

@Voice_Call_Initial.route("/Play_Greeting_Message", methods=['GET', 'POST'])
def Play_Greeting_Message():
        Logger(Host,"in /Play_Greeting_Message", "INFO")
        return Play(GlobalVariables.Voice_Initial.Welcome_Message, Task_URL + "/Play_Explain_Message")

@Voice_Call_Initial.route("/Play_Explain_Message", methods=['GET', 'POST'])
def Play_Explain_Message():
        Logger(Host,"in /Play_Explain_Message", "INFO")        
        return Play(GlobalVariables.Voice_Initial.Explanation_Message, Task_URL + "/Listen_For_Answer")

@Voice_Call_Initial.route("/Listen_For_Answer", methods=['GET', 'POST'])
def Listen_For_Answer():
        
        return Listen(Default_ListenTime_Begin,Default_ListenTime_Silence,Task_URL + "/Listen_For_Answer", Task_URL + "/Classify_Answer")

@Voice_Call_Initial.route("/Classify_Answer", methods=['GET', 'POST'])
def Classify_Answer():
        Logger(Host,"in /Classify_Answer", "INFO")
        
        global Errors

        Classification = Classify(GlobalVariables.LastMessage)

        Print_Log(GlobalVariables.LastMessage)
        Print_Log(Classification)

        if(Classification == "Yes"):
            return Redirect(Task_URL + "/Play_Check_Answer_Message/Yes")
        
        elif(Classification == "No"):
            return Redirect(Task_URL + "/Play_Check_Answer_Message/No")

        else:
            if (Errors >= 3):
                Errors = 0
                return Redirect(Task_URL + "/Finalize/Unclear")
            else:
                Errors += 1
                return Redirect(Task_URL + "/Play_Check_Answer_Message/Unclear")

@Voice_Call_Initial.route("/Play_Check_Answer_Message/<Classification>", methods=['GET', 'POST'])
def Classification(Classification):
    Logger(Host,"in /Play_Check_Answer_Message/" + Classification, "INFO")
    

    if(Classification == "Yes"):
        return Play(GlobalVariables.Voice_Initial.Check_Yes_Message, Task_URL + "/Listen_For_Check_Answer_Result/Yes")
    
    elif(Classification == "No"):
        return Play(GlobalVariables.Voice_Initial.Check_No_Message, Task_URL + "/Listen_For_Check_Answer_Result/No")

    else:
        return Play(GlobalVariables.Voice_Initial.Check_Unclear_Message, Task_URL + "/Listen_For_Answer")

@Voice_Call_Initial.route("/Listen_For_Check_Answer_Result/<Classification>", methods=['GET', 'POST'])
def Listen_For_Check_Answer_Result(Classification):
    
    return Listen(Default_ListenTime_Begin,Default_ListenTime_Silence,Task_URL + "/Listen_For_Check_Answer_Result/" + Classification, Task_URL +"/Classify_Answer_2/" + Classification)

@Voice_Call_Initial.route("/Classify_Answer_2/<Classification>", methods=['GET', 'POST'])
def Classify_Answer_2(Classification):
    Logger(Host,"in /Classify_Answer_2/" + Classification, "INFO")

    global Errors

    result = Classify(GlobalVariables.LastMessage)

    Print_Log("Message to Classify : " + GlobalVariables.LastMessage)
    Print_Log("Result of classification : " + result)
    Print_Log("Number of errors : " + str(Errors))

    if(result == "Yes"):
        Errors = 0
        return Redirect(Task_URL + "/Finalize/" + Classification)
    

    elif(result == "No"):
        if (Errors >= 3):
            Errors = 0
            return Redirect(Task_URL + "/Finalize/Unclear")
        Errors += 1
        if(Classification == "No"):
            return Redirect(Task_URL + "/Play_Check_Answer_Message/Yes")
        return Redirect(Task_URL + "/Play_Check_Answer_Message/No")


    else:
        if (Errors >= 3):
            Errors = 0
            return Redirect(Task_URL + "/Finalize/Unclear")
        else:
            Errors += 1
            return Redirect(Task_URL + "/Play_Check_Answer_Message/Unclear")

@Voice_Call_Initial.route("/Finalize/<Classification>", methods=['GET', 'POST'])
def Finalize(Classification):
    Logger(Host,"in /Finalize/" + Classification, "INFO")
    
    with open("Attendance/" + time.strftime("%Y-%m-%d") + ".txt", "a") as fo:
        fo.write("Voice_Call_Initial->" + Classification + "\n")

    if(Classification == "Yes"):
        return Play(GlobalVariables.Voice_Initial.Finalize_Yes_Message,Task_URL+ "/Hangup")
    
    elif(Classification == "No"):
        return Play(GlobalVariables.Voice_Initial.Finalize_No_Message, Task_URL + "/Hangup")
    else:
        return Play(GlobalVariables.Voice_Initial.Finalize_Unclear_Message, Task_URL + "/Hangup")

@Voice_Call_Initial.route("/Hangup", methods=['GET', 'POST'])
def Hangup():
    return str(VoiceResponse())

 