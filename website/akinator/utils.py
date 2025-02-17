from flask import request


def convert_datatime(rows: dict, field_name: str):
    for r in rows:
        r[field_name] = r[field_name].strftime('%d/%m/%Y, %H:%M:%S')


def read_data_from_form():
    record = {}
    for key in request.form:
        record[key] = request.form[key]
        if len(record[key]) == 0:
            record[key] = None
        elif record[key] == 'on':
            # checkbox selected!!!
            record[key] = True
    # NOTE: if a checkbox is not selected,
    #      it will NOT be part of the record dict!
    return record


def set_menu(section):
    menu_config = {}

    if len(section) > 0:
        menu_config[section] = "active"

    return menu_config
