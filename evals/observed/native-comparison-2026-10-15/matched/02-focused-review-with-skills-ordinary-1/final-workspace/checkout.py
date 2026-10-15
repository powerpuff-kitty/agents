from pricing import quote
from display import dollars
def checkout():
    return dollars(quote(2, 50, discount_percent=10))
