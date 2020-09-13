import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Cards(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'cards'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    name_method = sqlalchemy.Column(sqlalchemy.String)
    time = sqlalchemy.Column(sqlalchemy.String)

    classes_number = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("classes.name_class"))
    type_method_card = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("type_method.name_method"))
    stage_card = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("stage.name_stage"))

    creative_thinking = sqlalchemy.Column(sqlalchemy.Boolean)
    critical_thinking = sqlalchemy.Column(sqlalchemy.Boolean)
    communication = sqlalchemy.Column(sqlalchemy.Boolean)
    cooperation = sqlalchemy.Column(sqlalchemy.Boolean)
    metacognitive_skills = sqlalchemy.Column(sqlalchemy.Boolean)
    literacy = sqlalchemy.Column(sqlalchemy.Boolean)

    fgos_card = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("fgos.name_fgos"))
    text = sqlalchemy.Column(sqlalchemy.Text)

    classes = orm.relationship('Classes')
    type_method = orm.relationship('TypeMethod')
    stage = orm.relationship('Stage')
    fgos = orm.relationship('Fgos')
