from flask import Blueprint

Voice_Call_Callback = Blueprint('Voice_Call_Callback', __name__,
    static_folder='static')

@Voice_Call_Callback.route('/Start', methods=['GET', 'POST'])
def list():
    return "Test1"

