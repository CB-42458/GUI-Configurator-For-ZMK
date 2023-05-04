# noinspection SpellCheckingInspection
"""
Purpose of this program is to store a list of all the existing shields in the ZMK repository
So that the Package can check if the name set by the user is already taken, this is to avoid
conflicts with the shields already in the ZMK repository. as there will be conflicts if with
the files that are already in the ZMK repository.

module will contain a list of all the shields in the ZKM repository, I create a separate module for this
because it is possible to implement a user can select a shield from a list of shields that are already
in the ZMK repository. I will not be implementing this, but it could be a possibility in the future.

**Example List:**
```python
shields = [
    {"directory_name": "splitkb_aurora_lily58",
     "name": "splitkb.com Aurora Lily58",
     "id": "splitkb_aurora_lily58" },
    {"directory_name": "two_percent_milk",
     "name": "2% Milk",
     "id": "two_percent_milk" }
]
```
"""
__all__ = ['get_shields', 'is_name_taken', 'is_id_taken', 'is_directory_taken']

from pkg_resources import resource_filename

__shields = []

if not __shields:
    import json

    with open(resource_filename(__name__, 'shields.json'), "r") as file:
        __shields = json.load(file)


def get_shields() -> list:
    """Getter for the shields"""
    return __shields.copy()


def __taken(key: str, value: str) -> bool:
    """Checks if the value is already taken"""
    if not isinstance(value, str):
        raise TypeError(f"parameter 'value' of type {type(value)} is not a string")

    for shield in __shields:
        if shield[key] == value:
            return True

    return False


def is_name_taken(name: str) -> bool:
    """Checks if the name is already taken"""
    return __taken("name", name)


def is_id_taken(shield_id: str) -> bool:
    """Checks if the id is already taken"""
    return __taken("id", shield_id)


def is_directory_taken(directory: str) -> bool:
    """Checks if the directory name is already taken"""
    return __taken("directory_name", directory)
