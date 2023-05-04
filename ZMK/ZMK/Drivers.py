"""
Module for ZMK containing the parent class 'Driver' and its children.

@note: I only plan to implement one driver, but I need to do it in a way so that other drivers can be added. I think
"""
from __future__ import annotations

__all__ = ['AbstractDriver']

import abc
import typing

if typing.TYPE_CHECKING:
    from . import Config


class AbstractDriver:
    """
    Class Driver will store properties of a driver and possible properties that it can have alongside the methods to
    build it into the files
    """

    @abc.abstractmethod
    def __init__(self):
        """
        The _properties attribute is a list of dictionaries. Each dictionary will have the following structure:
        ```python
        {
            'name': (string) name of the property,
            'types': (list) list of types that the property can be,
            'value': (any) current value of the property
        }
        ```
        """
        self.__properties: list = []

    @abc.abstractmethod
    def check_property(self, zmk_config: Config.ZMKConfig, property_name: str, value: any = None) -> bool:
        """
        This method will check if the value is valid for the property

        @param zmk_config: ZMKConfig is required as it checks the config against this property
        @param property_name: name of the property to check
        @param value: value to check, if it is None then it will check the current value of the property
        @return: True if the config is valid, False otherwise.
        """

    def set_property(self, zmk_config: Config.ZMKConfig, property_name: str, value: any) -> None:
        """
        this method will pass the parameters to check_property to see if
        they are valid, if they are valid then it will be set

        @param zmk_config: ZMKConfig is required and passed onto check_property method so that it can check the config
        against the property
        @param property_name: name of the property to set
        @param value: value of the property to set
        """

        if self.check_property(zmk_config, property_name, value):
            for index, _property in enumerate(self.__properties):
                if _property['name'] == property_name:
                    self.__properties[index]['value'] = value
                    break

    def get_properties(self) -> list:
        """
        @return: list of dictionaries containing the properties
        """
        return self.__properties

    def get_property(self, property_name: str) -> dict:
        """
        @param property_name: name of the property to get
        @return: dictionary containing the property
        """
        for _property in self.__properties:
            if _property['name'] == property_name:
                return _property
        KeyError(f'Property {property_name} is not a property of this driver')

    @abc.abstractmethod
    def build(self, zmk_config: Config.ZMKConfig) -> dict:
        """Method will return a dictionary containing the necessary bits of code at the right parts of the code"""
        pass

    @abc.abstractmethod
    def export(self) -> dict:
        """
        this method will return a dictionary containing the values of the driver's
        properties so that it can be exported to a json file

        @return: dictionary containing the properties of the driver
        """
        return {
            'properties': self.__properties
        }

    @abc.abstractmethod
    def __str__(self):
        """
        @return: string representation of the driver
        """


class MatrixDriver(AbstractDriver):
    """
    Class MatrixDriver will store the properties to implement a matrix driver in ZMK
    """

    def __init__(self):
        """
        Refer to the AbstractDriver class for more information about the formatting of the properties.
        I have not added all the properties for the matrix driver as they are not needed, they are either optional
        config options or they are options which just complicate the process for my target end user.
        """
        super().__init__()
        self.__properties = [
            {'name': 'row-gpios', 'types': None, 'value': None},
            {'name': 'col-gpios', 'types': None, 'value': None},
            {'name': 'diode-direction', 'types': [str], 'value': None},
        ]

    def check_property(self, zmk_config: Config.ZMKConfig, property_name: str, value: any = None) -> bool:
        """
        refer to the AbstractDriver class for more information about this method
        """
        # aside from error checking to see if the types are correct

        pass
