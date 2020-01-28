def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts] for i in range(wanted_parts)]


def swap(alist1, alist2, limit):
    for i in limit:
        alist1[i] = alist2[i], alist2[i] = alist1[i]
