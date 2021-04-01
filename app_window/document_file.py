html_document = ['<!DOCTYPE html><html><head><title>be1.ru</title></head><body>'
                 '<p style="text-align:center">&nbsp;</p>'
                 '<p style="text-align:center">&nbsp;</p>'
                 '<p style="text-align:center">&nbsp;</p><p style="text-align:center">',

                 '<p style="text-align:center"><span style="font-family:Times New Roman,Times,serif">'
                 '<span style="font-size:18px">Этапы урока</span></span></p>'
                 '<p style="text-align:center">&nbsp;</p>'
                 '<table align="center" border="1" cellpadding="1" cellspacing="1" style="width:800px"><thead><tr>'
                 '<th scope="col"><p>№</p><p>этапа</p></th><th scope="col">Тип</th><th scope="col">Название</th>'
                 '<th scope="col">Описание</th><th scope="col">Длительность (минут)</th></tr></thead><tbody>',

                 '</tbody></table><p style="margin-left:80px">&nbsp;</p></body></html>']


def get_document_result(topic_lesson, subject, lesson_class, duration, competence, methods):
    info_lesson = '<span style="font-size:18px"><span style="font-family:Times New Roman,Times,serif">' \
                  f'Урок по теме "{topic_lesson}"' \
                  '</span></span></p>' \
                  '<p style="margin-left:80px"><span style="font-family:Times New Roman,Times,serif">' \
                  '<span style="font-size:14px">' \
                  f'Предмет:&nbsp; {subject}' \
                  '</span></span></p>' \
                  '<p style="margin-left:80px"><span style="font-family:Times New Roman,Times,serif">' \
                  '<span style="font-size:14px">' \
                  f'Класс: {lesson_class}' \
                  '</span></span></p>' \
                  '<p style="margin-left:80px"><span style="font-family:Times New Roman,Times,serif">' \
                  '<span style="font-size:14px">' \
                  f'Длительность урока: {duration}' \
                  '</span></span></p>' \
                  '<p style="margin-left:80px"><span style="font-family:Times New Roman,Times,serif">' \
                  '<span style="font-size:14px">' \
                  f'Планируемое формирование компетенций: {", ".join(competence)}' \
                  '</span> </span></p>' \
                  '<p style="margin-left:80px">&nbsp;</p>'

    info_methods = ''
    for i in range(len(methods)):
        info_methods += '<tr>' \
                        f'<td style="text-align:center">{i}</td>' \
                        f'<td>&nbsp;{methods[i][0]}</td>' \
                        f'<td>&nbsp;{methods[i][1]}</td>' \
                        f'<td>&nbsp;{methods[i][2]}</td>' \
                        f'<td>&nbsp;{methods[i][3]}</td>' \
                        '</tr>'
    document = html_document[0] + info_lesson + html_document[1] + info_methods + html_document[2]
    return document
