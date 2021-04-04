# -*- coding: utf-8 -*-

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class TypeMethod(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'type_method'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name_method = sqlalchemy.Column(sqlalchemy.String)

    methods = orm.relation("Methods", back_populates='type_method')
