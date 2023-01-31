import Config.General.General_Config as Config

def test_static_contents(client):

    FILES = ["DankUWel", "test"]

    for file in FILES:
        GETURL = "/"  + Config.STATIC_URL + "/General/" + file + ".mp3"
        response = client.get(GETURL)
        assert response.status_code == 200

    # FILE = "DankUWel"
    # GETURL = "/"  + Config.STATIC_URL + "/General/" + FILE + ".mp3"
    # response = client.get(GETURL)
    # print(GETURL)
    # assert response.status_code == 200
