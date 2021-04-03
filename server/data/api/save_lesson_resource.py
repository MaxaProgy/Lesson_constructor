from flask import jsonify
from flask_restful import reqparse, abort, Resource
from server.data import db_session
from server.data.save_lesson import SaveLesson


parser = reqparse.RequestParser()
parser.add_argument('name', required=True, type=str)
parser.add_argument('ids', required=True, type=str)
parser.add_argument('id_user', required=True, type=str)


def abort_if_save_lesson_not_found(save_lesson_id):
    session = db_session.create_session()
    save_lesson = session.query(SaveLesson).get(save_lesson_id)
    if not save_lesson:
        abort(404, message=f"SaveLesson {save_lesson_id} not found")


class SaveLessonResource(Resource):
    def get(self, save_lesson_id):
        abort_if_save_lesson_not_found(save_lesson_id)
        session = db_session.create_session()
        save_lesson = session.query(SaveLesson).get(save_lesson_id)
        return jsonify({'save_lesson': save_lesson.to_dict(
            only=('name', 'ids', 'id_user',))})

    def delete(self, save_lesson_id):
        abort_if_save_lesson_not_found(save_lesson_id)
        session = db_session.create_session()
        save_lesson = session.query(SaveLesson).get(save_lesson_id)
        session.delete(save_lesson)
        session.commit()
        return jsonify({'success': 'OK'})


class SaveLessonListResource(Resource):
    def get(self):
        session = db_session.create_session()
        save_lessons = session.query(SaveLesson).all()
        return jsonify({'categories': [item.to_dict(
            only=('name', 'ids', 'id_user',))
            for item in save_lessons]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        save_lesson = SaveLesson(
            name=args['name'],
            ids=args['ids'],
            id_user=args['id_user'],
        )
        session.add(save_lesson)
        session.commit()
        return jsonify({'success': 'OK'})
