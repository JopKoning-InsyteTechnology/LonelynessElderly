from flask import Flask
from Test1.Test1 import  products_bp
from Test2.Test2 import  products_bp_2


app = Flask(__name__)
app.register_blueprint(products_bp, url_prefix='/Test')
app.register_blueprint(products_bp_2)


# if __name__ == "__main__":
#     app.run(debug=True)