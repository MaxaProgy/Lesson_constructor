# -*- coding: utf-8 -*-

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class DocumentsLesson(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'documents_lesson'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.Integer)

    lesson_topic = sqlalchemy.Column(sqlalchemy.String)
    subject = sqlalchemy.Column(sqlalchemy.String)
    class_lesson = sqlalchemy.Column(sqlalchemy.String)
    lesson_duration = sqlalchemy.Column(sqlalchemy.Integer)
    competence = sqlalchemy.Column(sqlalchemy.String)

    ids = sqlalchemy.Column(sqlalchemy.String)
    id_user = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))

    user = orm.relation('User')
