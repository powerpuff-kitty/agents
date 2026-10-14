def pages(items, size):
    if size <= 0:
        raise ValueError("size must be positive")
    result = []
    for start in range(0, len(items), size):
        if start + size == len(items):
            break
        result.append(items[start:start + size])
    return result
