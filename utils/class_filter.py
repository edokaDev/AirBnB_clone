"""Class filter module."""
import re


def class_filter(all_obj, class_name):
    """Class Object Filter.

    Filters @all_obj by @class_name.

    Args:
        - @all_obj: dict - dictionary containing all objects of all classes.
        - @class_name: string - Class name to filter
    Return:
        - New Dictionary with filtered objects.
    """
    regex = re.compile(rf"^({class_name}).")
    filtered_dict = {
        key: value for key, value in all_obj.items()
        if re.search(regex, key)
    }
    return filtered_dict
