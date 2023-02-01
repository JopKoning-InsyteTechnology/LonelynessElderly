from Main import create_app

import Config.General.General_Config as Config

import Functions.General

from time import time

import GlobalVariables

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

# def test_Wait_for_answer_function(client):
#     REDIRECT_URL = "/test" 

#     response = Functions.General.Wait_for_answer(REDIRECT_URL)
#     print(response)
#     ACTION = "Action=\"" + REDIRECT_URL + "\""
#     STREAM = "<Stream url=\"" + Config.BASE_URL.replace("https://", "wss://") +"/"+ Config.STREAM_URL + "\" />" 

#     print(ACTION)
#     print(STREAM)
#     assert ACTION in response
#     assert STREAM in response

def test_Play_function(client):
    AUDIOFILE = "DankUWel"
    REDIRECT_URL = "/test" 

    response = Functions.General.Play(AUDIOFILE, REDIRECT_URL)
    print(response)
    REDIRECT = "<Redirect>" + Config.BASE_URL + REDIRECT_URL + "</Redirect>" 
    PLAY = "<Play>" + Config.BASE_URL + "/" + Config.STATIC_URL + "/" + AUDIOFILE + ".mp3" +"</Play>"

    print(REDIRECT)
    print(PLAY)

    assert REDIRECT in response
    assert PLAY in response


def test_Listen_function(client):
    ############################################ Test if listen function waits if websocket connection is still alive ######################3
    GlobalVariables.IsActive = True
    GlobalVariables.StreamStarted = False

    GlobalVariables.LastMessage = ""
    GlobalVariables.TimeFunctionStarted = 0
    GlobalVariables.TimeLastMessage = 0

    result = Functions.General.Listen(2,2,"/Current", "/Redirect")
    assert "/Current" in result


    ##################################### Test if stream is starting is working ##########################################
    GlobalVariables.IsActive = False
    GlobalVariables.StreamStarted = False

    GlobalVariables.LastMessage = ""
    GlobalVariables.TimeFunctionStarted = 0
    GlobalVariables.TimeLastMessage = 0

    STREAM = Config.BASE_URL.replace("https://", "wss://") +"/"+ Config.STREAM_URL + "\" />" 

    result = Functions.General.Listen(2,2,"/Current", "/Redirect")
    assert "<Stream" in result

    assert STREAM in result

    GlobalVariables.IsActive = False
    GlobalVariables.StreamStarted = True

    GlobalVariables.LastMessage = ""
    GlobalVariables.TimeFunctionStarted = 0
    GlobalVariables.TimeLastMessage = 0

    result = Functions.General.Listen(2,2,"/Current", "/Redirect")
    assert STREAM not in result
    assert "/Current" in result

    ######################################## Test if it returns current when timestart < given time##########################################
    GlobalVariables.IsActive = True
    GlobalVariables.StreamStarted = True

    GlobalVariables.LastMessage = ""
    GlobalVariables.TimeFunctionStarted = time()
    GlobalVariables.TimeLastMessage = time()

    result = Functions.General.Listen(2,2,"/Current", "/Redirect")
    assert "/Current" in result

    GlobalVariables.IsActive = True
    GlobalVariables.StreamStarted = True

    GlobalVariables.LastMessage = ""
    GlobalVariables.TimeFunctionStarted = time()- 5
    GlobalVariables.TimeLastMessage = time() - 5

    result = Functions.General.Listen(2,2,"/Current", "/Redirect")
    assert "/Current" not in result
    assert "<Stop><Stream name=" in result

def test_Classify_Function(client):
    assert Functions.General.Classify("Ja") == "Yes"
    assert Functions.General.Classify("Nee") == "No"
    assert Functions.General.Classify("BlaBlaBla Ja ldksjajlfdkahjkl") == "Yes"
    assert Functions.General.Classify("BlaBlaBla ja ldksjajlfdkahjkl") == "Yes"
    assert Functions.General.Classify("jlkfds;fsldk Nee ljksfddsfjlk") == "No"
    assert Functions.General.Classify("jlkfds;fsldk nee ljksfddsfjlk") == "No"
    assert Functions.General.Classify("sfdfdssdf") == "Unclear"
