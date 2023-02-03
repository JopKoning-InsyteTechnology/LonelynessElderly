import Config.General.General_Config as Config
import GlobalVariables
import Functions.General
from time import time
from Functions.Test import Check_Redirect, Set_Listen_Redirect

baseURL = "/Voice_Call_Callback/"

def test_Start(client):
    response = client.post(baseURL + "Start")
    assert response.status_code == 200

def test_Voice(client):
    response = client.post(baseURL + "Voice")
    assert response.status_code == 200
    assert Check_Redirect(baseURL,"Listen_For_Hello") in response.data

def test_Listen_For_Hello(client):
    Set_Listen_Redirect()
    response = client.post(baseURL + "Listen_For_Hello")
    assert response.status_code == 200
    assert Check_Redirect(baseURL,"Play_Greeting_Message") in response.data

def test_Play_Greeting_Message(client):
    response = client.post(baseURL + "Play_Greeting_Message")
    assert response.status_code == 200
    assert b"<Play>" in response.data                                                                                  
    GlobalVariables.LastMessage = "Ja"
    response = client.post(baseURL + "Classify_Answer")
    assert Check_Redirect(baseURL,"Finalize") in response.data

    GlobalVariables.LastMessage = "Nee"
    response = client.post(baseURL + "Classify_Answer")
    assert Check_Redirect(baseURL,"Play_Additional_Message") in response.data

    GlobalVariables.LastMessage = "sfdfdsfsd"
    response = client.post(baseURL + "Classify_Answer")
    assert Check_Redirect(baseURL,"Play_Additional_Message") in response.data

def test_Play_Additional_Message(client):
    response = client.post(baseURL + "Play_Additional_Message")
    assert response.status_code == 200
    assert b"<Play>"  in response.data
    assert Check_Redirect(baseURL,"Finalize") in response.data    

def test_Finalize(client):
    response = client.post(baseURL + "Finalize")
    assert response.status_code == 200
    assert b"<Play>"  in response.data

