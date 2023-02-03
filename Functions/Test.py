
import GlobalVariables
from time import time
import Config.General.General_Config as Config


def Check_Redirect(baseURL, URL):
    return ("<Redirect>" + Config.BASE_URL + baseURL + URL + "</Redirect>").encode("utf-8")

def Set_Listen_Redirect():
    GlobalVariables.IsActive = True
    GlobalVariables.StreamStarted = True

    GlobalVariables.LastMessage = ""
    GlobalVariables.TimeFunctionStarted = time()- 100
    GlobalVariables.TimeLastMessage = time() - 100
    return