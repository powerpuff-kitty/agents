OBJECTS = {"invoice-a": {"tenant": "alpha", "total": 10}, "invoice-b": {"tenant": "beta", "total": 99}}

def get_invoice(principal, object_id):
    if not principal.get("authenticated"):
        raise PermissionError("authentication required")
    return OBJECTS[object_id]
