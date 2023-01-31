from Main import create_app

import Config.General.General_Config as Config

import Functions.General


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_Wait_for_answer_function(client):
    REDIRECT_URL = "/test" 

    response = Functions.General.Wait_for_answer(REDIRECT_URL)
    print(response)
    ACTION = "Action=\"" + REDIRECT_URL + "\""
    STREAM = "<Stream url=\"" + Config.BASE_URL.replace("https://", "wss://") +"/"+ Config.STREAM_URL + "\" />" 

    print(ACTION)
    print(STREAM)
    assert ACTION in response
    assert STREAM in response

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

