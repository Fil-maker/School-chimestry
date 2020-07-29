from flask import Flask
from flask_restful import Api

from api.data import db_session

app = Flask(__name__)
api = Api(app)



db_session.global_init("api/db/misschedule.sqlite")


from api import auth