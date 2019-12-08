def flatten_lists(items):
    result = []

    for item in items:
        if not item:
            continue
        if type(item) is list:
            for sub_item in flatten_lists(item):
                result.append(sub_item)
        else:
            result.append(item)

    return result


def sign(x):
    if x == 0:
        return 0
    return 1 if x > 0 else -1
