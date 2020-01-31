import random

from genetic_algo.main import args


def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts] for i in range(wanted_parts)]


def swap(alist1, alist2, limit):
    """
    Swap elements of a list until the limit
    :param alist1: the first list
    :param alist2: the second list
    :param limit: the limit ( < len(alist1))
    :return:
    """
    for i in len(limit):
        alist1[i] = alist2[i], alist2[i] = alist1[i]


def mutate(nb, min_range, max_range, deviation):
    """
    Mutate one element
    :param nb: the number to mutate
    :param min_range: the lower bond
    :param max_range: the upper bond
    :param deviation: the max deviation
    :return: the mutated number
    """
    m_range = abs(max_range - min_range)
    return random.uniform(nb - m_range * deviation, nb + m_range * deviation)


def mutate_list(liste):
    """
    Mutate every element of the list
    :param liste: [( , ), ( , )] (list of tuple)
    :return: the mutated list
    """
    return_list = []
    for gene in liste:
        return_list.append((mutate(gene[0], args["weight_min"], args["weight_max"], args["mutation_deviation"]),
                            mutate(gene[1], args["bias_min"], args["bias_max"], args["mutation_deviation"])))

    return return_list
