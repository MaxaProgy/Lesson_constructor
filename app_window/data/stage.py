# -*- coding: utf-8 -*-

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Stage(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'stage'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name_stage = sqlalchemy.Column(sqlalchemy.String)

    methods = orm.relation("Methods", back_populates='stage')
