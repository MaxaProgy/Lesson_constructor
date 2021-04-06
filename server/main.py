# -*- coding: utf-8 -*-

from flask import Flask
import logging

from flask_restful import Api

from server.data.api.method_resource import MethodResource, MethodsListResource
from server.data.api.save_lesson_resource import SaveLessonResource, SaveLessonListResource
from server.data.api.user_resource import PostUserResource, GetUserResource

from server.const import *
from flask_login import LoginManager


logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = os.urandom(24)


api.add_resource(MethodResource, '/api/v1/method/<int:method_id>')
api.add_resource(MethodsListResource, '/api/v1/methods')

api.add_resource(SaveLessonResource, '/api/v1/save_lesson/<save_lesson_id>')
api.add_resource(SaveLessonListResource, '/api/v1/save_lessons')

api.add_resource(GetUserResource, '/api/v1/user/<int:user_id>')
api.add_resource(PostUserResource, '/api/v1/users')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)
