def is_nestable_type(t):
    return t in [list, dict]

def validate_all_fields(fields, o):
    return all(field[0] in o and type(o[field[0]]) == field[1] and (len(field) == 2 or not is_nestable_type(field[1]) or validate_all_fields(field[2], o[field[0]])) for field in fields)

def validate_any_field(fields, o):
    return any(field[0] in o and type(o[field[0]]) == field[1] and (len(field) == 2 or not is_nestable_type(field[1]) or validate_any_field(field[2], o[field[0]])) for field in fields)
