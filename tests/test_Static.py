import Config.General.General_Config as Config
from GlobalVariables import Voice_Initial, Voice_Callback, Dail_Callback , Dail_Initial

def test_static_contents_Voice_Initial(client):

    FILES = [    
        Voice_Initial.Welcome_Message,
        Voice_Initial.Explanation_Message, 
        Voice_Initial.Check_Yes_Message, 
        Voice_Initial.Check_No_Message, 
        Voice_Initial.Check_Unclear_Message, 
        Voice_Initial.Finalize_Yes_Message, 
        Voice_Initial.Finalize_No_Message, 
        Voice_Initial.Finalize_Unclear_Message] 

    for file in FILES: 
        GETURL = file + ".mp3"
        print("CHECKING FILE : " + GETURL)
        response = client.get(Config.STATIC_URL + "/" + GETURL)
        assert response.status_code == 200
        print("FILE OK")

def test_static_contents_Voice_Callback(client):

    FILES = [ 
        Voice_Callback.Voice_Callback_Aditional_Message,
        Voice_Callback.Voice_Callback_Explaination_Message,
        Voice_Callback.Voice_Callback_Finalize_Yes_Message
        ] 

    for file in FILES: 
        GETURL = file + ".mp3"
        print("CHECKING FILE : " + GETURL)
        response = client.get(Config.STATIC_URL + "/" + GETURL)
        assert response.status_code == 200
        print("FILE OK")

def test_static_contents_Dail_Initial(client):

    FILES = [    
        Dail_Initial.Welcome_Message,
        Dail_Initial.Explanation_Message, 
        Dail_Initial.Check_Yes_Message, 
        Dail_Initial.Check_No_Message, 
        Dail_Initial.Check_Unclear_Message, 
        Dail_Initial.Finalize_Yes_Message, 
        Dail_Initial.Finalize_No_Message, 
        Dail_Initial.Finalize_Unclear_Message] 

    for file in FILES: 
        GETURL = file + ".mp3"
        print("CHECKING FILE : " + GETURL)
        response = client.get(Config.STATIC_URL + "/" + GETURL)
        assert response.status_code == 200
        print("FILE OK")

def test_static_contents_Dail_Callback(client):

    FILES = [ 
        Dail_Callback.Callback_Aditional_Message,
        Dail_Callback.Callback_Explaination_Message,
        Dail_Callback.Callback_Finalize_Yes_Message
        ] 

    for file in FILES: 
        GETURL = file + ".mp3"
        print("CHECKING FILE : " + GETURL)
        response = client.get(Config.STATIC_URL + "/" + GETURL)
        assert response.status_code == 200
        print("FILE OK")