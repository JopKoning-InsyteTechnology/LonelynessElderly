from flask import Blueprint

products_bp = Blueprint('products_bp', __name__,
    static_folder='static')

@products_bp.route('/test')
def list():
    return "Test1"
