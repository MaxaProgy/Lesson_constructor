import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Subject(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'subject'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name_subject = sqlalchemy.Column(sqlalchemy.String)
