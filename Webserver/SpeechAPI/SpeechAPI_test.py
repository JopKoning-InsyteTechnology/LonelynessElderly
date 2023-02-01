from flask import Blueprint
import Functions.General
import time
#from Global_Variables.Speech_Recognition import LastMessage, TimeLastMessage
import GlobalVariables

SpeechAPI_test = Blueprint('SpeechAPI_test', __name__)
Host = "GOOGLE_SPEECH_API_TEST"

@SpeechAPI_test.route('/Start', methods=['GET', 'POST'])
def speechAPI():
    return Functions.General.Listen(3,2,"/SpeechAPI_test/Start", "/SpeechAPI_test/Test2")

@SpeechAPI_test.route('/Test2', methods=['GET', 'POST'])
def Test2():
    return Functions.General.Play("General/DankUWel", "/SpeechAPI_test/Test3")
    Functions.General.Listen(3,2,"/SpeechAPI_test/Test2", "/SpeechAPI_test/Test3")

@SpeechAPI_test.route('/Test3', methods=['GET', 'POST'])
def Test3():
    return Functions.General.Listen(3,2,"/SpeechAPI_test/Test3", "/SpeechAPI_test/End")


# @SpeechAPI_test.route('/TimeSinceInput', methods=['GET', 'POST'])
# def TimeSinceInput():
# #     print("LAST_MESSAGE VARIABLE : " + str(GlobalVariables.LastMessage
# # ) + " | TIME_LAST_MESSAGE_VARIABLE : " + str(GlobalVariables.TimeLastMessage) + " | CURRENT_TIME : " + str(time.time()))
# #     print("TIME_SINCE_LAST_MESSAGE : " + str(time.time() - GlobalVariables.TimeLastMessage))
#     return Functions.General.Listen(3,2,"/SpeechAPI_test/TimeSinceInput", "/SpeechAPI_test/End")
#     return Functions.General.Redirect("/SpeechAPI_test/TimeSinceInput")

# @SpeechAPI_test.route('/Wait5SecForInput', methods=['GET', 'POST'])
# def speechAPIWait():
#     time.sleep(5)
#     return Functions.General.Redirect("/SpeechAPI_test/Stop_Stream")

# @SpeechAPI_test.route('/Stop_Stream', methods=['GET', 'POST'])
# def Stop_Stream():
#     return  Functions.General.Stop_Stream("/SpeechAPI_test/EndWait")

# @SpeechAPI_test.route('/EndWait', methods=['GET', 'POST'])
# def EndWait():
#     time.sleep(10)
#     return  Functions.General.Stop_Stream("/SpeechAPI_test/EndWait")

@SpeechAPI_test.route('/End', methods=['GET', 'POST'])
def End():
    time.sleep(5)
    return  Functions.General.Stop_Stream("/SpeechAPI_test/End")