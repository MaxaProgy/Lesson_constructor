import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Classes(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'classes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name_class = sqlalchemy.Column(sqlalchemy.String)

    cards = orm.relation("Cards", back_populates='classes')
