_buffer = []


def capture(request_obj, response_obj):
    _buffer.clear()
    _buffer.append((request_obj, response_obj))


def pop_all():
    items = _buffer[:]
    _buffer.clear()
    return items
