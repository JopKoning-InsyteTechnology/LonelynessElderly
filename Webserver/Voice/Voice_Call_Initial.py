# Flask Imports
from flask import Blueprint, request

# Twilio Imports
from twilio.twiml.voice_response import VoiceResponse

# Configuration Imports
import Config.General.General_Config as Config

# Import Functions
import Functions.General



Voice_Call_Initial = Blueprint('Voice_Call_Initial', __name__,
    static_folder='static')

## Get the complete URL to this blueprint file
#Task_URL = Config.BASE_URL+request.url_rule.rule


@Voice_Call_Initial.route('/Start', methods=['GET', 'POST'])
def list():
    return "Test1"


@Voice_Call_Initial.route("/Voice", methods=['GET', 'POST'])
def Voice():
        Task_URL = Config.BASE_URL+request.url_rule.rule
        #TODO check if we can do this by call ID or in main
        # with open("Transcribed_call.txt", "a") as fo:
        #                 fo.write("Starting Call to voice\n")
                        
        resp = VoiceResponse()
        # Voice_Call_Initial.logger.info("Base URL of this blueprint = " + str(Task_URL))
        # #TODO check if this is nessesary
        # # global TimeToWait_begin
        # # global TimeToWait_begin_Initial
        # # Voice_Call_Initial.logger.info("Setting TimeToWait_begin before setting = " + str(TimeToWait_begin))
        # # TimeToWait_begin = TimeToWait_begin_Initial
        # # Voice_Call_Initial.logger.info("Setting TimeToWait_begin after setting = " + str(TimeToWait_begin))
        # # global METHOD
        # # METHOD = "VOICE"
        
        resp.redirect(Task_URL+"/Wait_for_greeting")

        return str(resp)

@Voice_Call_Initial.route("/Wait_for_greeting", methods=['GET', 'POST'])
def Wait_for_greeting():
    """Wait for a person to respond"""
    return Functions.General.Wait_for_answer("Greet")

@Voice_Call_Initial.route("/Greet", methods=['GET', 'POST'])
def Greet():
    return Functions.General.Play("Greet", "Ask_for_activity_speech")
    return Say("Hallo, u spreekt met jop koning van de activiteitenorganisatie", "Ask_for_activity_speech" )

@Voice_Call_Initial.route("/Ask_for_activity_speech", methods=['GET', 'POST'])
def Ask_for_activity_speech():
    return Functions.General.Play("Ask_for_activity_speech_voice", "Wait_for_activity_reaction" )
    return Say("We gaan vanavond bridgen, heeft u zin om mee te doen?", "Wait_for_activity_reaction" )
    
@Voice_Call_Initial.route("/Wait_for_activity_reaction", methods=['GET', 'POST'])
def Wait_for_activity_reaction():
    return Functions.General.Wait_for_answer("Play_Thanks")

@Voice_Call_Initial.route("/Play_Thanks", methods=['GET', 'POST'])
def Play_Thanks():
    return Functions.General.Play("DankUWel", "Classify_activity_reaction")
    return Say("Dank u wel!", "Classify_activity_reaction")

@Voice_Call_Initial.route("/Classify_activity_reaction", methods=['GET', 'POST'])
def Clasify_activity_reaction():
    resp = VoiceResponse()

    # global LastMessage
    # app.logger.info("Classify LastMessage = " + LastMessage)
    # global CHECK
    # app.logger.info("CHECK = " + str(CHECK))

    # global Classification
    # match (Classify_transcription(LastMessage)):
    #     case "Ja":
    #         app.logger.info("Classification = Ja")
    #         Classification = "Ja"
    #         app.logger.info("Classification = Ja")

    #         if (METHOD == "VOICE"):
    #             if (CHECK == True):
    #                 resp.redirect(URL+"Finalize")
    #             resp.redirect(URL+"Activity_say_yes")
    #         if (METHOD == "VOICE_CALLBACK"):  
    #             resp.redirect(URL+"Finalize")
    #         resp.redirect(URL+"Activity_say_yes")

    #     case "Nee":
    #         app.logger.info("Classification = Nee")
    #         Classification = "Nee"

    #         if (METHOD == "VOICE"):
    #             if (CHECK == True):
    #                 resp.redirect(URL+"Finalize")
    #             resp.redirect(URL+"Activity_say_no")
    #         if (METHOD == "VOICE_CALLBACK"):  
    #             resp.redirect(URL+"Callback_Additional_Message")
    #         resp.redirect(URL+"Activity_say_no")

    #     case "Unclear":
    #         resp.redirect(URL+"Activity_say_unclear")

    #     case "None":
    #         resp.redirect(URL+"Activity_say_unclear")

    #     case _:    
    #         resp.redirect(URL+"Activity_say_unclear")
    return str(resp)

@Voice_Call_Initial.route("/Test_Google_Speech", methods=['GET', 'POST'])
def Google_Speech():
    return Functions.General.Wait_for_answer("Play_Thanks")