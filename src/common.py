class InvalidAction(Exception):
    pass


class InvalidState(Exception):
    pass


def find(entry, list):
    for item in list:
        if item[0] == entry:
            return item
    return None


def state_size(graph):
    return len(graph)
