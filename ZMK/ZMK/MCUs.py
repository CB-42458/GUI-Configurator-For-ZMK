"""
Module for ZMK containing the parent class '' and its children.
"""
from __future__ import annotations

__all__ = ['ProMicroInterconnect', 'NiceNanoV2']

import abc
import typing

if typing.TYPE_CHECKING:
    from . import Config


class AbstractInterconnect:
    """
    Purpose of this class is to act as an abstract class which will define the interface for all other interconnects
    because as the ZMK package will only be able to create custom firmwares for shields that are not part of the ZMK
    Firmware. So most of the Micro controllers use a command interconnect between the PCB of the shield and the PCB of
    the MCU. For example one such interconnect is the arduino pro micro, now the arduino pro micro does not support the
    ZMK firmware, but it is used in a lot of keyboard shields therefore it makes sense to make an MCU which has a
    compatible pinout.

    not sure if all the methods will be needed, but I'll add them just incase
    """

    @abc.abstractmethod
    def __init__(self):
        """
        the gpio map could have been implemented as a two-dimensional array, but this will be accessed the same and at
        glance is more readable. the elements of each key in the dictionary are an array strings which equate the name
        of the pins on the MCU the keys are what are used in the files coded but this will nice to comprehend for the
        end user.
        """
        self.__gpio_map = {}

    def get_gpio_map(self) -> dict:
        """
        Getter for the gpio map
        """
        return self.__gpio_map.copy()

    def get_gpio_names(self) -> list:
        """
        Gets the names of the all the gpio, I see this to be useful for when the end user would want to select a pin the
        GUI will be able to retrieve this list and display it to the user to select.
        """
        return_names = []
        for pin_names in self.__gpio_map.values():
            return_names += pin_names
        return return_names

    def get_gpio_pin_name(self, pin_number: int) -> list:
        # noinspection GrazieInspection
        """
        Gets the get the names for a pin given the pin number

        @param pin_number: the pin number to get the names for
        """
        # error checking
        if not isinstance(pin_number, int):
            raise TypeError(f"parameter 'pin_number' of type {type(pin_number)} is not an integer")

        # if the error checking is done
        if pin_number in self.__gpio_map:
            return self.__gpio_map[pin_number]

        raise KeyError(f"parameter 'pin_number' of value '{pin_number}' not found in the available gpio")

    def get_gpio_pin_number(self, pin_name: str) -> int:
        """
        gets the pin given a string

        @param pin_name: the pin name to get the number for
        """
        # error checking
        if not isinstance(pin_name, str):
            raise TypeError(f"parameter 'pin_name' of type {type(pin_name)} is not a string")

        # if the error checking is done
        for pin_number, pin_names in self.__gpio_map.items():
            if pin_name in pin_names:
                return pin_number

        # if the pin name was not in the list of available gpio
        raise KeyError(f"parameter 'pin_name' of value '{pin_name}' not found in the available gpio")


class ProMicroInterconnect(AbstractInterconnect):
    """
    Class for the arduino pro micro interconnect
    """

    def __init__(self):
        super().__init__()
        self.__gpio_map = {
            0 : ['D0'],
            1 : ['D1'],
            2 : ['D2'],
            3 : ['D3'],
            4 : ['D4', 'A6'],
            5 : ['D5'],
            6 : ['D6', 'A7'],
            7 : ['D7'],
            8 : ['D8', 'A8'],
            9 : ['D9', 'A9'],
            10: ['D10', 'A10'],
            16: ['D16'],
            14: ['D14'],
            15: ['D15'],
            18: ['D18', 'A0'],
            19: ['D19', 'A1'],
            20: ['D20', 'A2'],
            21: ['D21', 'A3']
        }


class AbstractMCU:
    """
    This class represents an abstract class
    """

    def __init__(self):
        self.__interconnect: [AbstractInterconnect, None] = None

    def get_interconnect(self) -> AbstractInterconnect:
        """Getter for the interconnect"""
        return self.__interconnect

    @abc.abstractmethod
    def check_config(self, config: Config.ZMKConfig) -> bool:
        """Check method which checks if the config is compatible with the MCU"""
        # error checking
        if not isinstance(config, Config.ZMKConfig):
            raise TypeError(f"parameter 'config' of type {type(config)} is not a ZMKConfig")

        # if the error checking is done
        return True

    @abc.abstractmethod
    def build(self, zmk_config: Config.ZMKConfig) -> dict:
        """Method returns a dictionary which contains bits of code at the part of code"""
        return {}

    @abc.abstractmethod
    def export(self) -> str:
        """Method returns a string which represents the MCU, so that it can be exported to a json file."""
        return ""

    @abc.abstractmethod
    def __str__(self):
        """String representation of the MCU meant to be used for terminal output"""
        return ""


class NiceNanoV2(AbstractMCU):
    """
    Class for the nice nano v2
    """

    def __init__(self):
        super().__init__()
        self.__interconnect = ProMicroInterconnect()

    def check_config(self, config: Config.ZMKConfig) -> bool:
        """Check method which checks if the config is compatible with the MCU"""
        # TODO: implement the error checking on this method if needed
        # error checking
        if not isinstance(config, Config.ZMKConfig):
            raise TypeError(f"parameter 'config' of type {type(config)} is not a ZMKConfig")

        # if the error checking is done
        return True

    def build(self, zmk_config: Config.ZMKConfig) -> dict:
        """Method returns a dictionary which contains bits of code at the part of code"""
        return {
            'keyboard.zmk.yml': {'requires': 'nice_nano_v2'},
            'build.yaml'      : {'board': 'nice_nano_v2'}
        }

    def export(self) -> str:
        """Method returns a string which represents the MCU, so that it can be exported to a json file."""
        return "NiceNanoV2"

    def __str__(self):
        """String representation of the MCU meant to be used for terminal output"""
        return "NiceNanoV2"
