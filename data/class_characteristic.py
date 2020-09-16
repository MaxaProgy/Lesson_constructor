import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class ClassCharacteristic(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'class_characteristic'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name_class_characteristic = sqlalchemy.Column(sqlalchemy.String)