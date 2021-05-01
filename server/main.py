# -*- coding: utf-8 -*-
import json
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
from server.data.save_lesson import SaveLesson

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = os.urandom(24)


@app.route('/post_data_methods', methods=['POST'])
def post_data_methods():
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


@app.route('/get_data_methods', methods=['GET'])
def get_data_methods():
    session = db_session.create_session()
    methods = session.query(Methods).all()
    data = {'method': [item.to_dict(only=(
        'date_create', 'date_edit', 'name_method', 'time', 'id_user', 'id_classes_number', 'id_type_method',
        'id_stage_method',
        'id_fgos', 'is_local', 'creative_thinking', 'critical_thinking', 'communication', 'cooperation',
        'metacognitive_skills', 'literacy', 'text',)) for item in methods]}
    return jsonify(data)


@app.route('/post_data_user', methods=['POST'])
def post_data_user():
    data = json.loads(request.json)
    session = db_session.create_session()
    new_user = User(
        name_user=data['user'][0]["name_user"],
        email=data['user'][0]["email"],
        hashed_password=data['user'][0]["hashed_password"],
    )
    session.add(new_user)
    session.commit()

    return jsonify(request.json)


@app.route('/get_data_users', methods=['GET'])
def get_data_users():
    session = db_session.create_session()
    users = session.query(User).all()
    data = {'users': [item.to_dict(only=(
        'name_user', 'email', 'hashed_password', )) for item in users]}
    return jsonify(data)


@app.route('/post_data_save_lessons', methods=['POST'])
def post_data_save_lessons():
    data = json.loads(request.json)
    session = db_session.create_session()
    for save_lesson in session.query(SaveLesson).filter(SaveLesson.id_user == data['save_lessons'][0]['id_user']).all():
        session.delete(save_lesson)
    session.commit()

    for client_save_lesson in data['save_lessons']:
        save_lesson = Methods(
            date_create=client_save_lesson["date_create"],
            date_edit=client_save_lesson["date_edit"],
            name=client_save_lesson["name"],
            ids=client_save_lesson["ids"],
            id_user=client_save_lesson["id_user"],
        )
        session.add(save_lesson)
    session.commit()

    return jsonify(request.json)


@app.route('/get_data_save_lessons', methods=['GET'])
def get_data_save_lessons():
    session = db_session.create_session()
    save_lessons = session.query(SaveLesson).all()
    data = {'save_lessons': [item.to_dict(only=(
        'date_create', 'date_edit', 'name', 'ids', 'id_user',)) for item in save_lessons]}
    return jsonify(data)


api.add_resource(MethodResource, '/api/v1/method/<int:method_id>')
api.add_resource(MethodsListResource, '/api/v1/methods')

api.add_resource(SaveLessonResource, '/api/v1/save_lesson/<save_lesson_id>')
api.add_resource(SaveLessonListResource, '/api/v1/save_lessons')

api.add_resource(GetUserResource, '/api/v1/user/<int:user_id>')
api.add_resource(PostUserResource, '/api/v1/users')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
