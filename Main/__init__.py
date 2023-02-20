import os

from flask import Flask, request, render_template, redirect
import Config.General.General_Config as Config
from flask_sock import Sock
import requests
import time

from Webserver.Voice.Voice_Call_Initial import  Voice_Call_Initial
from Webserver.Voice.Voice_Call_Callback import  Voice_Call_Callback
from Webserver.Dail.Dail_Call_Initial import Dail_Call_Initial
from Webserver.Dail.Dail_Call_Callback import  Dail_Call_Callback

from Webserver.Entry_Points.Entry_Points import Entry_Points 

from Webserver.SpeechAPI.SpeechAPI import stream_google
from Webserver.SpeechAPI.SpeechAPI_test import SpeechAPI_test

import GlobalVariables

from Functions.General import Logger, Print_Log

from Static import Static

# Twilio Imports
from twilio.twiml.voice_response import VoiceResponse



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, static_folder='Static', template_folder='templates')
    sock = Sock(app)

    ################################################## Load configurations for testing ##########################################################
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    ################################################## End load configurations for testing ##########################################################
    ################################################## Load blueprints ##########################################################

    app.register_blueprint(Voice_Call_Initial, url_prefix='/Voice_Call_Initial')
    app.register_blueprint(Voice_Call_Callback, url_prefix='/Voice_Call_Callback')
    app.register_blueprint(Dail_Call_Initial, url_prefix='/Dail_Call_Initial')
    app.register_blueprint(Dail_Call_Callback, url_prefix='/Dail_Call_Callback')
    app.register_blueprint(Entry_Points, url_prefix='/Entry_Points')
    app.register_blueprint(SpeechAPI_test, url_prefix='/SpeechAPI_test')

    app.register_blueprint(Static, url_prefix='/Static')

    #TODO: Check google speech
    @sock.route('/SpeechAPI/stream_google')
    def Speech(ws):
        stream_google(ws)
        Print_Log("__INIT__.PY MAIN: We are done with the socket, no remaining connections")
        return 200
        
    GlobalVariables.FILE = time.strftime("%Y-%m-%d->%H:%M:%S") + ".txt"
    Logger("MAIN", "Starting", "INFO")
    

    @app.route('/', methods=['GET', 'POST'])
    def index():
        ## Display the HTML form template 
        return render_template('index.html')
    
    @app.route('/Call', methods=['GET', 'POST'])
    def Call():
        ## Display the HTML form template 
        if request.method == 'POST':

                value = request.form['Mobile_Number'] + " " + request.form['Name'] + " " + request.form['submit_button']
                redirect_url = Config.BASE_URL + "/Entry_Points/" + request.form['submit_button'] + "/" + request.form['Name'].replace(" ", "_") + "/" + request.form['Mobile_Number']
                return redirect(redirect_url)
                #return redirect("/Entry_Points/V/Jop/+31638475605")
                
        #         return redirect(url_for('success', name=user))
        # return render_template('index.html')

  ########################################################## RECORDING END ########################################################################################

    @app.route("/Recording_Done", methods=['GET', 'POST'])
    def Recording_Done():
        response = VoiceResponse()
        # The recording url will return a wav file by default, or an mp3 if you add .mp3
        recording_url = request.values['RecordingUrl'] + '.mp3'
        filename = request.values['RecordingSid'] + '.mp3'

        with open('{}/{}'.format("Recordings", GlobalVariables.FILE.replace(".txt", ".mp3")), 'wb') as f:
            f.write(requests.get(recording_url).content)

        with open("Attendance/" + time.strftime("%Y-%m-%d") + ".txt", "a") as fo:
                fo.write("Recording received, end of call" + "\n\n\n")

        return str(response)

########################################################## RECORDING END ########################################################################################

     #GlobalVariables.Voice_Messages.get("")
    ################################################## End Load blueprints ##########################################################


    # @app.route('/static/<path:filename>')
    # def send_file(filename):
    #         Print_Log(app.static_folder)
    #         Print_Log(filename)
    #         return send_from_directory("/home/jop/Desktop/Afstuderen/LonelynessElderly/Static/", filename)

    return app

    