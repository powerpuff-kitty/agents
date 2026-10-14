def quote(quantity, unit_price, discount_percent=0):
    return quantity * unit_price * (1 - discount_percent / 100)
