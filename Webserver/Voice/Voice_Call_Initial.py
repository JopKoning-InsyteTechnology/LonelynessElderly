# Flask Imports
from flask import Blueprint, request

# Twilio Imports
from twilio.twiml.voice_response import VoiceResponse

# Configuration Imports
import Config.General.General_Config as Config

# Import Functions
from Functions.General import Listen, Play, Redirect, Classify

# from GlobalVariables import Voice_Initial, LastMessage
import GlobalVariables




Voice_Call_Initial = Blueprint('Voice_Call_Initial', __name__,
    static_folder='static')

Task_URL = "/" + Voice_Call_Initial.name
## Get the complete URL to this blueprint file
#
Errors = 0

@Voice_Call_Initial.route('/Start', methods=['GET', 'POST'])
def list():
    return "Test1"


@Voice_Call_Initial.route("/Voice", methods=['GET', 'POST'])
def Voice():
        print(Task_URL)
        # print(request.url_root)
        # print(request.url_rule)
        # print(request.url_rule.rule)
        # print(Voice_Call_Initial.name)

        return Redirect(Task_URL + "/Listen_For_Hello")

@Voice_Call_Initial.route("/Listen_For_Hello", methods=['GET', 'POST'])
def Listen_For_Hello():
        return Listen(1,2,Task_URL + "/Listen_For_Hello", Task_URL + "/Play_Greeting_Message") 

@Voice_Call_Initial.route("/Play_Greeting_Message", methods=['GET', 'POST'])
def Play_Greeting_Message():
        
        return Play(GlobalVariables.Voice_Initial.Welcome_Message, Task_URL + "/Play_Explain_Message")

@Voice_Call_Initial.route("/Play_Explain_Message", methods=['GET', 'POST'])
def Play_Explain_Message():
        
        return Play(GlobalVariables.Voice_Initial.Explanation_Message, Task_URL + "/Listen_For_Answer")

@Voice_Call_Initial.route("/Listen_For_Answer", methods=['GET', 'POST'])
def Listen_For_Answer():
        
        return Listen(3,2,Task_URL + "/Listen_For_Answer", Task_URL + "/Classify_Answer")

@Voice_Call_Initial.route("/Classify_Answer", methods=['GET', 'POST'])
def Classify_Answer():
        
        global Errors

        Classification = Classify(GlobalVariables.LastMessage)

        print(GlobalVariables.LastMessage)
        print(Classification)

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
    

    if(Classification == "Yes"):
        return Play(GlobalVariables.Voice_Initial.Check_Yes_Message, Task_URL + "/Listen_For_Check_Answer_Result/Yes")
    
    elif(Classification == "No"):
        return Play(GlobalVariables.Voice_Initial.Check_No_Message, Task_URL + "/Listen_For_Check_Answer_Result/No")

    else:
        return Play(GlobalVariables.Voice_Initial.Check_Unclear_Message, Task_URL + "/Listen_For_Answer")

@Voice_Call_Initial.route("/Listen_For_Check_Answer_Result/<Classification>", methods=['GET', 'POST'])
def Listen_For_Check_Answer_Result(Classification):
    
    return Listen(2,2,Task_URL + "/Listen_For_Check_Answer_Result/" + Classification, Task_URL +"/Classify_Answer_2/" + Classification)

@Voice_Call_Initial.route("/Classify_Answer_2/<Classification>", methods=['GET', 'POST'])
def Classify_Answer_2(Classification):
    
    global Errors

    result = Classify(GlobalVariables.LastMessage)

    print("Message to Classify : " + GlobalVariables.LastMessage)
    print("Result of classification : " + result)
    print("Number of errors : " + str(Errors))

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
    

    if(Classification == "Yes"):
        return Play(GlobalVariables.Voice_Initial.Finalize_Yes_Message, "")
    
    elif(Classification == "No"):
        return Play(GlobalVariables.Voice_Initial.Finalize_No_Message, Task_URL + "")
    else:
        return Play(GlobalVariables.Voice_Initial.Finalize_Unclear_Message, Task_URL + "")
