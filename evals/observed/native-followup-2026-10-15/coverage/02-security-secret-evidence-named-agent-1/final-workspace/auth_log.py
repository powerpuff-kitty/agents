import logging

def authenticate(headers):
    logging.info("request authorization=%s", headers.get("Authorization"))
    return bool(headers.get("Authorization"))
