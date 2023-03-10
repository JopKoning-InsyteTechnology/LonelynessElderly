# Configuration Imports
import Config.General.General_Config as Config


from flask import url_for, request

def test_landing_page_Voice_Call_Initial(client):
    response = client.post('/Voice_Call_Initial/Start')
    assert response.data == b'Test1'

def test_landing_page_Voice_Call_Callback(client):
    response = client.post('/Voice_Call_Callback/Start')
    assert response.data == b'Test1'

def test_landing_page_Dail_Call_Initial(client):
    response = client.post('/Dail_Call_Initial/Start')
    assert response.data == b'Test1'
    

def test_landing_page_Dail_Call_Callback(client):
    response = client.post('/Dail_Call_Callback/Start')
    assert response.data == b'Test1'

def test_landing_page_Dail_Call_Callback(client):
    response = client.post('/Dail_Call_Callback/Start')
    assert response.data == b'Test1'
        
def test_landing_page_test_Speech_API(client):
    response = client.post('/SpeechAPI_test/Start')
    assert response.status_code == 200

def test_landing_config(client):
    assert client.post("/" + Config.STARTING_URL_DIAL).status_code == 200
    assert client.post("/" + Config.STARTING_URL_DIAL_CALLBACK).status_code == 200
    assert client.post("/" + Config.STARTING_URL_VOICE).status_code == 200
    assert client.post("/" + Config.STARTING_URL_VOICE_CALLBACK).status_code == 200

# def test_entry_point_initial_call(client):
#     response = client.post('/Entry_Points/V/Jop/0683949299')
#     assert response.status_code == 200
#     assert 0




# def test_landing_page_recording_done(client):
#     response = client.post("/Recording_Done")
#     print("/"+ Config.RECORDING_URL)
#     assert response.status_code == 200

# def test_landing_page_Voice_Call_Initial_Test(client):

#     GET_URL = '/Voice_Call_Initial/Voice'
#     EXPECTED_URL_RESPONSE = '/Voice_Call_Initial/Voice/Wait_for_greeting'

#     response = client.post(GET_URL)
#     Complete_URL = "<Redirect>" + Config.BASE_URL + EXPECTED_URL_RESPONSE + "</Redirect>"
#     assert Complete_URL.encode("utf-8") in response.data

