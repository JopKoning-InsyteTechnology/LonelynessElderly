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

def Wait_Till_Done_Talking(Minimal_Wait, Timeout, Current_URL, Redirect_adress):
    #TODO: when talking too long hangup
    #TODO: Intergrating start of server in this function?
   

    if (GlobalVariables.TimeFunctionStarted == 0 or GlobalVariables.TimeLastMessage == 0):
        print("WAIT_TILL_DONE_TALKING : Global_variables are 0, waiting 1 second : ")

        sleep(1)

    TimeSinceStart = time() - GlobalVariables.TimeFunctionStarted
    TimeSilent = time() - GlobalVariables.TimeLastMessage

    print("WAIT_TILL_DONE_TALKING : TimeSinceStart : " + str(TimeSinceStart) + " | TimeSilent : " + str(TimeSilent))
    if (TimeSinceStart < Minimal_Wait):
        print("WAIT_TILL_DONE_TALKING : TimeSinceStart < minimal wait  : " + str(TimeSinceStart) + " < " + str(Minimal_Wait))
        return Redirect(Current_URL)
    
    if (TimeSilent < Timeout):
        print("WAIT_TILL_DONE_TALKING : TimeSilent < Timeout  : " + str(TimeSilent) + " < " + str(Timeout))
        return Redirect(Current_URL)

    print("WAIT_TILL_DONE_TALKING : Done, initial parameters are Minimal_Wait :" + str(Minimal_Wait) + " | Timout : " + str(Timeout))
    print("WAIT_TILL_DONE_TALKING : Done, Time total begin start of websocketconnection :" + str(TimeSinceStart) + " | Total time since last message : " + str(TimeSilent))
    print("WAIT_TILL_DONE_TALKING : Done, result :" + str(GlobalVariables.LastMessage))


    return Stop_Stream(Redirect_adress)
    sleep(0.5)

    return Redirect(Current_URL)




def Redirect(Redirect):
    resp = VoiceResponse()
    resp.redirect(Config.BASE_URL + Redirect)
    return str(resp)


def Wait_for_answer(ActionNext):
    start = Start()    
    resp = VoiceResponse()
    start.stream(url= Config.BASE_URL.replace('https://',"wss://") + "/" + Config.STREAM_URL)
    #start.stream(url=f'wss://{request.host}/stream_google')
    resp.append(start)
    gather = Gather(input='speech', language='nl-NL', hints='ja, nee, graag, mogelijk, leuk, bridgen, vanavond, doe, ik, mee, niet, fijn, gezellig, samen, wat, hoe, wanneer, bellen, dat, dit, dus, dan', speechTimeout = 60, Action = ActionNext)
    resp.append(gather)
    return str(resp)

def Play(File, Redirect):
    resp = VoiceResponse()
    resp.play(Config.BASE_URL + "/" + Config.STATIC_URL + "/" + File + ".mp3")
    resp.redirect(Config.BASE_URL + Redirect)
    return str(resp)
