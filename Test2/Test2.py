from flask import Blueprint, send_from_directory, url_for
from Functions import GoogleSpeech 
# from Global_Variables import Variables
from Config.General import General_Config

products_bp_2 = Blueprint('products_bp_2', __name__)

@products_bp_2.route('/test2')
def list():
    return GoogleSpeech.Google()

@products_bp_2.route('/statictest')
def ServeStatic():

    return send_from_directory('Static/General', 'DankUWel.mp3')
    
# @products_bp_2.route('/VariableTest')
# def VariableTest():
#     return str(Variables.TestVariable)
