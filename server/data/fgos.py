import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Fgos(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'fgos'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name_fgos = sqlalchemy.Column(sqlalchemy.String)

    methods = orm.relation("Methods", back_populates='fgos')
