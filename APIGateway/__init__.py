from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_pyfile('/APIGateway/config.py')
jwt = JWTManager(app)

from APIGateway import routes
