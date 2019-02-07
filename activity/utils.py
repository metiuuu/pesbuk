def check_mandatory_fields(dictionary, fields):
    for field in fields:
        if field not in dictionary or not dictionary[field]:
            return False
    return True
