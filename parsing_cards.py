import pandas as pd

from data import db_session
from data.cards import Cards

data = pd.read_csv('db/Карточки.csv')
db_session.global_init("db/lesson_constructor_db.sqlite")
session = db_session.create_session()

for card in zip(data['название'], data['время'], data['классы'], data['индивидуальная/ групповая'],
                data['этап урока'], data['креативное мышление'], data['критическое мышление'], data['коммуникация'],
                data['кооперация'], data['метакогнитивные навыки'], data['грамотность'], data['фгос'], data['текст']):
    new_card = Cards(
        name_method=card[0],
        time=card[1],
        id_classes_number=card[2],
        id_type_method_card=card[3],
        id_stage_card=card[4],
        creative_thinking=int(card[5]),
        critical_thinking=card[6],
        communication=card[7],
        cooperation=card[8],
        metacognitive_skills=card[9],
        literacy=card[10],
        id_fgos=card[11],
        text=card[12],
    )
    session.add(new_card)
    session.commit()
