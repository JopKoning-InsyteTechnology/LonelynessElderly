# LonelynessElderly

Code used for the elderly lonelyness project

## Description


## Getting Started

### Dependencies

* Tested with Python 3.8.10
* Required python packages
* Flask>=0.12
* twilio
* flask-sock 
* simple-websocket 
* pytest
* TODO: Complete this

### Installing

* Install VScode
* Install Ngrok plugin
* Make Ngrok accound and add this to the Ngork yaml file
* Make a Credentials file named Credentials.py in the Webserver folder in the following  format:
* Config = { "TWILIO_ACCOUNT_SID" : "XXXX",
            "TWILIO_AUTH_TOKEN" : "XXXX",
            "TO" : "+XXX",
            "FROM" : "+XXX",
            "BASE_URL" : "XXX/",
            "STARTING_URL_DIAL" : "Dail_Menu",
            "STARTING_URL_DIAL_CALLBACK" : "Dail_Menu_Callback",
            "STARTING_URL_VOICE" : "Voice",
            "STARTING_URL_VOICE_CALLBACK" : "Voice_Callback",
            "RECORDING_URL" : "Recording_Done",
            }
* Generate a key.json from the google speech api and place in the Webserver folder


### Executing program

* Run the tests
```
pytest -v
```
* Run the Flask server
```
flask --app Main --debug run
```
* Start Ngrok
``
CTRL+SHIFT+P ngrok:start -> enter port 5000
``
* Set Ngrok adress in credentials.py
``
copy ngrok URL and paste in Credentials.py

Correctly set:
Account SID
WILIO_ACCOUNT_SID = "XXX"
TWILIO_AUTH_TOKEN = "XXX"
TO = "+316XXX"
FROM = "+316XXX"
``


* Run Voice_Initial_Call.py or similair program

## Help

* Known Problems when starting:
* Sometimes NGRUB has issues, this willl cause the service to fail. You can notice this when the URL is too long
* THIS IS NOT OK   https://50c7-2a02-a420-6b-a40e-95b8-d9e9-33cd-f4ee.ngrok.io/
* THIS IS OK https://2a98-92-70-48-114.ngrok.io/
* Solution not found (maybe restarting)?


## Version History

* 0.1
    * Initial Release
* 0.2
    * Complete code rewriting
    * Intergrated testing
    * Rerecorded voice messages

