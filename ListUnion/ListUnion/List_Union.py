"""
This file house the function for the package ListUnion
"""


def list_union(list_a: list, list_b: list):
    """
    This function creates a union of two lists. Assuming there are no duplicates in list_a and no duplicates in list_b.
    When the two lists are combined there will be no duplicates in the new list.
    """
    for element in list_b:
        if element not in list_a:
            list_a.append(element)
    return list_a
