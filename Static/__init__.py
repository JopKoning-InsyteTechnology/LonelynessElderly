from flask import Blueprint, send_from_directory
import Config.General.General_Config as Config


Static = Blueprint('Static', __name__, static_folder='')

@Static.route('/General/<path:filename>')
def send_file(filename):
        print(Static.static_folder)
        print(filename)
        return send_from_directory(Static.static_folder + "General", filename)

