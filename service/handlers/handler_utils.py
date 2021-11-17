from tornado.web import HTTPError

def parse_ids(*args):
    try:
        ids = [int(id) for id in args]
    except ValueError:
        raise HTTPError(400, "All IDs have to be numerical")
    if len(ids) == 1:
        return ids[0]
    return tuple(ids)
