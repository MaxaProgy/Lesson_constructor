# -*- coding: utf-8 -*-

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class SaveLesson(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'save_lesson'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    date_create = sqlalchemy.Column(sqlalchemy.Integer)
    date_edit = sqlalchemy.Column(sqlalchemy.Integer)

    name = sqlalchemy.Column(sqlalchemy.String)
    ids = sqlalchemy.Column(sqlalchemy.String)
    id_user = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))

    user = orm.relation('User')
