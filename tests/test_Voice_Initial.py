import Config.General.General_Config as Config

import Functions.General


# def test_greet_page_Voice_Call_Initial(client):
#     AUDIOFILE = "Greet"
#     REDIRECT_URL = "/Ask_for_activity_speech"

#     GET_URL = '/Voice_Call_Initial/Greet'
#     EXPECTED_URL_RESPONSE = Functions.General.Play(AUDIOFILE, REDIRECT_URL)

#     response = client.get(GET_URL)
#     Complete_URL = "<Redirect>" + Config.BASE_URL + EXPECTED_URL_RESPONSE + "</Redirect>"
#     assert Complete_URL.encode("utf-8") in response.data
