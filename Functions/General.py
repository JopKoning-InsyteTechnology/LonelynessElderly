from twilio.twiml.voice_response import Start, Stop, Gather, Stream, VoiceResponse
import Config.General.General_Config as Config
from flask import request
import GlobalVariables
from time import time, sleep


def Start_Stream(Redirect):
    start = Start()
    resp = VoiceResponse()
    start.stream(name = "Audio_Stream", url= Config.BASE_URL.replace('https://',"wss://") + "/" + Config.STREAM_URL)
    resp.append(start)
    resp.redirect(Config.BASE_URL + Redirect)
    return str(resp)

def Stop_Stream(Redirect):
    stop = Stop()
    resp = VoiceResponse()
    stop.stream(name = "Audio_Stream")
    resp.append(stop)
    resp.redirect(Config.BASE_URL + Redirect)
    return str(resp)


def Listen(Minimal_Wait, Timeout, Current_URL, Redirect_adress):
    #TODO: when talking too long hangup
    #TODO: test this in multiple times and ways
   
    if(GlobalVariables.StreamStarted == False and GlobalVariables.IsActive == True):
        print("LISTEN: stream is not yet started, but is still active. Wait one second and try again")
        sleep(1)
        return Redirect(Current_URL)

    if (GlobalVariables.StreamStarted == False):
        GlobalVariables.StreamStarted = True
        return Start_Stream(Current_URL)

    if (GlobalVariables.TimeFunctionStarted == 0 or GlobalVariables.TimeLastMessage == 0):
        print("Listen : Global_variables are 0, Trying again: ")
        return Redirect(Current_URL)


    TimeSinceStart = time() - GlobalVariables.TimeFunctionStarted
    TimeSilent = time() - GlobalVariables.TimeLastMessage

    print("Listen : TimeSinceStart : " + str(TimeSinceStart) + " | TimeSilent : " + str(TimeSilent))
    if (TimeSinceStart < Minimal_Wait):
        print("Listen : TimeSinceStart < minimal wait  : " + str(TimeSinceStart) + " < " + str(Minimal_Wait))
        return Redirect(Current_URL)
    
    if (TimeSilent < Timeout):
        print("Listen : TimeSilent < Timeout  : " + str(TimeSilent) + " < " + str(Timeout))
        return Redirect(Current_URL)

    print("Listen : Done, initial parameters are Minimal_Wait :" + str(Minimal_Wait) + " | Timout : " + str(Timeout))
    print("Listen : Done, Time total begin start of websocketconnection :" + str(TimeSinceStart) + " | Total time since last message : " + str(TimeSilent))
    print("Listen : Done, result:" + str(GlobalVariables.LastMessage))

    Logger("LISTENING_FUNCTION", "Done with listening, Message was -> " + str(GlobalVariables.LastMessage), "INFO")

    GlobalVariables.StreamStarted = False
    GlobalVariables.TimeLastMessage = 0
    GlobalVariables.TimeFunctionStarted = 0

    #return Redirect(Redirect_adress)
    return Stop_Stream(Redirect_adress)
    #sleep(0.5)

    return Redirect(Current_URL)


def Logger(Host, Messsage, Severity):
    f = open("Logging/" + GlobalVariables.FILE, "a")
    f.write(Severity + " : " + Host + " : " + Messsage + "\n")
    f.close()


def Redirect(Redirect):
    resp = VoiceResponse()
    resp.redirect(Config.BASE_URL + Redirect)
    return str(resp)


# def Wait_for_answer(ActionNext):
#     start = Start()    
#     resp = VoiceResponse()
#     start.stream(url= Config.BASE_URL.replace('https://',"wss://") + "/" + Config.STREAM_URL)
#     #start.stream(url=f'wss://{request.host}/stream_google')
#     resp.append(start)
#     gather = Gather(input='speech', language='nl-NL', hints='ja, nee, graag, mogelijk, leuk, bridgen, vanavond, doe, ik, mee, niet, fijn, gezellig, samen, wat, hoe, wanneer, bellen, dat, dit, dus, dan', speechTimeout = 60, Action = ActionNext)
#     resp.append(gather)
#     return str(resp)

def Play(File, Redirect):
    resp = VoiceResponse()
    resp.play(Config.BASE_URL + "/" + Config.STATIC_URL + "/" + File + ".mp3")
    resp.redirect(Config.BASE_URL + Redirect)
    return str(resp)

def Classify(Message):
    print(Message)
    if Message != "" :
        Speech = Message.strip(",.").lower()
        print (Speech)
        print (GlobalVariables.NoClassifierList)
        for Classifier in GlobalVariables.NoClassifierList:
            if Classifier in Speech:
                return "No"

        for Classifier in GlobalVariables.YesClassifierList:
            if Classifier in Speech:
                return "Yes"
    
    return "Unclear"