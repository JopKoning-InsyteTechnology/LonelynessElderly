from flask import Blueprint, send_from_directory
import Config.General.General_Config as Config


Static = Blueprint('Static', __name__, static_folder='')

@Static.route('/<path:folder>/<path:filename>')
def send_file(folder, filename):
        print(Static.static_folder)
        print("Folder : " + folder)
        print("Filename : " + filename)
        return send_from_directory(Static.static_folder + folder, filename)



# @Static.route('/Voice/<path:filename>')
# def send_file1(filename):
#         print(Static.static_folder)
#         print(filename)
#         return send_from_directory(Static.static_folder + "General", filename)

# @Static.route('/<string:path>')
# def Serve_Static_Content(path):
#         print("SERVE_STATIC: " + path + "/" )
#         return 200
#         return send_from_directory(Static.static_folder + path, filename)