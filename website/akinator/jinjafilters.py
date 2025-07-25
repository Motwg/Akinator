from inflection import parameterize
from markupsafe import Markup


# This data would better go in a database...
errorDict = {
    "Err1": "ERROR 1: watch out for error n.1!",
    "Err2": "ERROR 2: watch out for error n.2!",
    "Err9": "ERROR 9: watch out for error n.9!"
}


def display_error(err_num):
    key = "Err" + str(err_num)
    result = errorDict[key]
    return result


msgDict = {
    "Msg1": "<p>This is a <b>nice</b> message, the first of the list</p>",
    "Msg2": "<p>This is an even <b>nicer</b> message.</p>"
}


def display_message(msg_key):
    # THE DECORATOR IS NEEDED TO DISABLE CACHING OF JINJA CALLS!!!
    result = Markup(msgDict[msg_key])
    return result
