from numpy import allclose


def _compare(v1, v2) -> bool:
    if isinstance(v1, float) and isinstance(v2, float):
        return allclose(v1, v2)
    else:
        return v1 == v2


def compare_dict_values(current_dict: dict, other_dict: dict) -> dict:
    """
    Utility function for comparing the values of 2 dictionaries
    """
    differences = {}

    for key in set(other_dict.keys()).intersection(current_dict.keys()):
        if not _compare(current_dict[key], other_dict[key]):
            differences[key] = f"{current_dict[key]} != {other_dict[key]}"

    return differences
