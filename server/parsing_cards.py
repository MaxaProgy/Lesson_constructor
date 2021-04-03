import pandas as pd

from server.data import db_session
from server.data.methods import Methods

data = pd.read_csv('server/db/Карточки.csv')
db_session.global_init("server/db/lesson_constructor_db.sqlite")
session = db_session.create_session()

for method in zip(data['название'], data['время'], data['классы'], data['индивидуальная/ групповая'],
                  data['этап урока'], data['креативное мышление'], data['критическое мышление'], data['коммуникация'],
                  data['кооперация'], data['метакогнитивные навыки'], data['грамотность'], data['фгос'], data['текст']):
    new_method = Methods(
        name_method=method[0],
        time=method[1],
        id_classes_number=method[2],
        id_type_method_method=method[3],
        id_stage_method=method[4],
        creative_thinking=method[5],
        critical_thinking=method[6],
        communication=method[7],
        cooperation=method[8],
        metacognitive_skills=method[9],
        literacy=method[10],
        id_fgos=method[11],
        text=method[12],
    )
    session.add(new_method)
    session.commit()
