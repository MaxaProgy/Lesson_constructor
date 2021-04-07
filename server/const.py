# -*- coding: utf-8 -*-
from server.data import db_session
from server.data.classes import Classes
from server.data.quote import Quote
from server.data.fgos import Fgos
from server.data.stage import Stage
from server.data.type_method import TypeMethod
from server.data.class_characteristic import ClassCharacteristic
from server.data.lesson_type import LessonType
from server.data.subject import Subject
from server.data.user import User


db_session.global_init("../server/db/lesson_constructor_server_db.sqlite")
session = db_session.create_session()

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


if not [item.name_user for item in session.query(User).all()]:
    user_value = User(
        name_user="Lesson Constructor",
    )
    session.add(user_value)
    session.commit()
    user_value = User(
        name_user="я",
    )
    session.add(user_value)
    session.commit()

if not [item.name_method for item in session.query(TypeMethod).all()]:
    for value in TYPE_METHOD_VALUE_DB:
        type_method_value = TypeMethod(
            name_method=value,
        )
        session.add(type_method_value)
        session.commit()

if not [item.name_class for item in session.query(Classes).all()]:
    for value in CLASSES_VALUE_DB:
        classes_value = Classes(
            name_class=value,
        )
        session.add(classes_value)
        session.commit()

if not [item.name_fgos for item in session.query(Fgos).all()]:
    for value in FGOS_VALUE_DB:
        fgos_value = Fgos(
            name_fgos=value,
        )
        session.add(fgos_value)
        session.commit()

if not [item.name_stage for item in session.query(Stage).all()]:
    for value in STAGE_VALUE_DB:
        stage_value = Stage(
            name_stage=value,
        )
        session.add(stage_value)
        session.commit()

if not [item.name_subject for item in session.query(Subject).all()]:
    for value in SUBJECT_VALUE_DB:
        subject_value = Subject(
            name_subject=value,
        )
        session.add(subject_value)
        session.commit()

if not [item.name_class_characteristic for item in
        session.query(ClassCharacteristic).all()]:
    for value in CLASS_CHARACTERISTIC_VALUE_DB:
        class_characteristic_value = ClassCharacteristic(
            name_class_characteristic=value,
        )
        session.add(class_characteristic_value)
        session.commit()

if not [item.text for item in
        session.query(Quote).all()]:
    for value in LIST_LESSON_QUOTE:
        quotes = Quote(
            text=value,
        )
        session.add(quotes)
        session.commit()

if not [item.name_lesson_type for item in session.query(LessonType).all()]:
    for value in LESSON_TYPE_VALUE_DB:
        lesson_type_value = LessonType(
            name_lesson_type=value,
        )
        session.add(lesson_type_value)
        session.commit()
