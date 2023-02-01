import Config.General.General_Config as Config
import GlobalVariables
import Functions.General
from time import time

baseURL = "/Voice_Call_Initial/"

def Check_Redirect(URL):
    return ("<Redirect>" + Config.BASE_URL + baseURL + URL + "</Redirect>").encode("utf-8")

def Set_Listen_Redirect():
    GlobalVariables.IsActive = True
    GlobalVariables.StreamStarted = True

    GlobalVariables.LastMessage = ""
    GlobalVariables.TimeFunctionStarted = time()- 100
    GlobalVariables.TimeLastMessage = time() - 100
    return

def test_Voice(client):
    response = client.post(baseURL + "Voice")
    assert response.status_code == 200
    assert Check_Redirect("Listen_For_Hello") in response.data

def test_Listen_For_Hello(client):
    Set_Listen_Redirect()
    response = client.post(baseURL + "Listen_For_Hello")
    assert response.status_code == 200
    assert Check_Redirect("Play_Greeting_Message") in response.data

def test_Play_Greeting_Message(client):
    response = client.post(baseURL + "Play_Greeting_Message")
    assert response.status_code == 200
    assert b"<Play>" in response.data
    assert Check_Redirect("Play_Explain_Message") in response.data

def test_Play_Explain_Message(client):
    response = client.post(baseURL + "Play_Explain_Message")
    assert response.status_code == 200
    assert b"<Play>"  in response.data
    assert Check_Redirect("Listen_For_Answer") in response.data    

def test_Listen_For_Answer(client):
    Set_Listen_Redirect()
    response = client.post(baseURL + "Listen_For_Answer")
    assert response.status_code == 200
    assert Check_Redirect("Classify_Answer") in response.data

def test_Classify_Answer(client):
    response = client.post(baseURL + "Classify_Answer")
    assert response.status_code == 200

    GlobalVariables.LastMessage = "Ja"
    response = client.post(baseURL + "Classify_Answer")
    assert Check_Redirect("Play_Check_Answer_Message/Yes") in response.data

    GlobalVariables.LastMessage = "Nee"
    response = client.post(baseURL + "Classify_Answer")
    assert Check_Redirect("Play_Check_Answer_Message/No") in response.data

    GlobalVariables.LastMessage = "sfdfdsfsd"
    response = client.post(baseURL + "Classify_Answer")
    assert Check_Redirect("Play_Check_Answer_Message/Unclear") in response.data

    response = client.post(baseURL + "Classify_Answer")
    assert Check_Redirect("Play_Check_Answer_Message/Unclear") in response.data

    response = client.post(baseURL + "Classify_Answer")
    assert Check_Redirect("Finalize/Unclear") in response.data


def test_Play_Check_Answer_Message(client):
    response = client.post(baseURL + "Play_Check_Answer_Message/Yes")
    assert response.status_code == 200
    assert b"<Play>"  in response.data
    assert Check_Redirect("Listen_For_Check_Answer_Result/Yes") in response.data

    response = client.post(baseURL + "Play_Check_Answer_Message/No")
    assert response.status_code == 200
    assert b"<Play>"  in response.data
    assert Check_Redirect("Listen_For_Check_Answer_Result/No") in response.data

    response = client.post(baseURL + "Play_Check_Answer_Message/Unclear")
    assert response.status_code == 200
    assert b"<Play>"  in response.data
    assert Check_Redirect("Listen_For_Answer") in response.data

def test_Listen_For_Check_Answer_Result(client):
    Set_Listen_Redirect()
    response = client.post(baseURL + "Listen_For_Check_Answer_Result/Yes")
    assert response.status_code == 200
    assert Check_Redirect("Classify_Answer_2/Yes") in response.data

    Set_Listen_Redirect()
    response = client.post(baseURL + "Listen_For_Check_Answer_Result/No")
    assert response.status_code == 200
    assert Check_Redirect("Classify_Answer_2/No") in response.data

def test_Classify_Answer_2(client):
    GlobalVariables.LastMessage = "Ja"
    response = client.post(baseURL + "Classify_Answer_2/Yes")
    assert response.status_code == 200
    assert Check_Redirect("Finalize/Yes") in response.data

    GlobalVariables.LastMessage = "Ja"
    response = client.post(baseURL + "Classify_Answer_2/No")
    assert response.status_code == 200
    assert Check_Redirect("Finalize/No") in response.data

    GlobalVariables.LastMessage = "Nee"
    response = client.post(baseURL + "Classify_Answer_2/Yes")
    assert response.status_code == 200
    assert Check_Redirect("Play_Check_Answer_Message/No") in response.data

    GlobalVariables.LastMessage = "Nee"
    response = client.post(baseURL + "Classify_Answer_2/No")
    assert response.status_code == 200
    assert Check_Redirect("Play_Check_Answer_Message/Yes") in response.data

    #TODO: Test with errors

    # GlobalVariables.LastMessage = "sdfsdf"
    # response = client.post(baseURL + "Finalize/Unclear")
    # assert response.status_code == 200
    # assert Check_Redirect("Finalize/Unclear") in response.data

def test_Finalize(client):
    response = client.post(baseURL + "Finalize/Yes")
    assert response.status_code == 200
    assert b"<Play>"  in response.data

    response = client.post(baseURL + "Finalize/No")
    assert response.status_code == 200
    assert b"<Play>"  in response.data

    response = client.post(baseURL + "Finalize/Unclear")
    assert response.status_code == 200
    assert b"<Play>"  in response.data


# def test_Voice(client):
#     response = client.post('/SpeechAPI_test/Start')
#     assert response.status_code == 200

