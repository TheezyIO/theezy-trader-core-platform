def validate_fields(fields, o):
    return all(field[0] in o and type(o[field[0]]) == field[1] for field in fields)
