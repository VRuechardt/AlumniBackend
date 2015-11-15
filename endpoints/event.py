
from flask_restful import Resource, reqparse
import sqlite3
from decorators.auth import restricted

class Event(Resource):
    def get(self):
        return {}