# -*- coding: utf-8 -*-

import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class LessonType(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'lesson_type'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name_lesson_type = sqlalchemy.Column(sqlalchemy.String)
