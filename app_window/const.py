from os import path

import pandas as pd

from app_window.data import db_session
from app_window.data.cards import Cards
from app_window.data.classes import Classes
from app_window.data.fgos import Fgos
from app_window.data.stage import Stage
from app_window.data.type_method import TypeMethod
from app_window.data.class_characteristic import ClassCharacteristic
from app_window.data.lesson_type import LessonType
from app_window.data.subject import Subject

PATH_SPLASH_SCREEN = path.join('data', 'image', 'background', 'заставка.png')
PATH_MAIN_MENU = path.join('data', 'image', 'background', 'main_background_app.jpg')
PATH_BUTTON_OK = 'data/image/ok.png'
PATH_BUTTON_OK_HOVER = 'data/image/ok2.png'
PATH_BUTTON_BACK = 'data/image/back.png'
PATH_BUTTON_BACK_HOVER = 'data/image/back2.png'
PATH_BUTTON_PADROBNEE = 'data/image/Podtobnee.png'
PATH_BUTTON_PADROBNEE_HOVER = 'data/image/Podtobnee2.png'
PATH_BUTTON_ADD = 'data/image/add.png'
PATH_BUTTON_ADD_HOVER = 'data/image/add2.png'
PATH_BUTTON_DEL = 'data/image/del.png'
PATH_BUTTON_DEL_HOVER = 'data/image/del2.png'

LIST_LESSON_QUOTE = ["Учитель прикасается к вечности, никто не знает, где закончится его влияние..",
                     "Кто постигает новое, лелея старое, Тот может быть учителем.",
                     "Тот, кто обращаясь к старому, способен открывать новое, достоин быть учителем.",
                     "Книга — немой учитель.",
                     "Плохой учитель преподносит истину, хороший учит ее находить.",
                     "Гений – это талант изобретения того, чему нельзя учить или научиться.",
                     "Весьма имеют быть наставлены те, которые сами не знают.",
                     "Кто хорошо выявляет различия, тот хорошо учит.",
                     "Как в утлый мех воду лить, так безумного учить.",
                     "Учись тому, чему сам учишь.",
                     "Хорошо учит говорить тот, кто учит хорошо делать.",
                     "Опыт – самый лучший учитель, но плата за обучение чересур велика."]

TYPE_METHOD_VALUE_DB = ["Индивидуальная", "Групповая", "Индивидуальная/Групповая"]
CLASSES_VALUE_DB = ["1-4", "5-8", "9-11", "1-11", "1-8", "5-11"]
FGOS_VALUE_DB = ["Предметные", "Личностные", "-"]
STAGE_VALUE_DB = ["Знакомство", "Командообразование",
                  "Новый материал", "Бодрилки", "Проверка понимания", "Закрепление",
                  "Контроль усвоения", "Рефлексия", "Домашнее задание"]
SUBJECT_VALUE_DB = ["Начальные классы", "География", "Биология", "Химия", "Физика",
                    "Математика ", "Алгебра", "Геометрия", "Иностранный язык",
                    "Русский язык", "Литература", "Технология", "Физкультура", "Изобразительное искусство",
                    "Музыка", "История", "Обществознание"]
CLASS_CHARACTERISTIC_VALUE_DB = ["Активные дети", "Пассивные дети", "Дружный класс",
                                 "Имеется наличие лидера (лидеров)", "Имеются проблемы с дисциплиной"]
LESSON_TYPE_VALUE_DB = ["Новый материал", "Контроль усвоения",
                        "Проверка понимания", "Закрепление материала"]

data = pd.read_csv('db/Карточки.csv')
db_session.global_init("db/lesson_constructor_db.sqlite")
SESSION = db_session.create_session()

for card in zip(data['название'], data['время'], data['классы'], data['индивидуальная/ групповая'],
                data['этап урока'], data['креативное мышление'], data['критическое мышление'], data['коммуникация'],
                data['кооперация'], data['метакогнитивные навыки'], data['грамотность'], data['фгос'], data['текст']):
    new_card = Cards(
        name_method=card[0],
        time=card[1],
        id_classes_number=card[2],
        id_type_method_card=card[3],
        id_stage_card=card[4],
        creative_thinking=card[5],
        critical_thinking=card[6],
        communication=card[7],
        cooperation=card[8],
        metacognitive_skills=card[9],
        literacy=card[10],
        id_fgos=card[11],
        text=card[12],
    )
    SESSION.add(new_card)
    SESSION.commit()


if not [item.name_method for item in SESSION.query(TypeMethod).all()]:
    for value in TYPE_METHOD_VALUE_DB:
        type_method_value = TypeMethod(
            name_method=value,
        )
        SESSION.add(type_method_value)
        SESSION.commit()

if not [item.name_class for item in SESSION.query(Classes).all()]:
    for value in CLASSES_VALUE_DB:
        classes_value = Classes(
            name_class=value,
        )
        SESSION.add(classes_value)
        SESSION.commit()

if not [item.name_fgos for item in SESSION.query(Fgos).all()]:
    for value in FGOS_VALUE_DB:
        fgos_value = Fgos(
            name_fgos=value,
        )
        SESSION.add(fgos_value)
        SESSION.commit()

if not [item.name_stage for item in SESSION.query(Stage).all()]:
    for value in STAGE_VALUE_DB:
        stage_value = Stage(
            name_stage=value,
        )
        SESSION.add(stage_value)
        SESSION.commit()

if not [item.name_subject for item in SESSION.query(Subject).all()]:
    for value in SUBJECT_VALUE_DB:
        subject_value = Subject(
            name_subject=value,
        )
        SESSION.add(subject_value)
        SESSION.commit()

if not [item.name_class_characteristic for item in
        SESSION.query(ClassCharacteristic).all()]:
    for value in CLASS_CHARACTERISTIC_VALUE_DB:
        class_characteristic_value = ClassCharacteristic(
            name_class_characteristic=value,
        )
        SESSION.add(class_characteristic_value)
        SESSION.commit()

if not [item.name_lesson_type for item in SESSION.query(LessonType).all()]:
    for value in LESSON_TYPE_VALUE_DB:
        lesson_type_value = LessonType(
            name_lesson_type=value,
        )
        SESSION.add(lesson_type_value)
        SESSION.commit()
