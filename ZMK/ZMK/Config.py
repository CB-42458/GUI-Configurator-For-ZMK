"""
This module contains classes and functions which allow with given data to generate files within a directory structure
which will be pushed to GitHub that will leverage GitHub actions to build a firmware for a keyboard.

for the type hints in methods which are either not implemented or partially implemented "classmethod" is used to
represent a class as I couldn't think of a better way to do that.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict
from os import path

if TYPE_CHECKING:
    from . import Features, MCUs, Drivers, Behaviours, ConfigOptions, ExportConfig, Shields, \
        Transform, CustomDataStructures as CusDataStruc  # noqa: E402


def add_dependencies():
    """
    Function.
    """


from . import Features, MCUs, Drivers, Behaviours, ConfigOptions, ExportConfig, Shields, Transform, \
    CustomDataStructures as CusDataStruc  # noqa: E402


class ZMKConfig:
    """
    Class ZMKConfig is the main class will encapsulate all the data for a ZMK configuration.
    """

    # noinspection PyUnusedLocal
    def __init__(self, **kwargs):
        self.__config_name: str | None = None
        """Name of the keyboard configuration"""
        self.__config_id: str | None = None
        """ID of the keyboard configuration, used by ZMK to identify the keyboard"""
        self.__shield_directory: str | None = None
        """Directory of the shield used by the keyboard found in the app/boards/shields directory of the ZMK repo"""
        self.__working_directory: str | None = None
        """Directory where the configuration will be saved locally"""
        self.__features: list[Features.AbstractFeature] = []
        """Features that the keyboard will have, such as rotary encoder, RGB under-glow, etc."""
        self.__mcu: MCUs.AbstractMCU | None = None
        """MCU that the keyboard will use"""
        self.__default_config_options: list = []
        """Default configuration options that will be used by the keyboard, outputted in the .defconfig file"""
        self.__config_options: list = []
        """Configuration options that will be used by the keyboard, outputted in the .conf file"""
        self.__driver: Drivers.AbstractDriver | None = None
        """Driver that the keyboard will use such as a matrix driver, demux driver, etc."""
        self.__split_config: bool = False
        """Boolean value which represents if the keyboard is a split keyboard or not"""
        self.__split_config_options: TypedDict('__split_config_options', {'central': list, 'peripheral': list}) = \
            {'central': [], 'peripheral': []}
        """Configuration options for the respected halves of the split keyboard"""
        self.__behaviours: list[Behaviours.AbstractBehaviour] = []
        """List will store behaviors which are unique configurations of a behaviour such as a tap dance"""
        self.__keymap: CusDataStruc.Array = CusDataStruc.Array([None])
        """Array which will store behaviours for the keymap"""
        self.__transform: Transform.MatrixTransform | None = Transform.MatrixTransform()
        """Transform which is used to translate the physical layout of the keyboard to the logical layout"""

    def load_config(self, file_path: str) -> None:
        """
        Method used to load a configuration, not currently implemented.

        @param file_path: Path to the file containing the configuration loaded from a JSON file.
        """
        pass

    def save_config(self, file_path: str = None, overwrite: bool = False) -> None:
        """
        Method will save the configuration to a json file. If overwrite is not True and the file already exists then
        a FileExistsError will be raised.

        @param file_path: Path to the file where the configuration will be saved
        @param overwrite: If True then file it will overwrite
        """
        if path.isfile(file_path) and not overwrite:
            raise FileExistsError
        elif overwrite:
            ExportConfig.export_config(self, file_path)

    def set_config_name(self, name: str) -> None:
        """
        Method used to set the configuration name:

        @param name: Name of the configuration which is used to display to users
        """
        # TODO double check if this method requires a format check
        if not isinstance(name, str):
            raise TypeError(f"parameter 'name' of type {type(name)} is not a string")
        if Shields.is_name_taken(name):
            raise ValueError(f"parameter 'name' of value {name} is keyboard name that already exists")
        self.__config_name = name

    def get_config_name(self) -> str:
        """Getter for the configuration name"""
        return self.__config_name

    def set_config_id(self, config_id: str) -> None:
        """
        Setter for the config id

        @param config_id: ID of the configuration which is used by ZMK to identify the keyboard
        """
        # TODO add format checking to this method
        if not isinstance(config_id, str):
            raise TypeError(f"parameter 'config_id' of type {type(config_id)} is not a string")
        if Shields.is_id_taken(config_id):
            raise ValueError(f"parameter 'config_id' of value {config_id} is name id that is already taken")
        self.__config_id = config_id

    def get_config_id(self) -> str:
        """Getter for the config id"""
        return self.__config_id

    def set_shield_directory(self, shield_directory: str) -> None:
        """
        Setter for the shield directory

        @param shield_directory: Directory of the shield used by the keyboard found in the app/boards/shields directory
        """
        # TODO add format checking to this method
        if not isinstance(shield_directory, str):
            raise TypeError(f"parameter 'shield_directory' of type {type(shield_directory)} is not a string")
        if Shields.is_directory_taken(shield_directory):
            raise ValueError(f"parameter 'shield_directory' of value {shield_directory} is a directory that is already "
                             "taken")
        self.__shield_directory = shield_directory

    def get_shield_directory(self) -> str:
        """Getter for the shield directory"""
        return self.__shield_directory

    def set_working_directory(self, working_directory: str) -> None:
        """
        Setter for the working directory

        @param working_directory: Directory where the configuration will be saved locally
        """
        if not isinstance(working_directory, str):
            raise TypeError(f"parameter 'working_directory' of type {type(working_directory)} is not a string")
        if not path.isdir(working_directory):
            raise ValueError(f"parameter 'working_directory' of value {working_directory} either does not exist or "
                             "is not a directory")
        self.__working_directory = working_directory

    def get_working_directory(self) -> str:
        """Getter for the working directory"""
        return self.__working_directory

    def add_feature(self, feature: Features.AbstractFeature) -> None:
        """Method for adding a feature, currently not implemented"""
        pass

    def del_feature(self, feature: Features.AbstractFeature) -> None:
        """
        Method for deleting a feature, currently not implemented, but it will take the parameter and find a matching
        feature in the self.__features list and delete it"""
        pass

    def get_features(self) -> list:
        """Method for getting the features"""
        return self.__features

    def set_mcu(self, mcu: MCUs.AbstractMCU) -> None:
        """Method for setting the mcu"""
        if not isinstance(mcu, MCUs.AbstractMCU):
            raise TypeError(f"parameter 'mcu' of type {type(mcu)} is not an MCU")
        self.__mcu = mcu

    def get_mcu(self) -> MCUs.AbstractMCU:
        """
        Method for getting the MCU in the config, it might be a neat idea to make this a getattribute method so that can
        be accessed like an attribute"""
        return self.__mcu

    def set_driver(self, driver: Drivers.AbstractDriver) -> None:
        """Method for setting the driver"""
        self.__driver = driver

    def get_driver(self) -> Drivers.AbstractDriver:
        """Method for getting the driver"""
        return self.__driver

    def set_transform(self, transform: Transform.MatrixTransform) -> None:
        """
        Method for setting the transform
        for now the MatrixTransform is the only transform that is available which is why the type hints are not
        part of an abstract class
        """
        self.__transform = transform

    def get_transform(self) -> Transform.MatrixTransform:
        """
        Method for getting the transform:
        for now the MatrixTransform is the only transform that is available which is why the type hints are not
        part of an abstract class
        """
        return self.__transform

    def get_behaviours(self) -> list:
        """Method for getting the behaviours"""
        return self.__behaviours

    def set_keymap(self, keymap: CusDataStruc.Array) -> None:
        """
        Method for setting the keymap:

        @param keymap: List of behaviours which are used to define the keymap
        """
        for index, behaviour in enumerate(keymap):
            if not issubclass(behaviour, Behaviours.AbstractBehaviour) and behaviour is not None:
                raise TypeError(f"parameter 'keymap' at index {index} of type {type(behaviour)} is not a Behaviour")
            elif behaviour is not None:
                raise ValueError(f"parameter 'keymap' at index {index} of value {behaviour} is not a Behaviour "
                                 "or a NoneType")

        self.__keymap = keymap

    def get_keymap(self) -> CusDataStruc.Array:
        """
        Method for getting the keymap

        @return: List of behaviours which are used to define the keymap
        """
        return self.__keymap

    def modify_key_binding(self, index: int, key_binding: classmethod) -> None:
        """
        Method for modifying a key binding:

        @param index: Index of the behaviour in the keymap to be accessed
        @param key_binding: Behaviour which is modified in the keymap
        """
        self.__keymap[index] = key_binding

    def clear_key_binding(self, index: int) -> None:
        """
        Method for clearing a key binding:

        @param index: Index of the behaviour in the keymap to be cleared
        """
        self.__keymap[index] = None

    def add_default_config_option(self, option: ConfigOptions.AbstractConfigOption) -> None:
        """Method for adding a default config option, there is no error checking for this method yet."""
        self.__default_config_options.append(option)

    def change_default_config_option(self, option: ConfigOptions.AbstractConfigOption) -> None:
        """Method for changing a default config option"""
        self.__default_config_options.remove(option)
        self.__default_config_options.append(option)

    def del_default_config_option(self, option: ConfigOptions.AbstractConfigOption) -> None:
        """Method for deleting a default config option"""
        self.__default_config_options.remove(option)

    def get_default_config_options(self) -> list:
        """Method for getting the default config options"""
        return self.__default_config_options

    def add_config_option(self, option: ConfigOptions.AbstractConfigOption) -> None:
        """Method for adding a config option"""
        self.__config_options.append(option)

    def change_config_option(self, option: ConfigOptions.AbstractConfigOption) -> None:
        """Method for changing a config option"""
        self.__config_options.remove(option)
        self.__config_options.append(option)

    def del_config_option(self, option: ConfigOptions.AbstractConfigOption) -> None:
        """Method for deleting a config option"""
        self.__config_options.remove(option)

    def get_config_options(self) -> list:
        """Method for getting the config options"""
        return self.__config_options

    def split_config(self, enable_split_config: bool) -> None:
        """Method for setting the split config"""
        if not isinstance(enable_split_config, bool):
            raise TypeError(f"parameter 'enable_split_config' of type {type(enable_split_config)} is not a bool")
        self.__split_config = enable_split_config

    def is_split_config(self) -> bool:
        """Method for getting the split config:"""
        return self.__split_config

    def add_split_config_option(self, side: str, option: ConfigOptions.AbstractConfigOption) -> None:
        """
        Method for adding a split config option:

        @param side: String which is either 'Primary' or 'Secondary'
        @param option: ConfigOption which is added to the respected side
        """
        if side in self.__split_config_options.keys():
            # noinspection PyTypedDict
            self.__split_config_options[side].append(option)
        else:
            raise ValueError(
                f"side: {side} is not valid side. Valid sides {[key for key in self.__split_config_options]}")

    def del_split_config_option(self, side: str, option: classmethod) -> None:
        """
        Method for deleting a split config option:

        @param side: String which is either 'Primary' or 'Secondary'
        @param option: ConfigOption which is deleted from the respected side
        """
        if side in self.__split_config_options:
            # noinspection PyTypedDict
            self.__split_config_options[side].remove(option)
        else:
            raise ValueError(
                f"side: {side} is not valid side. Valid sides {[key for key in self.__split_config_options]}")

    def get_split_config_options(self) -> dict:
        """Method for getting the split config options"""
        return self.__split_config_options

    def check_config(self) -> bool:
        """
        Method for checking the config, not implemented yet, but it will return a boolean value of True if the config is
        okay according to the checks carried out.
        """
        pass

    def build_config(self) -> None:
        """
        Method for building the ZMK config, not yet implemented, but it will create the files for which is pushed to
        GitHub and GitHub Actions compiles the firmware
        """
        pass

    def clear_key_data(self) -> None:
        """
        Method is called when there is a required change to the keymap and removes all the key data for the keymap,
        behaviours, transform and driver. the type of driver and transform will be kept.
        """
        self.__keymap = []
        self.__behaviours = []
        self.__driver = self.__driver.__class__()
        self.__transform = self.__transform.__class__()
