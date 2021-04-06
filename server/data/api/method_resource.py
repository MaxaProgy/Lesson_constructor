from flask import jsonify
from flask_restful import reqparse, abort, Resource
from server.data import db_session
from server.data.methods import Methods

parser = reqparse.RequestParser()
parser.add_argument('name_method', required=True, type=str)
parser.add_argument('time', required=True, type=str)
parser.add_argument('id_user', required=True, type=str)
parser.add_argument('id_classes_number', required=True, type=str)
parser.add_argument('id_type_method', required=True, type=str)
parser.add_argument('id_stage_method', required=True, type=str)
parser.add_argument('id_fgos', required=True, type=str)
parser.add_argument('creative_thinking', required=True, type=str)
parser.add_argument('critical_thinking', required=True, type=str)
parser.add_argument('communication', required=True, type=str)
parser.add_argument('cooperation', required=True, type=str)
parser.add_argument('metacognitive_skills', required=True, type=str)
parser.add_argument('literacy', required=True, type=str)
parser.add_argument('text', required=True, type=str)
parser.add_argument('is_local', required=True, type=str)


def abort_if_method_not_found(method_id):
    session = db_session.create_session()
    method = session.query(Methods).get(method_id)
    if not method:
        abort(404, message=f"Method {method_id} not found")


class MethodResource(Resource):
    def get(self, method_id):
        abort_if_method_not_found(method_id)
        session = db_session.create_session()
        method = session.query(Methods).get(method_id)
        return jsonify({'method': method.to_dict(
            only=('name_method', 'time', 'id_user', 'id_classes_number', 'id_type_method', 'id_stage_method',
                  'id_fgos', 'is_local', 'creative_thinking', 'critical_thinking', 'communication', 'cooperation',
                                                                       'metacognitive_skills', 'literacy',
                  'text',))})

    def delete(self, method_id):
        abort_if_method_not_found(method_id)
        session = db_session.create_session()
        method = session.query(Methods).get(method_id)
        session.delete(method)
        session.commit()
        return jsonify({'success': 'OK'})


class MethodsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        methods = session.query(Methods).all()
        return jsonify({'methods': [item.to_dict(
            only=('name_method', 'time', 'id_user', 'id_classes_number', 'id_type_method', 'id_stage_method',
                  'id_fgos', 'is_local', 'creative_thinking', 'critical_thinking', 'communication', 'cooperation',
                  'metacognitive_skills', 'literacy',
                  'text',)) for item in methods]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        method = Methods(
            name_method=args['name_method'],
            time=args['time'],
            id_user=args['id_user'],
            id_classes_number=args['id_classes_number'],
            id_type_method=args['id_type_method'],
            id_stage_method=args['id_stage_method'],
            id_fgos=args['id_fgos'],
            creative_thinking=args['creative_thinking'],
            critical_thinking=args['critical_thinking'],
            communication=args['communication'],
            cooperation=args['cooperation'],
            metacognitive_skills=args['metacognitive_skills'],
            literacy=args['literacy'],
            is_local=args['is_local'],
            text=args['text'],
        )
        session.add(method)
        session.commit()
        return jsonify({'success': 'OK'})
