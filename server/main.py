# -*- coding: utf-8 -*-
import json
import os

from flask import Flask
import logging

from flask_restful import Api

from server.data.api.method_resource import MethodResource, MethodsListResource
from server.data.api.save_lesson_resource import SaveLessonResource, SaveLessonListResource
from server.data.api.user_resource import PostUserResource, GetUserResource
from flask import request, jsonify
from server.const import *
from flask_login import LoginManager

from server.data.methods import Methods

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = os.urandom(24)


@app.route('/update_data', methods=['POST'])
def update_data():
    data = json.loads(request.json)
    session = db_session.create_session()
    for method in session.query(Methods).filter(Methods.id_user == data['method'][0]['id_user']).all():
        session.delete(method)
    session.commit()

    for client_method in data['method']:
        new_method = Methods(
            date_create=client_method["date_create"],
            date_edit=client_method["date_edit"],
            name_method=client_method["name_method"],
            time=client_method["time"],
            id_user=client_method["id_user"],
            id_classes_number=client_method["id_classes_number"],
            id_type_method=client_method["id_type_method"],
            id_stage_method=client_method["id_stage_method"],
            creative_thinking=client_method["creative_thinking"],
            critical_thinking=client_method["critical_thinking"],
            communication=client_method["communication"],
            cooperation=client_method["cooperation"],
            metacognitive_skills=client_method["metacognitive_skills"],
            literacy=client_method["literacy"],
            is_local=client_method["is_local"],
            id_fgos=client_method["id_fgos"],
            text=client_method["text"],
        )
        session.add(new_method)
    session.commit()

    return jsonify(request.json)


api.add_resource(MethodResource, '/api/v1/method/<int:method_id>')
api.add_resource(MethodsListResource, '/api/v1/methods')

api.add_resource(SaveLessonResource, '/api/v1/save_lesson/<save_lesson_id>')
api.add_resource(SaveLessonListResource, '/api/v1/save_lessons')

api.add_resource(GetUserResource, '/api/v1/user/<int:user_id>')
api.add_resource(PostUserResource, '/api/v1/users')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
