import Config.General.General_Config as Config
import GlobalVariables
import Functions.General
import time
from Functions.Test import Check_Redirect, Set_Listen_Redirect

baseURL = "/Voice_Call_Initial/"


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
    assert Check_Redirect(baseURL,"Play_Explain_Message") in response.data

def test_Play_Explain_Message(client):
    response = client.post(baseURL + "Play_Explain_Message")
    assert response.status_code == 200
    assert b"<Play>"  in response.data
    assert Check_Redirect(baseURL,"Listen_For_Answer") in response.data    

def test_Listen_For_Answer(client):
    Set_Listen_Redirect()
    response = client.post(baseURL + "Listen_For_Answer")
    assert response.status_code == 200
    assert Check_Redirect(baseURL,"Classify_Answer") in response.data

def test_Classify_Answer(client):
    response = client.post(baseURL + "Classify_Answer")
    assert response.status_code == 200

    GlobalVariables.LastMessage = "Ja"
    response = client.post(baseURL + "Classify_Answer")
    assert Check_Redirect(baseURL,"Play_Check_Answer_Message/Yes") in response.data

    GlobalVariables.LastMessage = "Nee"
    response = client.post(baseURL + "Classify_Answer")
    assert Check_Redirect(baseURL,"Play_Check_Answer_Message/No") in response.data

    GlobalVariables.LastMessage = "sfdfdsfsd"
    response = client.post(baseURL + "Classify_Answer")
    assert Check_Redirect(baseURL,"Play_Check_Answer_Message/Unclear") in response.data

    response = client.post(baseURL + "Classify_Answer")
    assert Check_Redirect(baseURL,"Play_Check_Answer_Message/Unclear") in response.data

    response = client.post(baseURL + "Classify_Answer")
    assert Check_Redirect(baseURL,"Finalize/Unclear") in response.data


def test_Play_Check_Answer_Message(client):
    response = client.post(baseURL + "Play_Check_Answer_Message/Yes")
    assert response.status_code == 200
    assert b"<Play>"  in response.data
    assert Check_Redirect(baseURL,"Listen_For_Check_Answer_Result/Yes") in response.data

    response = client.post(baseURL + "Play_Check_Answer_Message/No")
    assert response.status_code == 200
    assert b"<Play>"  in response.data
    assert Check_Redirect(baseURL,"Listen_For_Check_Answer_Result/No") in response.data

    response = client.post(baseURL + "Play_Check_Answer_Message/Unclear")
    assert response.status_code == 200
    assert b"<Play>"  in response.data
    assert Check_Redirect(baseURL,"Listen_For_Answer") in response.data

def test_Listen_For_Check_Answer_Result(client):
    Set_Listen_Redirect()
    response = client.post(baseURL + "Listen_For_Check_Answer_Result/Yes")
    assert response.status_code == 200
    assert Check_Redirect(baseURL,"Classify_Answer_2/Yes") in response.data

    Set_Listen_Redirect()
    response = client.post(baseURL + "Listen_For_Check_Answer_Result/No")
    assert response.status_code == 200
    assert Check_Redirect(baseURL,"Classify_Answer_2/No") in response.data

def test_Classify_Answer_2(client):
    GlobalVariables.LastMessage = "Ja"
    response = client.post(baseURL + "Classify_Answer_2/Yes")
    assert response.status_code == 200
    assert Check_Redirect(baseURL,"Finalize/Yes") in response.data

    GlobalVariables.LastMessage = "Ja"
    response = client.post(baseURL + "Classify_Answer_2/No")
    assert response.status_code == 200
    assert Check_Redirect(baseURL,"Finalize/No") in response.data

    GlobalVariables.LastMessage = "Nee"
    response = client.post(baseURL + "Classify_Answer_2/Yes")
    assert response.status_code == 200
    assert Check_Redirect(baseURL,"Play_Check_Answer_Message/No") in response.data

    GlobalVariables.LastMessage = "Nee"
    response = client.post(baseURL + "Classify_Answer_2/No")
    assert response.status_code == 200
    assert Check_Redirect(baseURL,"Play_Check_Answer_Message/Yes") in response.data

    #TODO: Test with errors

    # GlobalVariables.LastMessage = "sdfsdf"
    # response = client.post(baseURL + "Finalize/Unclear")
    # assert response.status_code == 200
    # assert Check_Redirect(baseURL,"Finalize/Unclear") in response.data

def test_Finalize(client):
    with open("Attendance/" + time.strftime("%Y-%m-%d") + ".txt", "a") as fo:
        fo.write("-------------------------- TEST START -------------------------- " + "\n")    

    response = client.post(baseURL + "Finalize/Yes")
    assert response.status_code == 200
    assert b"<Play>"  in response.data

    response = client.post(baseURL + "Finalize/No")
    assert response.status_code == 200
    assert b"<Play>"  in response.data

    response = client.post(baseURL + "Finalize/Unclear")
    assert response.status_code == 200
    assert b"<Play>"  in response.data
    with open("Attendance/" + time.strftime("%Y-%m-%d") + ".txt", "a") as fo:
        fo.write("-------------------------- TEST END -------------------------- " + "\n")