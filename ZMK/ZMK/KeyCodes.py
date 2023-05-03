"""
This module contains classes for the keycodes with private attributes that protect from overwriting.
"""
from __future__ import annotations

__all__ = ["AbstractJSONDictionary", "KeyCodesJSON", "FunctionModifiersJSON",
           'BluetoothKeyCodesJSON',
           'OutputKeyCodesAbstractJSON', 'KeyCode', 'FunctionModifier', 'BluetoothKeyCode', 'OutputKeyCode']

import abc
import json

from pkg_resources import resource_filename
from ListUnion import list_union


class AbstractJSONDictionary:
    """
    AbstractJSONDictionary is an abstract class which will encompasses the methods which all JSON dictionary
    classes will use
    """

    @abc.abstractmethod
    def __init__(self):
        self._dictionary = {}

    def __iter__(self):
        return iter(self._dictionary)

    def __getitem__(self, key) -> dict:
        if key not in self._dictionary:
            raise KeyError(f"key {key} is not in the dictionary")
        return self._dictionary[key]

    def __contains__(self, item):
        return item in self._dictionary


class KeyCodesJSON(AbstractJSONDictionary):
    """
    this class will act as a dictionary which is protected, as the JSON files are used frequently and otherwise the
    program would have to read the file several times
    """
    _dictionary = json.load(open(resource_filename(__name__, 'key_codes.json'), 'r', encoding='utf8'))

    def __init__(self):
        super().__init__()
        self._dictionary = KeyCodesJSON._dictionary


class FunctionModifiersJSON(AbstractJSONDictionary):
    """
    this class will act as a dictionary which is protected, as the JSON files are used frequently and otherwise the
    program would have to read the file several times
    """
    _dictionary = json.load(open(resource_filename(__name__, 'function_modifiers.json'), 'r', encoding='utf8'))

    def __init__(self):
        super().__init__()
        self._dictionary = FunctionModifiersJSON._dictionary


class BluetoothKeyCodesJSON(AbstractJSONDictionary):
    """
    this class will act as a dictionary which is protected, as the JSON files are used frequently and otherwise the
    program would have to read the file several times
    """
    _dictionary = json.load(open(resource_filename(__name__, 'bluetooth_keycodes.json'), 'r', encoding='utf8'))

    def __init__(self):
        super().__init__()
        self._dictionary = BluetoothKeyCodesJSON._dictionary


class OutputKeyCodesAbstractJSON(AbstractJSONDictionary):
    """
    this class will act as a dictionary which is protected, as the JSON files are used frequently and otherwise the
    program would have to read the file several times
    """
    _dictionary = json.load(open(resource_filename(__name__, 'output_keycodes.json'), 'r', encoding='utf8'))

    def __init__(self):
        super().__init__()
        self._dictionary = OutputKeyCodesAbstractJSON._dictionary


class AbstractCode:
    """
    AbstractCode is an abstract class which will function as a blueprint that will make sure all child classes have
    the correct methods
    """

    @abc.abstractmethod
    def __init__(self):
        self._name = None
        self._description = None
        self._context = None

    def get_name(self) -> str:
        """getter for the protected attribute _name"""
        return self._name

    def get_description(self) -> str:
        """getter for the protected attribute _description"""
        return self._description

    def get_context(self) -> str:
        """getter for the protected attribute _context"""
        return self._context

    @abc.abstractmethod
    def build(self) -> dict:
        """
        method will return a dictionary containing the necessary bits for the zmk firmware to build it
        """
        pass

    @abc.abstractmethod
    def __str__(self):
        pass

    def export(self) -> dict:
        """
        method will turn a dictionary in a format which is able to be serialised to JSON
        """
        return {f"{self.__class__}": {'_name': self._name}}


class AbstractCodeWithBinding(AbstractCode):
    """
    AbstractCodeWithBinding is an abstract class which will have a property attribute _binding which is a dictionary
    with the following structure:
    {'property_name': str,
     'data_types': list of classes,
     'current_value': value,
     'data_validation': lambda expression}
    'data_validation' is optional
    """

    @abc.abstractmethod
    def __init__(self):
        super().__init__()
        self._binding = {}

    def get_binding(self) -> dict:
        """
        getter for the protected attribute _binding
        """
        return self._binding

    def set_binding(self, value) -> None:
        """
        setter for the protected attribute _binding
        """
        # checks for the correct data type
        if type(value) not in self._binding['data_types']:
            raise TypeError(f"parameter 'value' expected {self._binding['data_types']} but received {type(value)}")
        # if there is data validation, and it is not passed then raise error
        if 'data_validation' in self._binding and not self._binding['data_validation'](value):
            raise ValueError(f"parameter 'value' failed data validation")

        self._binding['current_value'] = value

    def export(self, recursion: dict = None) -> dict:
        """
        method will turn a dictionary in a format which is able to be serialised to JSON
        """
        if recursion is None:
            return_dict = super().export()
            return_dict[f"{self.__class__}"]['_binding'] = self.export(recursion=self._binding)
            return return_dict
        if 'export' in dir(recursion['current_value']):
            return recursion['current_value'].export()
        return recursion['current_value']


class KeyCode(AbstractCode):
    """
    class Keycode is has protected attributes which ensures that the ZMK keycodes are not tampered with and thus will
    not cause errors on the build of the firmware.
    """

    def __init__(self, name: str):
        super().__init__()
        if type(name) is not str:
            raise TypeError(f"parameter 'name' expected {str} but received {type(name)}")
        if name not in KeyCodesJSON():
            raise KeyError(f"parameter 'name' expected to be from key_codes.json but received {name}")

        self._name = name
        self._description = KeyCodesJSON()[name]["description"]
        self._context = KeyCodesJSON()[name]["context"]

    def build(self) -> dict:
        """
        method will return a dictionary containing the necessary bits for the zmk firmware to build it
        """
        return {
            '.keymap': {
                'include': ['dt-bindings/zmk/keys.h'],
                'return' : self._name
            }
        }

    def __str__(self):
        return f"KeyCode('{self._name}')"


class FunctionModifier(AbstractCodeWithBinding):
    """
    Class FunctionModifier has protected attributes which ensures that its parameters are not tampered with and thus
    not cause errors on the build of the firmware.
    """

    def __init__(self, name: str, binding: any):
        super().__init__()
        self._binding = {
            'property_name': 'binding',
            'data_types'   : [FunctionModifier, KeyCode]
        }
        if type(name) is not str:
            raise TypeError(f"parameter 'name' expected {str} but received {type(name)}")
        if name not in FunctionModifiersJSON():
            raise KeyError("parameter 'name' required a valid name from function_modifiers.json")

        self._name: str = name
        self._description: str = FunctionModifiersJSON()[name]["description"]
        self._context: str = FunctionModifiersJSON()[name]["context"]
        self.set_binding(binding)

    def build(self) -> dict:
        """
        method will return a dictionary containing the necessary bits for the zmk firmware to build it
        """
        built_binding_dict = self._binding['current_value'].build()
        return {
            '.keymap': {
                'include': list_union(built_binding_dict['.keymap']['include'], ['dt-bindings/zmk/keys.h']),
                'return' : self._name.replace('xx', built_binding_dict['.keymap']['return'])
            }
        }

    def __str__(self):
        return f"FunctionModifier('{self._name}', {self._binding['current_value']})"


class BluetoothKeyCode(AbstractCodeWithBinding):
    """
    Class BluetoothKeyCode has protected attributes which ensures that its parameters are not tampered with and thus
    not cause errors on the build of the firmware.
    """

    def __init__(self, name: str, binding: any = None):
        super().__init__()
        self._binding = {
            'property_name'  : 'binding',
            'data_types'     : [int, type(None)],
            'data_validation': lambda value: (self._name == 'BT_SEL(xx)' and type(value) is int and 0 <= value) or (
                    name != 'BT_SEL(xx)' and value is None),
            'current_value'  : None
        }

        if type(name) is not str:
            raise TypeError(f"parameter 'name' expected {str} but received {type(name)}")
        if name not in BluetoothKeyCodesJSON():
            raise KeyError(f"parameter 'name' expected to be from bluetooth_key_codes.json but received {name}")

        self._name = name
        self._description = BluetoothKeyCodesJSON()[name]["description"]
        self._context = BluetoothKeyCodesJSON()[name]["context"]
        self.set_binding(binding)

    def build(self) -> dict:
        """
        method will return a dictionary containing the necessary bits for the zmk firmware to build it
        """
        return {
            '.keymap': {
                'include': ['dt-bindings/zmk/bt.h'],
                'return' : self._name.replace('(xx)', f" {self._binding['current_value']}")
            }
        }

    def __str__(self):
        return f"BluetoothKeyCode('{self._name}', {self._binding['current_value']})"


class OutputKeyCode(AbstractCode):
    """
    Class OutputKeyCode has protected attributes which ensures that its parameters are not tampered with and thus
    not cause errors on the build of the firmware.
    """

    def __init__(self, name: str):
        super().__init__()
        if type(name) is not str:
            raise TypeError(f"parameter 'name' expected {str} but received {type(name)}")
        if name not in OutputKeyCodesAbstractJSON():
            raise KeyError(f"parameter 'name' expected to be from output_key_codes.json but received {name}")

        self._name = name
        self._description = OutputKeyCodesAbstractJSON()[name]["description"]
        self._context = OutputKeyCodesAbstractJSON()[name]["context"]

    def build(self) -> dict:
        """
        method will return a dictionary containing the necessary bits for the zmk firmware to build it
        """
        return {
            '.keymap': {
                'include': ['dt-bindings/zmk/outputs.h'],
                'return' : self._name
            }
        }

    def __str__(self):
        return f"OutputKeyCode('{self._name}')"
