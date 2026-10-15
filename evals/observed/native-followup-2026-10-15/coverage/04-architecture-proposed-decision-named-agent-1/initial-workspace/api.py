from application import submit_order
def post_order(body, caller):
    return submit_order(body["idempotency_key"], body["items"], caller)
