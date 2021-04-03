import os

import pandas as pd

from server.data import db_session
from server.data.methods import Methods
from server.data.classes import Classes
from server.data.quote import Quote
from server.data.fgos import Fgos
from server.data.stage import Stage
from server.data.type_method import TypeMethod
from server.data.class_characteristic import ClassCharacteristic
from server.data.lesson_type import LessonType
from server.data.subject import Subject
from server.data.user import User


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
                     "Опыт – самый лучший учитель, но плата за обучение чересчур велика."]

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

if not os.path.isfile("../server/db/lesson_constructor_server_db.sqlite"):
    db_session.global_init("../server/db/lesson_constructor_server_db.sqlite")
    SESSION = db_session.create_session()
    data = pd.read_csv('../server/db/Карточки.csv')
    for method in zip(data['название'], data['время'], data['автор'], data['классы'], data['индивидуальная/ групповая'],
                      data['этап урока'], data['креативное мышление'], data['критическое мышление'],
                      data['коммуникация'], data['кооперация'], data['метакогнитивные навыки'],
                      data['грамотность'], data['фгос'], data['текст']):
        new_method = Methods(
            name_method=method[0],
            time=method[1],
            id_user=method[2],
            id_classes_number=method[3],
            id_type_method=method[4],
            id_stage_method=method[5],
            creative_thinking=method[6],
            critical_thinking=method[7],
            communication=method[8],
            cooperation=method[9],
            metacognitive_skills=method[10],
            literacy=method[11],
            id_fgos=method[12],
            text=method[13],
        )
        SESSION.add(new_method)
        SESSION.commit()
else:
    db_session.global_init("../server/db/lesson_constructor_server_db.sqlite")
    SESSION = db_session.create_session()

if not [item.name_user for item in SESSION.query(User).all()]:
    user_value = User(
        name_user="Lesson Constructor",
    )
    SESSION.add(user_value)
    SESSION.commit()
    user_value = User(
        name_user="я",
    )
    SESSION.add(user_value)
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

if not [item.text for item in
        SESSION.query(Quote).all()]:
    for value in LIST_LESSON_QUOTE:
        quotes = Quote(
            text=value,
        )
        SESSION.add(quotes)
        SESSION.commit()

if not [item.name_lesson_type for item in SESSION.query(LessonType).all()]:
    for value in LESSON_TYPE_VALUE_DB:
        lesson_type_value = LessonType(
            name_lesson_type=value,
        )
        SESSION.add(lesson_type_value)
        SESSION.commit()
