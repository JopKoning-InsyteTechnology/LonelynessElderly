from flask import Blueprint

Dail_Call_Initial = Blueprint('Dail_Call_Initial', __name__,
    static_folder='static')

@Dail_Call_Initial.route('/Start',  methods=['GET', 'POST'])
def list():
    return "Test1"

