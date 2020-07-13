import re

from datetime import datetime

password_pattern = "((?=.*[0-9])(?=.*[!@#$%&*s]).{6,20})"
email_regex = "^[\\w!#$%&'*+/=?`{|}~^-]+(?:\\.[\\w!#$%&'*+/=?`{|}~^-]+)*@(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,5}$"
format = "%Y-%m-%d %H:%M:%S"

def validate_password(password):
    return re.match(password_pattern, password)

def validate_email(email):
    return re.match(email_regex, email)

# method to validate null or empty check
def validate_null_or_empty(input, code, field, error):
    d = {}
    if(type(input) == str):
        if(input is None or input ==""):
            d["message"] = field + " cannot be null or empty"
            d["code"] = code
            error.append(d)
    elif(type(input) == int):
            if (input == 0):
                d["message"] = field + " cannot be null or empty"
                d["code"] = code
                error.append(d)
    elif (type(input) == float):
        if (input == 0.0):
            d["message"] =  field + " cannot be null or empty"
            d["code"] = code
            error.append(d)
    else:
        if (input is None or input == "" or len(input) == 0):
            d["message"] =  field + " cannot be null or empty"
            d["code"] = code
            error.append(d)

    return error

def convert_str_time(time):
    newtime = datetime.strptime(time, format)
    return newtime