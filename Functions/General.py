from twilio.twiml.voice_response import Start, Stop, Gather, Stream, VoiceResponse
import Config.General.General_Config as Config
from flask import request
import GlobalVariables
from time import time, sleep, strftime


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
    sleep(0.2)

    if(GlobalVariables.StreamStarted == False and GlobalVariables.IsActive == True):
        Print_Log("LISTEN: stream is not yet started, but is still active. Wait one second and try again")
        sleep(1)
        return Redirect(Current_URL)

    if (GlobalVariables.StreamStarted == False):
        GlobalVariables.StreamStarted = True
        return Start_Stream(Current_URL)

    if (GlobalVariables.TimeFunctionStarted == 0 or GlobalVariables.TimeLastMessage == 0):
        Print_Log("Listen : Global_variables are 0, Trying again: ")
        sleep(0.2)
        return Redirect(Current_URL)


    TimeSinceStart = time() - GlobalVariables.TimeFunctionStarted
    TimeSilent = time() - GlobalVariables.TimeLastMessage

    Print_Log("Listen : TimeSinceStart : " + str(TimeSinceStart) + " | TimeSilent : " + str(TimeSilent))
    if (TimeSinceStart < Minimal_Wait):
        Print_Log("Listen : TimeSinceStart < minimal wait  : " + str(TimeSinceStart) + " < " + str(Minimal_Wait))
        sleep(0.2)
        return Redirect(Current_URL)
    
    if (TimeSilent < Timeout):
        Print_Log("Listen : TimeSilent < Timeout  : " + str(TimeSilent) + " < " + str(Timeout))
        sleep(0.2)
        return Redirect(Current_URL)

    Print_Log("Listen : Done, initial parameters are Minimal_Wait :" + str(Minimal_Wait) + " | Timout : " + str(Timeout))
    Print_Log("Listen : Done, Time total begin start of websocketconnection :" + str(TimeSinceStart) + " | Total time since last message : " + str(TimeSilent))
    Print_Log("Listen : Done, result:" + str(GlobalVariables.LastMessage))

    Logger("LISTENING_FUNCTION", "Done with listening, Message was -> " + str(GlobalVariables.LastMessage), "INFO")

    GlobalVariables.StreamStarted = False
    GlobalVariables.TimeLastMessage = 0
    GlobalVariables.TimeFunctionStarted = 0

    #return Redirect(Redirect_adress)
    return Stop_Stream(Redirect_adress)
    #sleep(0.5)

    return Redirect(Current_URL)

def Print_Log(Message):
    f = open("Logging/" + GlobalVariables.FILE + "-Log", "a")
    f.write(strftime("%Y-%m-%d  %H:%M:%S") + " \t " + Message + "\n")
    f.close()

def Logger(Host, Message, Severity):
    f = open("Logging/" + GlobalVariables.FILE, "a")
    f.write(strftime("%Y-%m-%d  %H:%M:%S") + "\t" + Severity + " \t " + Host + " \t " + Message + "\n")
    f.close()

def Logger_Classification(Host, Message, Severity):
    f = open("Logging/" + GlobalVariables.FILE + "_Classification", "a")
    f.write(strftime("%Y-%m-%d  %H:%M:%S") + "\t" + Severity + " \t " + Host + " \t " + Message + "\n")
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
    Print_Log(Message)
    if Message != "" :
        Speech = Message.strip(",.").lower()
        Print_Log (Speech)
        for Classifier in GlobalVariables.NoClassifierList:
            if Classifier in Speech:
                return "No"

        for Classifier in GlobalVariables.YesClassifierList:
            if Classifier in Speech:
                return "Yes"
    
    return "Unclear"

def GatherDailInput(Redirect_on_input, Redirect_on_error):
    #TODO: Test this
    """Respond to incoming phone calls with a menu of options"""
    # Start our TwiML response
    resp = VoiceResponse()

    # Start our <Gather> verb
    gather = Gather(num_digits=1, action=Redirect_on_input, timeout = 10)
    resp.append(gather)

    # If the user doesn't select an option, redirect them into a loop
    resp.redirect(Redirect_on_error)

    return str(resp)
    
def ClassifyDailInput(Input, Redirect_on_1, Redirect_on_2,Redirect_on_3, Redirect_on_other):

    #TODO: Test this
    """Processes results from the <Gather> prompt in /voice"""
    # Start our TwiML response
    resp = VoiceResponse()
    global Classification

    # If Twilio's request to our app included already gathered digits,
    # process them
    if 'Digits' in Input.values:
        # Get which digit the caller chose
        choice = Input.values['Digits']

        # <Say> a different message depending on the caller's choice
        if choice == '1':
            resp.redirect(Redirect_on_1)
            return str(resp)
        elif choice == '2':
            resp.redirect(Redirect_on_2)
            return str(resp)
        elif choice == '3':
            resp.redirect(Redirect_on_3)
            return str(resp)
        else:
            # If the caller didn't choose 1 or 2, apologize and ask them again
            return str(resp.redirect(Redirect_on_other))
    else: 
        #resp.say("Er is iets mis gegaan, we proberen het opnieuw")
        return str(resp.redirect(Redirect_on_other))

def ClassifyDailInputSimple(Input):

    #TODO: Test this
    """Processes results from the <Gather> prompt in /voice"""
    # Start our TwiML response
    resp = VoiceResponse()
    global Classification

    # If Twilio's request to our app included already gathered digits,
    # process them
    if 'Digits' in Input.values:
        # Get which digit the caller chose
        choice = Input.values['Digits']

        # <Say> a different message depending on the caller's choice
        if choice == '1':
            return "Yes"
        elif choice == '2':
            return "No"
        elif choice == '3':
            return "Unclear"
        else:
            # If the caller didn't choose 1 or 2, apologize and ask them again
            return "Unclear"
    else: 
        #resp.say("Er is iets mis gegaan, we proberen het opnieuw")
            return "Unclear"