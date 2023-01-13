import Credentials as CRD

import requests


from argparse import Action
from ast import Global
from flask import Flask, request, send_from_directory, url_for

from flask_sock import Sock
import json, base64, audioop

import os, threading
from google.cloud.speech import RecognitionConfig, StreamingRecognitionConfig
from SpeechClientBridge import SpeechClientBridge

from twilio.twiml.voice_response import VoiceResponse,  Gather, Start, Stream
from time import time ,sleep

from twilio.rest import Client


app = Flask(__name__)
sock = Sock(app)



@app.route("/", methods=['GET', 'POST'])
def Voice():
        return "welcome"

if __name__ == "__main__":
    app.run(debug=True)
