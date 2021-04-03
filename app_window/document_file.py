def get_document_result_word(topic_lesson, teacher, subject, lesson_class, duration, competence, methods):
    from docx import Document

    document = Document()

    document.add_heading(f'Урок по теме "{topic_lesson}"', 0)

    p = document.add_paragraph('Учитель: ')
    p.add_run(f'{", ".join(teacher)}').bold = True
    p = document.add_paragraph('Предмет: ')
    p.add_run(f'{subject}').bold = True
    p = document.add_paragraph('Класс: ')
    p.add_run(f'{lesson_class}').bold = True
    p = document.add_paragraph('Длительность урока: ')
    p.add_run(f'{duration}').bold = True
    p = document.add_paragraph('Планируемое формирование компетенций: ')
    p.add_run(f'{", ".join(competence)}').bold = True

    document.add_heading('Этапы урока', level=1)

    table = document.add_table(rows=1, cols=5)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = '№ этапа'
    hdr_cells[1].text = 'Название'
    hdr_cells[2].text = 'Тип'
    hdr_cells[3].text = 'Описание'
    hdr_cells[4].text = 'Длительность (минут)'
    for i in range(len(methods)):
        row_cells = table.add_row().cells
        row_cells[0].text = str(i + 1)
        row_cells[1].text = methods[i][1][0].upper() + methods[i][1][1:].lower()
        row_cells[2].text = methods[i][0]
        if methods[i][2] is None:
            row_cells[3].text = ' - '
        else:
            row_cells[3].text = methods[i][2]
        row_cells[4].text = methods[i][3]

    document.add_page_break()
    return document


html_document = ['<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN"><html><head>'
                 ' <meta http-equiv="content-type" content="text/html; charset=iso-8859-1"/><title></title>'
                 '<meta name="generator" content="LibreOffice 6.1.5.2 (Linux)"/>'
                 '<meta name="user" content="python-docx"/><meta name="created" content="2013-12-23T23:15:00"/>'
                 '<meta name="changed" content="2013-12-23T23:15:00"/>'
                 '<meta name="description" content="generated by python-docx"/>'
                 '<meta name="AppVersion" content="14.0000"/><meta name="DocSecurity" content="0"/>'
                 '<meta name="HyperlinksChanged" content="false"/><meta name="LinksUpToDate" content="false"/>'
                 '<meta name="ScaleCrop" content="false"/><meta name="ShareDoc" content="false"/>'
                 '<style type="text/css">@page { size: 8.5in 11in; margin-left: 1.25in;'
                 'margin-right: 1.25in; margin-top: 1in; margin-bottom: 1in }p { margin-bottom: 0.08in;'
                 'direction: ltr; line-height: 115%; text-align: left; orphans: 2; widows: 2; background: transparent }'
                 'h1 { margin-top: 0.33in; margin-bottom: 0in; direction: ltr; color: #365f91; line-height: 115%;'
                 'text-align: left; page-break-inside: avoid; orphans: 2; widows: 2; background:'
                 'transparent; page-break-after: avoid }h1.western { font-family: "Calibri", serif; font-size:'
                 '14pt; font-weight: bold }h1.cjk { font-family: "MS ????"; font-size: 14pt; font-weight: bold }'
                 'h1.ctl { font-family: ; font-size: 14pt; font-weight: bold }'
                 '</style></head><body lang="en-US" link="#000080" vlink="#800000" dir="ltr">',

                 '<h1 class="western">Этапы урока</h1><table width="576" cellpadding="7" cellspacing="0">'
                 '<col width="101"/><col width="101"/><col width="101"/><col width="101"/><col width="101"/>'
                 '<tr valign="top"><td width="101" style="border: none; padding: 0in"><p>№ этапа</p></td>'
                 '<td width="101" style="border: none; padding: 0in"><p>Название</p></td>'
                 '<td width="101" style="border: none; padding: 0in"><p>Тип</p></td>'
                 '<td width="101" style="border: none; padding: 0in"><p>Описание</p></td>'
                 '<td width="101" style="border: none; padding: 0in"><p>Длительность (минут)</p></td></tr>',

                 '</table><p style="margin-bottom: 0.14in"><br/><br/></p></body></html>']


def get_document_result(topic_lesson, subject, lesson_class, duration, competence, methods):
    info_lesson = '<p style="margin-bottom: 0.21in; border-top: none; border-bottom: 1.00pt solid #4f81bd;' \
                  ' border-left: ' \
                  'none; border-right: none; padding-top: 0in; padding-bottom: 0.06in; padding-left: 0in;' \
                  ' padding-right: 0in;' \
                  'letter-spacing: 0.3pt; line-height: 100%"><font color="#17365d"><font face="Calibri, serif">' \
                  f'<font size="6" style="font-size: 26pt">Урок по теме "{topic_lesson}"</font></font></font></p>' \
                  f'<p style="margin-bottom: 0.14in">Предмет: <b>{subject}</b></p>' \
                  f'<p style="margin-bottom: 0.14in">Класс: <b>{lesson_class}</b></p>' \
                  f'<p style="margin-bottom: 0.14in">Длительность урока: <b>{duration}</b></p>' \
                  '<p style="margin-bottom: 0.14in">Планируемое формирование компетенций: ' \
                  f'<b>{", ".join(competence)}</b></p>'

    info_methods = ''
    for i in range(len(methods)):
        info_methods += '<tr valign="top"><td width="101" style="border: none; padding: 0in">' \
                        '</td><td width="101" style="border: none; padding: 0in">' \
                        f'<p>{methods[i][1][0].upper() + methods[i][1][1:].lower()}</p>' \
                        '</td><td width="101" style="border: none; padding: 0in">' \
                        f'<p>{methods[i][0]}</p>' \
                        '</td><td width="101" style="border: none; padding: 0in">' \
                        f'<p>{methods[i][2]}</p>' \
                        '</td><td width="101" style="border: none; padding: 0in">' \
                        f'<p>{methods[i][3]}</p>' \
                        ' </td></tr>'

    document = html_document[0] + info_lesson + html_document[1] + info_methods + html_document[2]
    return document
