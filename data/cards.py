import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Cards(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'cards'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    name_method = sqlalchemy.Column(sqlalchemy.String)
    time = sqlalchemy.Column(sqlalchemy.String)

    id_classes_number = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("classes.id"))
    id_type_method_card = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("type_method.id"))
    id_stage_card = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("stage.id"))

    creative_thinking = sqlalchemy.Column(sqlalchemy.Boolean)
    critical_thinking = sqlalchemy.Column(sqlalchemy.Boolean)
    communication = sqlalchemy.Column(sqlalchemy.Boolean)
    cooperation = sqlalchemy.Column(sqlalchemy.Boolean)
    metacognitive_skills = sqlalchemy.Column(sqlalchemy.Boolean)
    literacy = sqlalchemy.Column(sqlalchemy.Boolean)

    id_fgos = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("fgos.id"))
    text = sqlalchemy.Column(sqlalchemy.Text)

    classes = orm.relation('Classes')
    type_method = orm.relation('TypeMethod')
    stage = orm.relation('Stage')
    fgos = orm.relation('Fgos')
