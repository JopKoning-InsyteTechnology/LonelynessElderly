import Credentials as CRD

import requests
tes

from argparse import Action
from ast import Global
from flask import Flask, request, send_from_directory, url_for

from flask_sock import Sock
import json, base64, audioop

import os, threading
from google.cloud.speech import RecognitionConfig, StreamingRecognitionConfig
from SpeechClientBridge import SpeechClientBridge

from twilio.twiml.voice_response import VoiceResponse,  Gather, Start, Stream
from time import time ,sleep

from twilio.rest import Client

YesClassifierList = ['ja', 'dat klopt']
NoClassifierList = ['nee', 'dat klopt niet']

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'key.json'

URL = CRD.Config["BASE_URL"]

client = Client(CRD.Config["TWILIO_ACCOUNT_SID"], CRD.Config["TWILIO_AUTH_TOKEN"])

config = RecognitionConfig(
    encoding=RecognitionConfig.AudioEncoding.MULAW,
    sample_rate_hertz=8000,
    language_code="nl-NL",
)
streaming_config = StreamingRecognitionConfig(config=config, interim_results=True)

CL = '\x1b[0K'
BS = '\x08'

app = Flask(__name__)
sock = Sock(app)

timer = time()
NextAction = ""

TimeToWait_begin = 3 #how long do you wait at the start of a message
TimeToWait_begin_Default = 3
TimeToWait_begin_Initial = 1

TimeToWaitDefault = 0.5 #how long to wait once someone stops talking

LastTranscription = 0
LastMessage = ""


TimeToWait = 2


TranscriptionDone = 0
Classification = ""
TimesUnclear = 0

METHOD = ""
CHECK = False #This variable helps with the classification routing. It is set to true when the check question is asked.

####################################### FUNCTION DEFINITION ##########################################
def ClearAllVariables():
    global TimeToWait_begin
    TimeToWait_begin = 3 #how long do you wait at the start of a message
    global TimeToWait_begin_Default
    TimeToWait_begin_Default = 3
    global TimeToWait_begin_Initial
    TimeToWait_begin_Initial = 1
    global TimeToWaitDefault
    TimeToWaitDefault = 0.5 #how long to wait once someone stops talking
    global LastTranscription
    LastTranscription = 0
    global LastMessage
    LastMessage = ""
    global TimeToWait
    TimeToWait = 2
    global TranscriptionDone
    TranscriptionDone = 0
    global Classification
    Classification = ""
    global TimesUnclear
    TimesUnclear = 0

def Say(Text, Redirect):
    resp = VoiceResponse()
    resp.say(Text,language='nl-NL', voice="Polly.Ruben")
    resp.redirect(URL+Redirect)
    return str(resp)

def Play(File, Redirect):
    resp = VoiceResponse()
    resp.play(URL+ "static/" + File+ ".mp3")
    resp.redirect(URL+Redirect)
    return str(resp)

def Wait_for_answer_short(Waittime, ActionNext):
    global TimeToWait
    global TimeToWaitDefault
    global NextAction
    global TranscriptionDone

    resp = VoiceResponse()
    start = Start()
    
    #Waittime max 60 seconds due to gather
    if(Waittime == 0):
        TimeToWait = TimeToWaitDefault
    else:
        TimeToWait = Waittime

    NextAction = ActionNext
    
    TranscriptionDone = 0
    start.stream(url=f'wss://{request.host}/stream_google')
    resp.append(start)
    gather = Gather(input='speech', language='nl-NL', hints='ja, nee, graag, mogelijk, leuk, bridgen, vanavond, doe, ik, mee, niet, fijn, gezellig, samen, wat, hoe, wanneer, bellen, dat, dit, dus, dan', speechTimeout = 60, Action = NextAction)
    resp.append(gather)
    return str(resp)

def Wait_for_answer(Waittime, ActionNext, Type, Content):
    global TimeToWait
    global TimeToWaitDefault
    global NextAction
    global TranscriptionDone

    resp = VoiceResponse()
    start = Start()
    
    #Waittime max 60 seconds due to gather
    if(Waittime == 0):
        TimeToWait = TimeToWaitDefault
    else:
        TimeToWait = Waittime

    NextAction = ActionNext
    
    TranscriptionDone = 0
    start.stream(url=f'wss://{request.host}/stream_google')
    resp.append(start)
    gather = Gather(input='speech', language='nl-NL', hints='ja, nee, graag, mogelijk, leuk, bridgen, vanavond, doe, ik, mee, niet, fijn, gezellig, samen, wat, hoe, wanneer, bellen, dat, dit, dus, dan', speechTimeout = 60, Action = NextAction)
    if (Type == "Say"):
        resp.say(Content,language='nl-NL', voice="Polly.Ruben")

    if (Type == "Play"): 
        gather.play(URL+ "static/" + Content + ".mp3")

    resp.append(gather)
    return str(resp)

def Classify_transcription(Transcript):

    if Transcript != "" :
        Speech = Transcript.strip(",.").lower()
        # with open("Transcribed_call.txt", "w") as fo:
        #     fo.write(Speech)
        # if 'Confidence' in request.values:
        #     with open("Transcribed_call_confidence.txt", "w") as fo:
        #         fo.write(request.values['Confidence'])

        for Classifier in NoClassifierList:
            if Classifier in Speech:
                return "Nee"

        for Classifier in YesClassifierList:
            if Classifier in Speech:
                return "Ja"
        
        return "Unclear"
        resp.say('onduidelijk antwoord',language='nl-NL', voice="Polly.Ruben") #Polly.Lotte

    else:
        return "None"

@app.route('/static/<path:path>')
def send_file(path):
    return send_from_directory('static', path)

####################################### FUNCTION DEFINITION END ##########################################

@app.route("/Voice", methods=['GET', 'POST'])
def Voice():

        with open("Transcribed_call.txt", "a") as fo:
                        fo.write("Starting Call to voice\n")
                        
        resp = VoiceResponse()
        global TimeToWait_begin
        global TimeToWait_begin_Initial
        app.logger.info("Setting TimeToWait_begin before setting = " + str(TimeToWait_begin))
        TimeToWait_begin = TimeToWait_begin_Initial
        app.logger.info("Setting TimeToWait_begin after setting = " + str(TimeToWait_begin))
        global METHOD
        METHOD = "VOICE"
        resp.redirect(URL+"Wait_for_greeting")
        return str(resp)

@app.route("/Voice_Callback", methods=['GET', 'POST'])
def Voice_Callback():
        resp = VoiceResponse()
        global TimeToWait_begin
        global TimeToWait_begin_Initial
        app.logger.info("Setting TimeToWait_begin before setting = " + str(TimeToWait_begin))
        TimeToWait_begin = TimeToWait_begin_Initial
        app.logger.info("Setting TimeToWait_begin after setting = " + str(TimeToWait_begin))
        global METHOD
        METHOD = "VOICE_CALLBACK"
        resp.redirect(URL+"Wait_for_greeting")
        return str(resp)

@app.route("/Dail_Menu", methods=['GET', 'POST'])
def Dail_Menu():
        resp = VoiceResponse()

        global TimeToWait_begin
        global TimeToWait_begin_Initial
        app.logger.info("Setting TimeToWait_begin before setting = " + str(TimeToWait_begin))
        TimeToWait_begin = TimeToWait_begin_Initial
        app.logger.info("Setting TimeToWait_begin after setting = " + str(TimeToWait_begin))

        global METHOD
        METHOD = "DAIL"
        resp.redirect(URL+"Wait_for_greeting")
        return str(resp)

@app.route("/Dail_Menu_Callback", methods=['GET', 'POST'])
def Dail_Menu_Callback():
        resp = VoiceResponse()

        global TimeToWait_begin
        global TimeToWait_begin_Initial
        app.logger.info("Setting TimeToWait_begin before setting = " + str(TimeToWait_begin))
        TimeToWait_begin = TimeToWait_begin_Initial
        app.logger.info("Setting TimeToWait_begin after setting = " + str(TimeToWait_begin))

        global METHOD
        METHOD = "DAIL_CALLBACK"
        resp.redirect(URL+"Wait_for_greeting")
        return str(resp)

@app.route("/Wait_for_greeting", methods=['GET', 'POST'])
def Wait_for_greeting():
    """Wait for a person to respond"""

    return Wait_for_answer_short(0, "Greet")

@app.route("/Greet", methods=['GET', 'POST'])
def Greet():
    return Play("Greet", "Ask_for_activity_speech")
    return Say("Hallo, u spreekt met jop koning van de activiteitenorganisatie", "Ask_for_activity_speech" )

@app.route("/Ask_for_activity_speech", methods=['GET', 'POST'])
def Ask_for_activity_speech():
    global METHOD
    if(METHOD == "VOICE"):
        return Play("Ask_for_activity_speech_voice", "Wait_for_activity_reaction" )
        return Say("We gaan vanavond bridgen, heeft u zin om mee te doen?", "Wait_for_activity_reaction" )
    if(METHOD == "DAIL"):
        return Play("Ask_for_activity_speech_dail", "Gather_Dail" )
        return Say("We gaan vanavond bridgen, toets 1 als u graag mee doet, toets 2 als u niet mee wilt doen, toets 3 als ik u later terug moet bellen", "Gather_Dail" )
    if(METHOD == "VOICE_CALLBACK"):
        return Play("Ask_for_activity_speech_voice_callback", "Wait_for_activity_reaction" )
    if(METHOD == "DAIL_CALLBACK"):
        return Play("Ask_for_activity_speech_dail_callback", "Gather_Dail" )

@app.route("/Gather_Dail", methods=['GET', 'POST'])
def Gather_Dail():
    """Respond to incoming phone calls with a menu of options"""
    # Start our TwiML response
    resp = VoiceResponse()

    # Start our <Gather> verb
    gather = Gather(num_digits=1, action='/Classify_Gather')
    #gather.say('Druk 1 om mee te doen, druk 2 om niet mee te doen')
    #gather.play("/static/Welkom.mp3")

    resp.append(gather)

    # If the user doesn't select an option, redirect them into a loop
    resp.redirect('/Ask_for_activity_speech')

    return str(resp)

@app.route('/Classify_Gather', methods=['GET', 'POST'])
def gather():
    """Processes results from the <Gather> prompt in /voice"""
    # Start our TwiML response
    resp = VoiceResponse()
    global Classification


    # If Twilio's request to our app included already gathered digits,
    # process them
    if 'Digits' in request.values:
        # Get which digit the caller chose
        choice = request.values['Digits']

        # <Say> a different message depending on the caller's choice
        if choice == '1':
            # resp.play("/static/Aangemeld.mp3")
            Classification = "Ja"
            resp.redirect('/Play_Thanks_3')
            return str(resp)
        elif choice == '2':
            Classification = "Nee"
            # resp.play("/static/Afgemeld.mp3")
            resp.redirect('/Play_Thanks_3')
            return str(resp)
        elif choice == '3':
            Classification = "Call_Later"
            # resp.play("/static/Afgemeld.mp3")
            resp.redirect('/Play_Thanks_3')
            return str(resp)
        else:
            # If the caller didn't choose 1 or 2, apologize and ask them again

            # resp.say("Er is iets mis gegaan, we proberen het opnieuw")
            # resp.redirect('/Ask_for_activity_speech')
            return Play("Error", "Ask_for_activity_speech" )
            return Say("Er is iets mis gegaan, we proberen het opnieuw", "Ask_for_activity_speech")
    else: 
        #resp.say("Er is iets mis gegaan, we proberen het opnieuw")
        return Play("Error", "Ask_for_activity_speech" )

        resp.redirect('/Ask_for_activity_speech')
        return str(resp)

@app.route("/Play_Thanks_3", methods=['GET', 'POST'])
def Play_Thanks_3():
    global Classification
    global METHOD
    if (METHOD == "DAIL_CALLBACK" and  Classification == "Nee"):
        return Play("DankUWel", "Callback_Additional_Message")
    return Play("DankUWel", "Finalize")
    return Say("Dank u wel!", "Finalize")

@app.route("/Callback_Additional_Message", methods=['GET', 'POST'])
def Dail_Callback_Additional_Message():
    global Classification
    Classification = "Ja"
    return Play("Callback_Additional_Message", "Finalize")
    return Say("Dank u wel!", "Finalize")

@app.route("/Wait_for_activity_reaction", methods=['GET', 'POST'])
def Wait_for_activity_reaction():
    return Wait_for_answer_short(0, "Play_Thanks")

@app.route("/Play_Thanks", methods=['GET', 'POST'])
def Play_Thanks():
    return Play("DankUWel", "Classify_activity_reaction")
    return Say("Dank u wel!", "Classify_activity_reaction")

@app.route("/Classify_activity_reaction", methods=['GET', 'POST'])
def Clasify_activity_reaction():
    resp = VoiceResponse()

    global LastMessage
    app.logger.info("Classify LastMessage = " + LastMessage)
    global CHECK
    app.logger.info("CHECK = " + str(CHECK))

    global Classification
    result = Classify_transcription(LastMessage)
    if result == "Ja":
        app.logger.info("Classification = Ja")
        Classification = "Ja"
        app.logger.info("Classification = Ja")

        if (METHOD == "VOICE"):
            if (CHECK == True):
                resp.redirect(URL+"Finalize")
            resp.redirect(URL+"Activity_say_yes")
        if (METHOD == "VOICE_CALLBACK"):  
            resp.redirect(URL+"Finalize")
        resp.redirect(URL+"Activity_say_yes")

    if result == "Nee":
        app.logger.info("Classification = Nee")
        Classification = "Nee"

        if (METHOD == "VOICE"):
            if (CHECK == True):
                resp.redirect(URL+"Finalize")
            resp.redirect(URL+"Activity_say_no")
        if (METHOD == "VOICE_CALLBACK"):  
            resp.redirect(URL+"Callback_Additional_Message")
        resp.redirect(URL+"Activity_say_no")

    if result ==  "Unclear":
        resp.redirect(URL+"Activity_say_unclear")

    else :
        resp.redirect(URL+"Activity_say_unclear")

    return str(resp)

@app.route("/Activity_say_yes", methods=['GET', 'POST'])
def Activity_say_yes():
    global Classification
    app.logger.info("In Activity_say_yes, classification = " + Classification)
    return Play("Activity_say_yes", "Activity_check_yes")
    return Say("Ik heb begrepen dat je vanavond wel mee zou willen doen, klopt dit?", "Activity_check_yes")
    return Wait_for_answer(0, "Activity_check_Classify", "Say", "Klopt het dat je vanavond wel mee wilt doen?")

# @app.route("/Activity_say_yes_callback", methods=['GET', 'POST'])
# def Activity_say_yes_callback():
#     global Classification
#     app.logger.info("In Activity_say_yes_callback, classification = " + Classification)
#     return Play("Activity_say_yes_callback", "Finalize")
#     return Say("Ik heb begrepen dat je vanavond wel mee zou willen doen, klopt dit?", "Activity_check_yes")
#     return Wait_for_answer(0, "Activity_check_Classify", "Say", "Klopt het dat je vanavond wel mee wilt doen?")

@app.route("/Activity_check_yes", methods=['GET', 'POST'])
def Activity_check_yes():
    return Wait_for_answer_short(0, "Play_Thanks_2")

@app.route("/Activity_say_no", methods=['GET', 'POST'])
def Activity_say_no():
    global Classification
    app.logger.info("In Activity_say_no, classification = " + Classification)
    return Play("Activity_say_no", "Activity_check_no" )

    return Say("Ik heb begrepen dat je vanavond niet mee wilt doen, klopt dit?", "Activity_check_no")

@app.route("/Activity_check_no", methods=['GET', 'POST'])
def Activity_check_no():
    return Wait_for_answer_short(0, "Play_Thanks_2")

@app.route("/Play_Thanks_2", methods=['GET', 'POST'])
def Play_Thanks_2():
    return Play("DankUWel", "Activity_check_Classify")
    return Say("Dank u wel!", "Activity_check_Classify")

@app.route("/Activity_say_unclear", methods=['GET', 'POST'])
def Activity_say_unclear():
    global TimesUnclear
    global Classification
    TimesUnclear = TimesUnclear + 1
    if (TimesUnclear >= 2):
        Classification = "Unclear"
        app.logger.info("Too often unclear, sending to /Finalize")
        resp = VoiceResponse()
        resp.redirect(URL+"Finalize")
        TimesUnclear = 0
        return str(resp)
    
    else:
        return Play("Activity_say_unclear", "Activity_check_unclear" )
        return Say("Ik begrijp je niet zo goed, zou je ja of nee kunnen zeggen? Mocht je willen dat ik je later terug bel blijf dan heel even hangen", "Activity_check_unclear")


# @app.route("/Activity_say_unclear_for_check", methods=['GET', 'POST'])
# def Activity_say_unclear_for_check():



@app.route("/Activity_check_unclear", methods=['GET', 'POST'])
def Activity_check_unclear():
    return Wait_for_answer_short(0, "Play_Thanks")

@app.route("/Activity_check_Classify", methods=['GET', 'POST'])
def Activity_check_Classify():
    resp = VoiceResponse()
    global CHECK
    CHECK = True
    global Classification
    global LastMessage
    app.logger.info("In Activity_check_Classify, classification = " + Classification)
    app.logger.info(LastMessage)
    result = Classify_transcription(LastMessage)

    if result == "Ja":
        resp.redirect(URL+"Finalize")

    if result == "Nee":
        app.logger.info("In Nee of Activity_check_Classify, LastMessage = " + LastMessage)

        if (Classification == "Ja"):
            Classification = "Nee"
            resp.redirect(URL+"Activity_say_no")

        elif (Classification == "Nee"):
            Classification = "Ja"
            resp.redirect(URL+"Activity_say_yes")


    else:
        resp.redirect(URL+"Activity_say_unclear")

        
    return str(resp)

@app.route("/Finalize", methods=['GET', 'POST'])
def Finalize():
    global Classification
    global METHOD

    with open("../Attendance/activity1", "a") as fo:
            fo.write(Classification + "\n")


    
    if Classification ==  "Ja":
        if (METHOD == "VOICE" or METHOD == "DAIL"):
            return Wait_for_answer(10,"End","Play", "Finalize_ja")
        if (METHOD == "VOICE_CALLBACK" or METHOD == "DAIL_CALLBACK"):
            return Wait_for_answer(10,"End","Play", "Finalize_ja_callback")
        

        return Wait_for_answer(30,"End","Say", "Ik heb u aangemeld, ik bel u later terug met de details, tot straks!")

    if Classification ==  "Nee":
        if (METHOD == "VOICE" or METHOD == "DAIL"):
            return Wait_for_answer(10,"End","Play", "Finalize_nee")

        return Wait_for_answer(30,"End","Say", "Ik heb u afgemeld, nog een fijne dag gewenst")

    if Classification ==  "Call_Later":
        return Wait_for_answer(10,"End","Play", "Finalize_call_later")

        return Wait_for_answer(30,"End","Say", "Ik bel u later terug, tot straks")

    else :    
        return Wait_for_answer(10,"End","Play", "Finalize_unclear")

        return Wait_for_answer(30,"End","Say", "Ik heb het niet helemaal begrepen, ik bel u straks nogmaals. nog een fijne dag gewenst")    

@app.route("/End", methods=['GET', 'POST'])
def End():
    return str(VoiceResponse())


########################################################## TRANSCRIPTION ########################################################################################
def on_transcription_response(response, ended):
    if not response.results:
        app.logger.info("no results in response of transcription")
        #exit()
        app.logger.info(round((time()-timer)*1000))
        return

    result = response.results[0]
    if not result.alternatives:
        app.logger.info("no result alternative in response")
        app.logger.info(round((time()-timer)*1000))
        return

    transcription = result.alternatives[0].transcript
    app.logger.info("Transcription: " + transcription + " -> Ended variable = " + str(ended))
    if(not ended):
        global LastMessage
        LastMessage = transcription
        global LastTranscription 
        LastTranscription = 1

@sock.route('/stream_google')
def stream_google(ws):
    try:

        app.logger.info("WS connection opened")
        TimeStartFunction = time()
        Lasttime = TimeStartFunction
        bridge = SpeechClientBridge(streaming_config, on_transcription_response)
        t = threading.Thread(target=bridge.start)
        t.start()

        while True:
            global URL
            global TranscriptionDone
            global LastMessage
            global TimeToWait
            global TimeToWait_begin
            global TimeToWait_begin_Default
            
            message = ws.receive()
            if message is None:
                # app.logger.info("3")
                # app.logger.info(round((time()-timer)*1000))
                bridge.add_request(None)
                bridge.terminate()
                break

            data = json.loads(message)
            if data["event"] in ("connected", "start"):
                app.logger.info(f"Media WS: Received event '{data['event']}': {message}")

                if (data["event"] == "start"):
                    #app.logger.info(f"Test1'{data['start']}'")
                    app.logger.info(f"Test2'{data['start']['callSid']}'")
                    callSid = data['start']['callSid']
                continue
            if data["event"] == "media":
                media = data["media"]
                chunk = base64.b64decode(media["payload"])
                bridge.add_request(chunk)
                global LastTranscription
                #app.logger.info(LastTranscription)                                  
                if(LastTranscription ==1):
                    Lasttime = time()
                    #app.logger.info("Retimed last message")

                    LastTranscription = 0
                
                if(((time()-Lasttime) > TimeToWait) and ((time()-TimeStartFunction) > TimeToWait_begin)):
                    app.logger.info("Time is up")
                    app.logger.info("Time since start function = " + str(time()-TimeStartFunction) + " which is > " + str(TimeToWait_begin))
                    app.logger.info("Timetowait_begin this time " + str(TimeToWait_begin))
                    TimeToWait_begin = TimeToWait_begin_Default
                    app.logger.info("Timetowait_begin reset to " + str(TimeToWait_begin))

                    app.logger.info("TimeToWait = " + str(TimeToWait))
                    app.logger.info("TimeToWait_begin_Default = " + str(TimeToWait_begin_Default))

                    app.logger.info("Time since start of function was " + str(time()-TimeStartFunction) + " and it is " + str(time()-Lasttime) + " since last message")


                    # if nothing is said
                    if ((time()-TimeStartFunction) < (time()-Lasttime)):
                        LastMessage = ""
                        app.logger.info("Set Lastmessage to "" since Start of function was at " + str(TimeStartFunction) + "and Time of last message was " + str(Lasttime))

                    with open("Transcribed_call.txt", "a") as fo:
                        fo.write(LastMessage.strip(",.").lower() + "\n")

                    call = client.calls(callSid) \
                .update(url=URL+NextAction)
                    # bridge.terminate()
                    # t.join()
                    # app.logger.info("Stopping... Expecting thread not alive : " +  + t.is_alive())
                    break

                # if (time()-Lasttime ):
                #         app.logger.info("Too Long")                                  
        
            if data["event"] == "stop":
                app.logger.info(f"Media WS: Received event 'stop': {message}")
                app.logger.info("Stopping...")
                break

        app.logger.info("Stopping... Expecting thread alive : " + str(t.is_alive()))
        bridge.terminate()
        t.join()
        app.logger.info("Stopping... Expecting thread not alive : " + str(t.is_alive()))

        TranscriptionDone = 1
        app.logger.info("WS connection closed")
        #return "done"
    
    except Exception as e:
        app.logger.warning(e)    
########################################################## TRANSCRIPTION END ########################################################################################
########################################################## RECORDING START ########################################################################################

@app.route("/Recording_Done", methods=['GET', 'POST'])
def Recording_Done():
    ClearAllVariables()
    response = VoiceResponse()
    app.logger.info("Recorded message done")
    # The recording url will return a wav file by default, or an mp3 if you add .mp3
    recording_url = request.values['RecordingUrl'] + '.mp3'

    filename = request.values['RecordingSid'] + '.mp3'
    with open('{}/{}'.format("../Recordings", filename), 'wb') as f:
        f.write(requests.get(recording_url).content)

    return str(response)

########################################################## RECORDING END ########################################################################################
# 

# @app.route("/", methods=['GET', 'POST'])
# def answer_call():
#     """Respond to incoming phone calls with a brief message."""
#     # Start our TwiML response
#     resp = VoiceResponse()

    
#     #app.logger.info(timer)
#     # Read a message aloud to the caller
#     resp.say("Thank you for calling! Have a great day.", voice='alice')


#     return str(resp)

# @app.route("/SpeechRecognition", methods=['GET', 'POST'])
# def SpeechRecognition():
#     resp = VoiceResponse()
#     start = Start()
#     start.stream(url=f'wss://{request.host}/stream_google')
#     resp.append(start)
#     gather = Gather(input='speech', language='nl-NL', hints='ja, nee, graag, mogelijk, leuk, bridgen, vanavond, doe, ik, mee, niet, fijn, gezellig, samen, wat, hoe, wanneer, bellen, dat, dit, dus, dan', speechTimeout = 5, action='/SpeechRecognition_Result')
#     resp.append(gather)
#     return str(resp)

    #response = VoiceResponse()
    ##Partial Results callback? Speech model? Enhanced?Is this supported? Live streaming link in bookmark?
    #gather = Gather(input='speech', language='nl-NL', speechTimeout = 5, action='/SpeechRecognition_Result')
    #gather.say('we testen de nederlandse taal',language='nl-NL', voice="Polly.Ruben") #Polly.Lotte
    #response.append(gather)
    #app.logger.info(str(response))


# @app.route("/SpeechRecognition_Result", methods=['GET', 'POST'])
# def SpeechRecognition_Result():
#     # Start our TwiML response
#     resp = VoiceResponse()


#     resp.play("/static/Dankjewel.mp3")


#     # If Twilio's request to our app included already gathered digits,
#     # process them
#     if 'SpeechResult' in request.values:
#         Speech = request.values['SpeechResult'].strip(",.").lower()
#         # with open("Transcribed_call.txt", "w") as fo:
#         #     fo.write(Speech)
#         # if 'Confidence' in request.values:
#         #     with open("Transcribed_call_confidence.txt", "w") as fo:
#         #         fo.write(request.values['Confidence'])

#         if "ja" in Speech:
#             resp.play("/static/Aangemeld.mp3")
#             return str(resp)
    
#         elif "nee" in Speech:
#             resp.play("/static/Afgemeld.mp3")
#             return str(resp)
#         else:
#             resp.say('onduidelijk antwoord',language='nl-NL', voice="Polly.Ruben") #Polly.Lotte

#     else:
#         with open("Transcribed_call.txt", "w") as fo:
#             fo.write("No speechresult detected") 
#             resp.say('geen spraak gedetecteerd',language='nl-NL', voice="Polly.Ruben") #Polly.Lotte


#     return str(resp)




# @app.route("/Dail", methods=['GET', 'POST'])
# def voice():
#     """Respond to incoming phone calls with a menu of options"""
#     # Start our TwiML response
#     resp = VoiceResponse()

#     # Start our <Gather> verb
#     gather = Gather(num_digits=1, action='/gather')
#     #gather.say('Druk 1 om mee te doen, druk 2 om niet mee te doen')
#     gather.play("/static/Welkom.mp3")

#     resp.append(gather)

#     # If the user doesn't select an option, redirect them into a loop
#     resp.redirect('/voice')

#     return str(resp)






if __name__ == "__main__":
    app.run(debug=True)
