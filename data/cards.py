import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Cards(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'cards'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    name_method = sqlalchemy.Column(sqlalchemy.String)
    time = sqlalchemy.Column(sqlalchemy.String)

    classes_number = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("classes.id"))
    type_method = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("type_method.id"))
    stage = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("stage.id"))

    creative_thinking = sqlalchemy.Column(sqlalchemy.Boolean)
    critical_thinking = sqlalchemy.Column(sqlalchemy.Boolean)
    communication = sqlalchemy.Column(sqlalchemy.Boolean)
    cooperation = sqlalchemy.Column(sqlalchemy.Boolean)
    metacognitive_skills = sqlalchemy.Column(sqlalchemy.Boolean)
    literacy = sqlalchemy.Column(sqlalchemy.Boolean)

    fgos = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("fgos.id"))
    text = sqlalchemy.Column(sqlalchemy.Text)

    classes_table = orm.relation('Classes')
    type_method_table = orm.relation('TypeMethod')
    stage_table = orm.relation('Stage')
    fgos_table = orm.relation('Fgos')
