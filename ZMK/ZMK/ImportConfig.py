"""
Purpose of this module is to be able to import a .json file
it will convert it to a python object
"""
__all__ = ["decode_zmk_config"]

import json as _json


def _decode_zmk_config_hook(obj: dict) -> any:
    """
    This function is planned to be used as a hook for json.loads
    """
    for key, element in obj.items():
        print(key, element)
    return obj


def decode_zmk_config(json_str: str) -> any:
    """
    This function will decode a json string from a file which should contain a zmk config into a zmk config object
    """
    return _json.loads(json_str, object_hook=_decode_zmk_config_hook)
