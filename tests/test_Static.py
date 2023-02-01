import Config.General.General_Config as Config
from GlobalVariables import Voice_Initial

def test_static_contents(client):

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
        response = client.get(GETURL)
        assert response.status_code == 200
        print("FILE OK")

    # FILE = "DankUWel"
    # GETURL = "/"  + Config.STATIC_URL + "/General/" + FILE + ".mp3"
    # response = client.get(GETURL)
    # print(GETURL)
    # assert response.status_code == 200

