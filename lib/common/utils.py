def is_nestable_type(t):
    return t in [list, dict]

def validate_all_fields(fields, o):
    return all(field[0] in o and type(o[field[0]]) == field[1] and (len(field) == 2 or not is_nestable_type(field[1]) or validate_all_fields(field[2], o[field[0]])) for field in fields)

def validate_any_field(fields, o):
    return any(field[0] in o and type(o[field[0]]) == field[1] and (len(field) == 2 or not is_nestable_type(field[1]) or validate_any_field(field[2], o[field[0]])) for field in fields)

transaction_types = {
    'PURCHASE': 1,
    'CONTRIBUTION': 2,
    'DEPOSIT': 3,
    'RETURN': 4,
    'SALE': 5,
    'WITHDRAWAL': 6
}

def get_transaction_type_id(name):
    if name not in transaction_types:
        raise ValueError(f"Transaction type '{name}' not found!")
    return transaction_types.get(name)