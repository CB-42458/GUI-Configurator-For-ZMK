"""
Module for ZMK containing implementing Behaviours
"""
from __future__ import annotations

__all__ = ['AbstractBehaviour', 'KeyPress', 'MomentaryLayer', 'LayerTap', 'ToggleLayer', 'Transparent', 'NoneBehaviour',
           'Reset', 'BootloaderReset', 'Bluetooth', 'OutputSelection']

import typing
import abc

if typing.TYPE_CHECKING:
    from .KeyCodes import KeyCode, FunctionModifier, BluetoothKeyCode, OutputKeyCode
    from ListUnion import list_union

from .KeyCodes import KeyCode, FunctionModifier, BluetoothKeyCode, OutputKeyCode
from ListUnion import list_union


class AbstractBehaviour:
    """
    Class Behaviour will be an abstract class allowing for a specific behaviour and its properties to be implemented
    """

    @abc.abstractmethod
    def __init__(self):
        """
        each element in the list _properties will be of this structure:
        {'property_name': name,
         'data_types': [list of valid data types],
         'current_value': value,
         'data_validation': lambda expression}

        the 'data_validation' property is optional but is used when validation is required
        because on the creation of the object, the data type of property is set, so that error checking can be carried
        out.
        """
        self._properties: list = []

    def get_behaviour_config_properties(self) -> list:
        """
        Method will return a list of properties for the configuration

        @return: list of properties
        """
        return self._properties

    def set_config_property(self, property_name: str, value: any) -> None:
        """
        This method is used for all behaviours to set the value of the protected property '_properties'
        This method has standard error and type checking as each behaviour will have a different set of properties
        refer to __init__ for the structure of the array.

        @param property_name: name of the property to be set
        @param value: value to be set
        """
        property_found = False
        for index_dict, property_dict in enumerate(self._properties):
            # searches for the property in the list of properties
            if property_name == property_dict['property_name']:
                property_found = True  # this boolean is used as it would raise an error if there was no property found
                if type(value) not in property_dict['data_types']:
                    raise TypeError(
                        f"property '{property_name}' not in {property_dict['data_types']} so its not a valid datatype")
                if 'data_validation' in property_dict and not property_dict['data_validation'](value):
                    raise ValueError(
                        f"property '{property_name}' didn't pass data validation of {property_dict['data_validation']}")
                self._properties[index_dict]['current_value'] = value
                break
        # raises error if property not found
        if not property_found:
            raise KeyError(f"'{property_name}' not found in the properties of {self.__class__.__name__}")

    @abc.abstractmethod
    def build(self) -> dict:
        """
        Method will return strings as a dictionary containing the necessary bits of code at the right parts of the code
        to build the behaviour.
        """
        pass

    @abc.abstractmethod
    def __str__(self):
        pass

    def export(self) -> dict:
        """
        Method will return a dictionary containing the properties of the behaviour
        """
        properties_list = []
        for property_dict in self._properties:
            if 'export' in dir(property_dict['current_value']):
                properties_list.append({property_dict['property_name']: property_dict['current_value'].export()})
            else:
                properties_list.append({property_dict['property_name']: property_dict['current_value']})
        return {f"{self.__class__}": {'_properties': properties_list}}


class KeyPress(AbstractBehaviour):
    """
    Class KeyPress will be a child of Behaviour and will implement the behaviour of a key press
    """

    def __init__(self, binding: any = None):
        super().__init__()
        # creates the properties for this behaviour
        self._properties: list = [
            {'property_name': 'binding',
             'data_types'   : [KeyCode, FunctionModifier],
             'current_value': binding}
        ]

        self.set_config_property('binding', binding)

    def build(self) -> dict:
        """
        Refer to the documentation of the method 'build' in the parent class 'Behaviour'
        """
        if self._properties[0]['current_value'] is None:
            raise ValueError('the value for the behaviour was never set')

        binding_dict: [KeyCode, FunctionModifier] = self._properties[0]['current_value'].build()
        return {
            '.keymap': {
                'include': list_union(['behaviors.dtsi'], binding_dict['.keymap']['include']),
                'return' : f"&kp {binding_dict['.keymap']['return']}"
            }
        }

    def __str__(self):
        return f"KeyPress({self._properties[0]['current_value']})"


class MomentaryLayer(AbstractBehaviour):
    """
    Class MomentaryLayer will be a child of Behaviour and will implement the behaviour of a momentary layer
    """

    def __init__(self, layer: int = None):
        super().__init__()
        # creates the properties for this behaviour
        self._properties = [
            {'property_name': 'layer', 'data_types': [int], 'current_value': layer, 'data_validation': lambda x: x >= 0}
        ]
        self.set_config_property('layer', layer)

    def build(self) -> dict:
        """
        Refer to the documentation of the method 'build' in the parent class 'Behaviour'
        """
        if self._properties is None:
            raise ValueError('the value for the behaviour was never set')

        return {
            '.keymap': {
                'include': ['behaviors.dtsi'],
                'return' : f"&mo {self._properties[0]['current_value']}"
            }
        }

    def __str__(self):
        return f"MomentaryLayer({self._properties[0]['current_value']})"


class LayerTap(AbstractBehaviour):
    """
    Class LayerTap will be a child of Behaviour and will implement the behaviour of a 'layer tap'
    """

    def __init__(self, layer: int = None, binding: any = None):
        super().__init__()
        # creates the properties for this behaviour
        self._properties = [
            {'property_name': 'layer', 'data_types': [int], 'current_value': None, 'data_validation': lambda x: x >= 0},
            {'property_name': 'binding', 'data_types': [KeyCode, FunctionModifier], 'current_value': None}
        ]
        self.set_config_property('layer', layer)
        self.set_config_property('binding', binding)

    def build(self) -> dict:
        """
        Refer to the documentation of the method 'build' in the parent class 'Behaviour'
        """
        if self._properties is None:
            raise ValueError('the value for the behaviour was never set')

        binding_dict: dict = self._properties[1]['current_value'].build()
        return {
            '.keymap': {
                'include': list_union(['behaviors.dtsi'], binding_dict['.keymap']['include']),
                'return' : f"&lt {self._properties[0]['current_value']} {binding_dict['.keymap']['return']}"
            }
        }

    def __str__(self):
        return f"LayerTap({self._properties[0]['current_value']}, {self._properties[1]['current_value']})"


class ToggleLayer(AbstractBehaviour):
    """
    Class ToggleLayer will be a child of Behaviour and will implement the behaviour of a 'toggle layer'
    """

    def __init__(self, layer: int = None):
        super().__init__()
        # creates the properties for this behaviour
        self._properties = [
            {'property_name': 'layer', 'data_types': [int], 'current_value': layer, 'data_validation': lambda x: x >= 0}
        ]
        self.set_config_property('layer', layer)

    def build(self) -> dict:
        """
        Refer to the documentation of the method 'build' in the parent class 'Behaviour'
        """
        if self._properties is None:
            raise ValueError('the value for the behaviour was never set')

        return {
            '.keymap': {
                'include': ['behaviors.dtsi'],
                'return' : f"&tog {self._properties[0]['current_value']}"
            }
        }

    def __str__(self):
        return f"ToggleLayer({self._properties[0]['current_value']})"


class Transparent(AbstractBehaviour):
    """
    Class Transparent will be a child of Behaviour and will implement the behaviour of '&trans'
    """

    def __init__(self):
        super().__init__()
        # creates the properties for this behaviour
        self._properties = []

    def build(self) -> dict:
        """
        Refer to the documentation of the method 'build' in the parent class 'Behaviour'
        """
        return {
            '.keymap': {
                'include': ['behaviors.dtsi'],
                'return' : '&trans'
            }
        }

    def __str__(self):
        return f"Transparent()"


class NoneBehaviour(AbstractBehaviour):
    """
    Class NoneBehaviour will be a child of Behaviour and will implement the behaviour of '&none'
    """

    def __init__(self):
        super().__init__()
        # creates the properties for this behaviour
        self._properties = []

    def build(self) -> dict:
        """
        Refer to the documentation of the method 'build' in the parent class 'Behaviour'
        """
        return {
            '.keymap': {
                'include': ['behaviors.dtsi'],
                'return' : '&none'
            }
        }

    def __str__(self):
        return f"NoneBehaviour()"


class Reset(AbstractBehaviour):
    """
    Class Reset will be a child of Behaviour and will implement the behaviour of '&reset'
    """

    def __init__(self):
        super().__init__()
        # creates the properties for this behaviour
        self._properties = []

    def build(self) -> dict:
        """
        Refer to the documentation of the method 'build' in the parent class 'Behaviour'
        """
        return {
            '.keymap': {
                'include': ['behaviors.dtsi'],
                'return' : '&reset'
            }
        }

    def __str__(self):
        return f"Reset()"


class BootloaderReset(AbstractBehaviour):
    """
    Class BootloaderReset will be a child of Behaviour and will implement the behaviour of '&bootloader'
    """

    def __init__(self):
        super().__init__()
        # creates the properties for this behaviour
        self._properties = []

    def build(self) -> dict:
        """
        Refer to the documentation of the method 'build' in the parent class 'Behaviour'
        """
        return {
            '.keymap': {
                'include': ['behaviors.dtsi'],
                'return' : '&bootloader'
            }
        }

    def __str__(self):
        return f"BootloaderReset()"


class Bluetooth(AbstractBehaviour):
    """
    Class Bluetooth will be a child of Behaviour and will implement the behaviour of a '&bt'
    """

    def __init__(self, binding: BluetoothKeyCode = None):
        super().__init__()
        # creates the properties for this behaviour
        self._properties = [
            {'property_name': 'binding', 'data_types': [BluetoothKeyCode], 'current_value': None},
        ]
        self.set_config_property('binding', binding)

    def build(self) -> dict:
        """
        Refer to the documentation of the method 'build' in the parent class 'Behaviour'
        """
        if self._properties is None:
            raise ValueError('the value for the behaviour was never set')

        binding_dict: dict = self._properties[0]['current_value'].build()
        print(binding_dict)
        return {
            '.keymap': {
                'include': list_union(['behaviors.dtsi'], binding_dict['.keymap']['include']),
                'return' : f"&bt {binding_dict['.keymap']['return']}"
            }
        }

    def __str__(self):
        return f"Bluetooth({self._properties[0]['current_value']})"


class OutputSelection(AbstractBehaviour):
    """
    Class OutputSelection will be a child of Behaviour and will implement the behaviour of a 'output selection'
    """

    def __init__(self, binding: OutputKeyCode = None):
        super().__init__()
        # creates the properties for this behaviour
        self._properties = [
            {'property_name': 'binding', 'data_types': [OutputKeyCode], 'current_value': None},
        ]
        self.set_config_property('binding', binding)

    def build(self) -> dict:
        """
        Refer to the documentation of the method 'build' in the parent class 'Behaviour'
        """
        if self._properties is None:
            raise ValueError('the value for the behaviour was never set')

        binding_dict: dict = self._properties[0]['current_value'].build()
        return {
            '.keymap': {
                'include': list_union(['behaviors.dtsi'], binding_dict['.keymap']['include']),
                'return' : f"&out {binding_dict['.keymap']['return']}"
            }
        }

    def __str__(self):
        return f"OutputSelection({self._properties[0]['current_value']})"


# main tests the methods of the classes
if __name__ == '__main__':
    pass
