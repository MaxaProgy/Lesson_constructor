from flask import jsonify
from flask_restful import reqparse, abort, Resource
from server.data import db_session
from server.data.user import User

parser = reqparse.RequestParser()
parser.add_argument('name', required=True, type=str)
parser.add_argument('email', required=True, type=str)
parser.add_argument('password', required=True, type=str)


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class GetUserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': {
            'name_user': user.name_user,
            'email': user.email, 'save_lesson': user.save_lesson,
            "methods_id": [method.id for method in user.methods]}})


class PostUserResource(Resource):
    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            name_user=args['name_user'],
            email=args['email'],
            save_lesson=[],
            methods_id=[]
        )
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
