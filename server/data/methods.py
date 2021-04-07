# -*- coding: utf-8 -*-

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Methods(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'methods'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    date_create = sqlalchemy.Column(sqlalchemy.Integer)
    date_edit = sqlalchemy.Column(sqlalchemy.Integer)

    name_method = sqlalchemy.Column(sqlalchemy.String)
    time = sqlalchemy.Column(sqlalchemy.String)

    id_user = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    id_classes_number = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("classes.id"))
    id_type_method = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("type_method.id"))
    id_stage_method = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("stage.id"))
    id_fgos = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("fgos.id"))
    creative_thinking = sqlalchemy.Column(sqlalchemy.Boolean)
    critical_thinking = sqlalchemy.Column(sqlalchemy.Boolean)
    communication = sqlalchemy.Column(sqlalchemy.Boolean)
    cooperation = sqlalchemy.Column(sqlalchemy.Boolean)
    metacognitive_skills = sqlalchemy.Column(sqlalchemy.Boolean)
    literacy = sqlalchemy.Column(sqlalchemy.Boolean)

    is_local = sqlalchemy.Column(sqlalchemy.Boolean)
    text = sqlalchemy.Column(sqlalchemy.Text)

    user = orm.relation('User')
    classes = orm.relation('Classes')
    type_method = orm.relation('TypeMethod')
    stage = orm.relation('Stage')
    fgos = orm.relation('Fgos')
