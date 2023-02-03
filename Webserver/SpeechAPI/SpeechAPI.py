from flask import Blueprint
import threading, json, base64
from Functions.SpeechClientBridge import SpeechClientBridge
# from Global_Variables import Speech_Recognition 
import GlobalVariables

from Functions.General import Logger_Classification
from google.cloud.speech import RecognitionConfig, StreamingRecognitionConfig
from time import time
from twilio.rest import Client
import Config.General.General_Config as Config
import os

config = RecognitionConfig(
    encoding=RecognitionConfig.AudioEncoding.MULAW,
    sample_rate_hertz=8000,
    language_code="nl-NL",
)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/jop/Desktop/Afstuderen/LonelynessElderly/Webserver/SpeechAPI/key.json"

SpeechAPI = Blueprint('SpeechAPI', __name__)
streaming_config = StreamingRecognitionConfig(config=config, interim_results=True)

client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)


def on_transcription_response(response, ended):
    if not response.results:
        print ("ON_TRANSCRIPTION_RESPONSE: No results for the input")
        Logger_Classification("ON-TRANSCRIPTION-RESPONSE", str(GlobalVariables.TimeLastMessage) + " : NOTHING RECOGNIZED", "INFO")

        return

    result = response.results[0]
    if not result.alternatives:
        print ("ON_TRANSCRIPTION_RESPONSE: No alternatives for the input")

        return

    transcription = result.alternatives[0].transcript
    GlobalVariables.LastMessage = transcription
    GlobalVariables.TimeLastMessage = time()
    Logger_Classification("ON-TRANSCRIPTION-RESPONSE", str(GlobalVariables.TimeLastMessage) + " : " + str(GlobalVariables.LastMessage), "INFO")
    print("ON-TRANSCRIPTION-RESPONSE: " + str(GlobalVariables.TimeLastMessage) + " : " + str(GlobalVariables.LastMessage) )

def stream_google(ws):
    print("STARTING WEBSOCKET")
    GlobalVariables.IsActive = True
    GlobalVariables.LastMessage = ""
    GlobalVariables.TimeLastMessage = time()
    GlobalVariables.TimeFunctionStarted = time()


    try:
        # TimeStartFunction = time()
        # Lasttime = TimeStartFunction
        bridge = SpeechClientBridge(streaming_config, on_transcription_response)
        t = threading.Thread(target=bridge.start)
        t.start()
        
        while True:            
            message = ws.receive()
            if message is None:
                print("\nSTREAM-GOOGLE-WEBSOCKET: message is none, Terminating thread. Current thread status :" + str(t.isAlive()))
                bridge.add_request(None)
                bridge.terminate()
                print("STREAM-GOOGLE-WEBSOCKET: thread terminated, status is:" + str(t.isAlive()))
                break

            data = json.loads(message)
            # print("\nSTREAM-GOOGLE-WEBSOCKET: data in message : " + str(data))
            # print("STREAM-GOOGLE-WEBSOCKET: event in message : " + str(data["event"]))

            if data["event"] in ("connected", "start"):

                if (data["event"] == "start"):
                    callSid = data['start']['callSid']
                continue
            if data["event"] == "media":
                media = data["media"]
                chunk = base64.b64decode(media["payload"])
                bridge.add_request(chunk)
                # break                                
        
            if data["event"] == "stop":
                print("\nSTREAM-GOOGLE-WEBSOCKET: message is stop")
                break

        print("STREAM-GOOGLE-WEBSOCKET: Break occured, Terminating thread. Current thread status :" + str(t.isAlive()))

        bridge.terminate()
        print("STREAM-GOOGLE-WEBSOCKET: Joining Thread")

        #t.join()
        print("STREAM-GOOGLE-WEBSOCKET: thread terminated and joined, status is:" + str(t.isAlive()))
        GlobalVariables.IsActive = False
        

    
    except Exception as e:
        print("STREAM-GOOGLE-WEBSOCKET: exception occured : " + str(e))
        print("STREAM-GOOGLE-WEBSOCKET: Terminating Thread")
        bridge.terminate()
        print("STREAM-GOOGLE-WEBSOCKET: Joining Thread")
        #t.join()
        print("STREAM-GOOGLE-WEBSOCKET: Thread Joined")
        # GlobalVariables.LastMessage = ""
        # GlobalVariables.TimeLastMessage = 0
        # GlobalVariables.TimeFunctionStarted = 0
        GlobalVariables.IsActive = False
        print("STREAM-GOOGLE-WEBSOCKET: Cleared Global Variables")

        
        




