from flask import Blueprint

Dail_Call_Callback = Blueprint('Dail_Call_Callback', __name__,
    static_folder='static')

@Dail_Call_Callback.route('/Start',  methods=['GET', 'POST'])
def list():
    return "Test1"
