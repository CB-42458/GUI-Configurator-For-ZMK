"""
Module for ZMK containing the parent class 'AbstractConfigOption' and its subclasses.
"""
from __future__ import annotations

__all__ = ['AbstractConfigOption', 'ZMK_KEYBOARD_NAME', 'ZMK_HID_CONSUMER_REPORT_SIZE', 'BT_MAX_CONN', 'BT_MAX_PAIRED',
           'ZMK_SPLIT', 'ZMK_SPLIT_ROLE_CENTRAL']

import typing
import abc

if typing.TYPE_CHECKING:
    from . import Config


class AbstractConfigOption:
    """
    Class ConfigOption is an abstract class that will store methods and attributes that will form a common interface
    for all config options.
    """

    # noinspection PyUnusedLocal
    @abc.abstractmethod
    def __init__(self, zmk_config: Config.ZMKConfig):
        """
        @param zmk_config: the ZMKConfig object is passed into so that it can be passed into the check_config_property
        method can check the value of the property against the config.
        
        `self.__config_option` is a dictionary containing the properties of the attribute. it will have this structure:
        ```python
        {'name' : (string) name of the property,
         'types': (list) list of types the property can be,
         'value': (any) current value of the property }
        ```
        
        """
        self.__config_option: dict = {
            'name' : '',
            'types': [],
            'value': None
        }

    @abc.abstractmethod
    def check_config_property(self, zmk_config: Config.ZMKConfig, value: any = None) -> bool:
        """
        Method will check the value of the property against the config. This is an abstract method because the error
        checking is more intricate that other modules such as KeyCodes.py or Behaviors.py.

        @param zmk_config: the ZMKConfig is passed into so that it can be passed into the check_config_property
        method can check the value of the property against the config.
        @param value: value passed into to check against the config. if value is None then it will check the current
        value of the property against the config.
        """
        pass

    def set_config_property(self, zmk_config: Config.ZMKConfig, value: any) -> None:
        """
        Method will set the configuration property.

        @param zmk_config: The ZMKConfig object is passed into so that it can be passed into the check_config_property
        method can check the value of the property against the config.
        @param value: value passed into the method which will set the attribute.
        """
        if self.check_config_property(zmk_config, value):
            self.__config_option['value'] = value

    def get_config_property(self) -> dict:
        """Getter for the configuration property."""
        return self.__config_option

    @abc.abstractmethod
    def build(self, zmk_config: Config.ZMKConfig) -> dict:
        """
        Method will return a dictionary containing the necessary bits of code at the right parts of the code

        @param zmk_config: The Config.ZMKConfig object is passed into method so
        that the config option can know which config file it belongs to.
        """

    def __str__(self) -> str:
        """Method will return a string which is used to represent the class in the output of a console"""
        return f'{self.__config_option["name"]}={self.__config_option["value"]}'

    def export(self) -> dict:
        """Method will return a dictionary containing the properties of the config options so that it can be exported to
        a json file."""
        return {f"{self.__class__}": self.__config_option['value']}


# General Config Options ===============================================================================================
"""
I did not deem it necessary to add the following config options because they are not imperative to the functionality of
the keyboard. They are extra config options that could be added in the future because of my implementation of the
AbstractConfigOption class

Goto https://zmk.dev/docs/config/system to see more information about the following config options:
- ZMK_SETTINGS_SAVE_DEBOUNCE
- ZMK_WPM
- HEAP_MEM_POOL_SIZE
- ZMK_BATTERY_REPORT_INTERVAL 
"""


class ZMK_KEYBOARD_NAME(AbstractConfigOption):
    """
    Class ZMK_KEYBOARD_NAME is a class which will represent the config option CONFIG_ZMK_KEYBOARD_NAME. refer to the
    __init__ know more about the attribute of this config option.
    """

    def __init__(self, zmk_config: Config.ZMKConfig, value: str = None):
        """
        refer to AbstractConfigOption __init__ for information about the purpose of the parameters.

        The Value of this config option is a string which will be the name of the keyboard. there is no default value
        and the value must be a string of length no more than 16 characters.
        """
        self.__config_option = {
            'name' : 'ZMK_KEYBOARD_NAME',
            'types': [str],
            'value': None
        }

        self.set_config_property(zmk_config, value)

    def check_config_property(self, zmk_config: Config.ZMKConfig, value: any = None) -> bool:
        """
        refer to AbstractConfigOption check_config_property for information about the purpose of the method and the
        parameters.

        The value of this config option must be a string of length no more than 16 characters.
        """

        # TODO check if this config option already exists in the config and if it does raise an error

        if value is None:
            value = self.__config_option['value']

        if not isinstance(value, str):
            return False

        if len(value) > 16:
            return False

        return True

    def build(self, zmk_config: Config.ZMKConfig) -> dict:
        """
        refer to AbstractConfigOption build for information about the purpose of the method and the parameters.
        """
        # TODO implement this method so that it can figure out which config file it belongs to and return the
        #   appropriate dictionary

        return {}


# HID Config Options ===================================================================================================
"""
I did not deem it necessary to add the following config options because they are not imperative to the functionality of
the keyboard. They are extra config options that could be added in the future because of my implementation of the
AbstractConfigOption class.

Goto https://zmk.dev/docs/config/system to see more information about the following config options:
- ZMK_HID_CONSUMER_REPORT_USAGES_FULL
- ZMK_HID_CONSUMER_REPORT_USAGES_BASIC
"""


class ZMK_HID_CONSUMER_REPORT_SIZE(AbstractConfigOption):
    """
    Class ZMK_HID_CONSUMER_REPORT_SIZE is a class which will represent the config option ZMK_HID_CONSUMER_REPORT_SIZE.
    refer to the __init__ know more about the attribute of this config option.
    """

    def __init__(self, zmk_config: Config.ZMKConfig, value: int = None):
        """
        refer to AbstractConfigOption __init__ for information about the purpose of the parameters.

        The Value of this config option is an integer which will correspond to the amount of consumer keys
        simultaneously reportable. The default value is 6
        """
        self.__config_option = {
            'name' : 'ZMK_HID_CONSUMER_REPORT_SIZE',
            'types': [int],
            'value': None
        }

        self.set_config_property(zmk_config, value)

    def check_config_property(self, zmk_config: Config.ZMKConfig, value: any = None) -> bool:
        # noinspection SpellCheckingInspection
        """
        refer to AbstractConfigOption check_config_property for information about the purpose of the method and the
        parameters.

        The value of this config option must be an integer, the default value is 6. if this value is set then exactly
        zero or one of the following config options may be set to y:
        - ZMK_HID_REPORT_TYPE_HKNO: Enable ZMK_HID_CONSUMER_REPORT_SIZE key roll over
        - ZMK_HID_REPORT_TYPE_NKRO: Enable full N-key rollover
        """

        # TODO check if this config option already exists in the config and if it does raise an error

        if value is None:
            value = self.__config_option['value']

        if not isinstance(value, int):
            return False

        return True

    def build(self, zmk_config: Config.ZMKConfig) -> dict:
        """
        refer to AbstractConfigOption build for information about the purpose of the method and the parameters.
        """
        return {
            '.conf': f'CONFIG_{self.__config_option["name"]}={self.__config_option["value"]}'
        }


# Bluetooth Config Options =============================================================================================
"""
I did not deem it necessary to add the following config options because they are not imperative to the functionality of
the keyboard. They are extra config options that could be added in the future because of my implementation of the
AbstractConfigOption class.

Goto https://zmk.dev/docs/config/system to see more information about the following config options:
- BT
- ZMK_BLE
- ZMK_BLUE_CLEAR_ALL_BONDS_ON_START
- ZMK_BLE_CONSUMER_REPORT_QUEUE_SIZE
- ZMK_BLE_KEYBOARD_REPORT_QUEUE_SIZE
- ZMK_BLE_INIT_PRIORITY
- ZMK_BLE_THREAD_PRIORITY
- ZMK_BLE_THREAD_STACK_SIZE
- ZMK_BLE_PASSKEY_ENTRY
"""


class BT_MAX_CONN(AbstractConfigOption):
    """
    Class BT_MAX_CONN is a class which will represent the config option BT_MAX_CONN. refer to the __init__ know more
    about the attribute of this config option.
    """

    def __init__(self, zmk_config: Config.ZMKConfig, value: int = None):
        """
        refer to AbstractConfigOption __init__ for information about the purpose of the parameters.

        The value of this config option is an integer which corresponds to the maximum number of simultaneous Bluetooth
        connections. The default value is 5.
        this config option and BT_MAX_PAIRED should be set to the same value. On a split keyboard, these values should
        only be set on the central half and must be set to one greater than the desired number bluetooth profiles.
        therefor in split config the minimum value for this config option is 2.
        """
        self.__config_option = {
            'name' : 'BT_MAX_CONN',
            'types': [int],
            'value': None
        }

        self.set_config_property(zmk_config, value)

    def check_config_property(self, zmk_config: Config.ZMKConfig, value: any = None) -> bool:
        """
        refer to AbstractConfigOption check_config_property for information about the purpose of the method and the
        parameters.
        """

        # TODO check if this config option already exists in the config and if it does raise an error

        if value is None:
            value = self.__config_option['value']

        if not isinstance(value, int):
            return False

        return True

    def build(self, zmk_config: Config.ZMKConfig) -> dict:
        """refer to AbstractConfigOption build for information about the purpose of the method and the parameters."""
        # TODO implement this method so that it can figure out which config file it belongs to and return the
        #   appropriate dictionary
        return {
            '.conf': f'CONFIG_{self.__config_option["name"]}={self.__config_option["value"]}'
        }


class BT_MAX_PAIRED(AbstractConfigOption):
    """
    Class BT_MAX_PAIRED is a class which will represent the config option BT_MAX_PAIRED. refer to the __init__ know more
    about the attribute of this config option.
    """

    def __init__(self, zmk_config: Config.ZMKConfig, value: int = None):
        """
        refer to AbstractConfigOption __init__ for information about the purpose of the parameters.

        The value of this config option is an integer which corresponds to the maximum number of paired Bluetooth
        Connections. The default value is 5.
        this config option and BT_MAX_CONN should be set to the same value. On a split keyboard, these values should
        only be set on the central half and must be set to one greater than the desired number bluetooth profiles.
        therefor in split config the minimum value for this config option is 2.
        """
        self.__config_option = {
            'name' : 'BT_MAX_PAIRED',
            'types': [int],
            'value': None
        }

        self.set_config_property(zmk_config, value)

    def check_config_property(self, zmk_config: Config.ZMKConfig, value: any = None) -> bool:
        """
        refer to AbstractConfigOption check_config_property for information about the purpose of the method and the
        parameters.

        The value of this config option should have the same value as the value of the config option BT_MAX_CONN.
        if it is a split config then the value of this config option should be how many simultaneous bluetooth
        connections are desired plus one. therefore the minimum value for this config option is 2.
        """

        # TODO check if this config option already exists in the config and if it does raise an error

        if value is None:
            value = self.__config_option['value']

        if not isinstance(value, int):
            return False

        return True

    def build(self, zmk_config: Config.ZMKConfig) -> dict:
        """refer to AbstractConfigOption build for information about the purpose of the method and the parameters."""
        # TODO implement this method so that is can figure out which config file it belongs to and return the
        #   appropriate dictionary
        return {
            '.conf': f'CONFIG_{self.__config_option["name"]}={self.__config_option["value"]}'
        }


# Split Keyboard Config Options =======================================================================================

"""
I did not deem it necessary to add the following config options because they are not imperative to the functionality of
the keyboard. They are extra config options that could be added in the future because of my implementation of the
AbstractConfigOption class.

Goto https://zmk.dev/docs/config/system to see more information about the following config options:
 - ZMK_SPLIT_BLE
 - ZMK_SPLIT_BLE_CENTRAL_POSITION_QUEUE_SIZE
 - ZMK_BLE_SPLIT_CENTRAL_SPLIT_RUN_STACK_SIZE
 - ZMK_BLE_SPLIT_CENTRAL_SPLIT_RUN_QUEUE_SIZE
 - ZMK_SPLIT_BLE_PERIPHERAL_STACK_SIZE
 - ZMK_SPLIT_BLE_PERIPHERAL_PRIORITY
 - ZMK_SPLIT_BLE_PERIPHERAL_POSITION_QUEUE_SIZE
"""


class ZMK_SPLIT(AbstractConfigOption):
    """
    Class ZMK_SPLIT is a class which will represent the config option ZMK_SPLIT. refer to the __init__ know more
    about the attribute of this config option.
    """

    def __init__(self, zmk_config: Config.ZMKConfig, value: bool = None):
        """
        refer to AbstractConfigOption __init__ for information about the purpose of the parameters.

        The value of this config option is a boolean which corresponds to whether or not the keyboard is a split
        keyboard. The default value is False.
        """
        self.__config_option = {
            'name' : 'ZMK_SPLIT',
            'types': [bool],
            'value': None
        }

        self.set_config_property(zmk_config, value)

    def check_config_property(self, zmk_config: Config.ZMKConfig, value: any = None) -> bool:
        """
        refer to AbstractConfigOption check_config_property for information about the purpose of the method and the
        parameters.

        The value of this config option must be a boolean, the default value is False. this config option must be set
        on both halves of the keyboard.
        """

        # TODO check if this config option already exists in the config and if it does raise an error

        if value is None:
            value = self.__config_option['value']

        if not isinstance(value, bool):
            return False

        return True

    def build(self, zmk_config: Config.ZMKConfig) -> dict:
        """refer to AbstractConfigOption build for information about the purpose of the method and the parameters."""
        # TODO implement this method so that is can figure out which config file it belongs to and return the
        #   appropriate dictionary
        return {}


class ZMK_SPLIT_ROLE_CENTRAL(AbstractConfigOption):
    """
    Class ZMK_SPLIT_ROLE_CENTRAL is a class which will represent the config option ZMK_SPLIT_ROLE_CENTRAL. refer to the
    __init__ know more about the attribute of this config option.
    """

    def __init__(self, zmk_config: Config.ZMKConfig, value: bool = None):
        """
        refer to AbstractConfigOption __init__ for information about the purpose of the parameters.

        The value of this config option is a boolean which corresponds to whether or not a particular half of the
        keyboard is the central half. there can only be one central half. other properties also require this property
        if the keyboard is a split keyboard. for example encoders must be on the central half. because as of this time
        encoders are only supported on the central half.
        """
        self.__config_option = {
            'name' : 'ZMK_SPLIT_ROLE_CENTRAL',
            'types': [bool],
            'value': None
        }

        self.set_config_property(zmk_config, value)

    def check_config_property(self, zmk_config: Config.ZMKConfig, value: any = None) -> bool:
        """
        refer to AbstractConfigOption check_config_property for information about the purpose of the method and the
        parameters.

        The value of this config option must be a boolean, the default value is False. this config option must be set
        on both halves of the keyboard.
        """

        # TODO check if this config option already exists in the config and if it does raise an error

        if value is None:
            value = self.__config_option['value']

        if not isinstance(value, bool):
            return False

        return True

    def build(self, zmk_config: Config.ZMKConfig) -> dict:
        """refer to AbstractConfigOption build for information about the purpose of the method and the parameters."""
        # TODO implement this method so that is can figure out which config file it belongs to and return the
        #   appropriate dictionary
        return {}
