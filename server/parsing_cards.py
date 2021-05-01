# -*- coding: utf-8 -*-

import os

import pandas as pd

from server.data import db_session
from server.data.methods import Methods

if not os.path.isfile("../server/db/lesson_constructor_server_db.sqlite"):
    data = pd.read_csv('../server/db/Карточки.csv')
    db_session.global_init("../server/db/lesson_constructor_server_db.sqlite")
    session = db_session.create_session()

    for method in zip(data['дата создания'], data['дата изменения'], data['название'], data['время'],
                      data['автор'], data['классы'],
                      data['тип урока'], data['этап урока'],
                      data['креативное мышление'], data['критическое мышление'],
                      data['коммуникация'], data['кооперация'], data['метакогнитивные навыки'],
                      data['грамотность'], data['фгос'], data['локально'], data['текст']):
        new_method = Methods(
            date_create=method[0],
            date_edit=method[1],
            name_method=method[2],
            time=method[3],
            id_user=method[4],
            id_classes_number=method[5],
            id_type_method=method[6],
            id_stage_method=method[7],
            creative_thinking=method[8],
            critical_thinking=method[9],
            communication=method[10],
            cooperation=method[11],
            metacognitive_skills=method[12],
            literacy=method[13],
            id_fgos=method[14],
            is_local=method[15],
            text=method[16],
        )
        session.add(new_method)
        session.commit()
else:
    db_session.global_init("../server/db/lesson_constructor_server_db.sqlite")
    session = db_session.create_session()
