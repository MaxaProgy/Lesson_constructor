from os import path
from data import db_session

from data.type_method import TypeMethod
from data.stage import Stage
from data.classes import Classes
from data.fgos import Fgos
from data.subject import Subject
from data.class_characteristic import ClassCharacteristic
from data.lesson_type import LessonType

PATH_SPLASH_SCREEN = path.join('data', 'image', 'фоны', 'заставка.png')
PATH_MAIN_MENU = path.join('data', 'image', 'фоны', 'меню.jpg')

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
                  "Новый материал", "Бодрилки", "Проверка понимания", "Закрепление материала",
                  "Контроль усвоения", "Рефлексия", "Домашнее задание"]
SUBJECT_VALUE_DB = ["Начальные классы", "География", "Биология", "Химия", "Физика",
                    "Математика ", "Алгебра", "Геометрия", "Иностранный язык",
                    "Русский язык", "Литература", "Технология", "Физкультура", "Изобразительное искусство",
                    "Музыка", "История", "Обществознание"]
CLASS_CHARACTERISTIC_VALUE_DB = ["Активные дети", "Пассивные дети", "Дружный класс",
                                 "Имеется наличие лидера (лидеров)", "Имеются проблемы с дисциплиной"]
LESSON_TYPE_VALUE_DB = ["Новый материал", "Контроль усвоения",
                        "Проверка понимания", "Закрепление материала"]

db_session.global_init("db/lesson_constructor_db.sqlite")
SESSION = db_session.create_session()

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
