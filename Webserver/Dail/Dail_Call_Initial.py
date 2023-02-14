from flask import Blueprint, request

# Import Functions
from Functions.General import  Play, Redirect, Logger, Listen, ClassifyDailInput, GatherDailInput, ClassifyDailInputSimple
import GlobalVariables
from twilio.twiml.voice_response import VoiceResponse

import time

Dail_Call_Initial = Blueprint('Dail_Call_Initial', __name__,
    static_folder='static')

Task_URL = "/" + Dail_Call_Initial.name

Errors = 0

Host = "DAIL_CALL_INITIAL"

@Dail_Call_Initial.route('/Start',  methods=['GET', 'POST'])
def list():
    return "Test1"

@Dail_Call_Initial.route("/Dail", methods=['GET', 'POST'])
def Voice():
        print(Task_URL)
        Logger(Host,"in /Voice", "INFO")
        return Redirect(Task_URL + "/Listen_For_Hello")

@Dail_Call_Initial.route("/Listen_For_Hello", methods=['GET', 'POST'])
def Listen_For_Hello():
        return Listen(1,1,Task_URL + "/Listen_For_Hello", Task_URL + "/Play_Greeting_Message") 

@Dail_Call_Initial.route("/Play_Greeting_Message", methods=['GET', 'POST'])
def Play_Greeting_Message():
        Logger(Host,"in /Play_Greeting_Message", "INFO")
        return Play(GlobalVariables.Dail_Initial.Welcome_Message, Task_URL + "/Play_Explain_Message")

@Dail_Call_Initial.route("/Play_Explain_Message", methods=['GET', 'POST'])
def Play_Explain_Message():
        Logger(Host,"in /Play_Explain_Message", "INFO")        
        return Play(GlobalVariables.Dail_Initial.Explanation_Message, Task_URL + "/Listen_For_Answer")

@Dail_Call_Initial.route("/Listen_For_Answer", methods=['GET', 'POST'])
def Listen_For_Answer():
        return GatherDailInput(Task_URL + "/Classify_Answer", Task_URL + "/No_Input")
        #return Listen(Default_ListenTime_Begin,Default_ListenTime_Silence,Task_URL + "/Listen_For_Answer", Task_URL + "/Classify_Answer")@app.route('/Classify_Gather', methods=['GET', 'POST'])

@Dail_Call_Initial.route("/No_Input", methods=['GET', 'POST'])
def No_Input():
    global Errors
    if Errors >= 3:
        return Redirect(Task_URL + "/Finalize/Unclear")
    Errors += 1

    return Play(GlobalVariables.Dail_Initial.Check_Unclear_Message, Task_URL + "/Play_Explain_Message")
    return Redirect("/Play_Explain_Message")
    #return Listen(Default_ListenTime_Begin,Default_ListenTime_Silence,Task_URL + "/Listen_For_Answer", Task_URL + "/Classify_Answer")@app.route('/Classify_Gather', methods=['GET', 'POST'])


@Dail_Call_Initial.route("/Classify_Answer", methods=['GET', 'POST'])
def Classify_Answer():
    return ClassifyDailInput(request, Task_URL + "/Play_Check_Answer_Message/Yes", Task_URL + "/Play_Check_Answer_Message/No", Task_URL + "/Play_Check_Answer_Message/Unclear", Task_URL + "/Play_Check_Answer_Message/Unclear")


@Dail_Call_Initial.route("/Play_Check_Answer_Message/<Classification>", methods=['GET', 'POST'])
def Classification(Classification):
    Logger(Host,"in /Play_Check_Answer_Message/" + Classification, "INFO")

    if(Classification == "Yes"):
        return Play(GlobalVariables.Dail_Initial.Check_Yes_Message, Task_URL + "/Listen_For_Check_Answer_Result/Yes")
    
    elif(Classification == "No"):
        return Play(GlobalVariables.Dail_Initial.Check_No_Message, Task_URL + "/Listen_For_Check_Answer_Result/No")

    else:
        return Play(GlobalVariables.Dail_Initial.Check_Unclear_Message, Task_URL + "/Listen_For_Answer")

@Dail_Call_Initial.route("/Listen_For_Check_Answer_Result/<Classification>", methods=['GET', 'POST'])
def Listen_For_Check_Answer_Result(Classification):
    return GatherDailInput( Task_URL +"/Classify_Answer_2/" + Classification, Task_URL + "/Listen_For_Check_Answer_Result/" + Classification)

@Dail_Call_Initial.route("/Classify_Answer_2/<Classification>", methods=['GET', 'POST'])
def Classify_Answer_2(Classification):
    Logger(Host,"in /Classify_Answer_2/" + Classification, "INFO")

    global Errors

    result = ClassifyDailInputSimple(request)
    
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


@Dail_Call_Initial.route("/Finalize/<Classification>", methods=['GET', 'POST'])
def Finalize(Classification):
    Logger(Host,"in /Finalize/" + Classification, "INFO")
    
    with open("Attendance/" + time.strftime("%Y-%m-%d") + ".txt", "a") as fo:
        fo.write("Dail_Call_Initial->" + Classification + "\n")

    if(Classification == "Yes"):
        return Play(GlobalVariables.Dail_Initial.Finalize_Yes_Message,Task_URL+ "/Hangup")
    
    elif(Classification == "No"):
        return Play(GlobalVariables.Dail_Initial.Finalize_No_Message, Task_URL + "/Hangup")
    else:
        return Play(GlobalVariables.Dail_Initial.Finalize_Unclear_Message, Task_URL + "/Hangup")

@Dail_Call_Initial.route("/Hangup", methods=['GET', 'POST'])
def Hangup():
    return str(VoiceResponse())

 