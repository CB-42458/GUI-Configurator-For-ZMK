"""
Module is used to Export the ZMKConfig to a JSON file
"""
from __future__ import annotations

__all__ = ['export_config']

import json
import typing

if typing.TYPE_CHECKING:
    from . import Config


class ZMKJSONEncoder(json.JSONEncoder):
    """This class is used to encode the ZMKConfig to a JSON file"""

    def default(self, o: any) -> any:
        """
        Method is used to encode the ZMKConfig to a JSON file.

        @param o: object to encode
        @return: encoded object

        The object in question should be objects of the ZMK package which have an export method which converts the
        attributes of to a format which can be exported to a json file and then imported again
        """
        if 'export' in dir(o):
            return o.export()
        return super().default(o)


def export_config(config: Config.ZMKConfig, file: any) -> None:
    """
    Method is used to export the ZMKConfig to a JSON file
    @param config: ZMKConfig to export
    @param file: file object created by open()
    """
    export_dict = {
        '_config_name'           : config.get_config_name(),
        '_features'              : config.get_features(),
        '_mcu'                   : config.get_mcu(),
        '_default_config_options': config.get_default_config_options(),
        '_config_options'        : config.get_config_options(),
        '_driver'                : config.get_driver(),
        '_split_config_options'  : config.get_split_config_options(),
        '_behaviours'            : config.get_behaviours(),
        '_keymap'                : config.get_keymap()
    }
    """Dictionary containing the objects of the ZMK package for the custom JSONEncoder to encode"""
    json.dump(export_dict, file, cls=ZMKJSONEncoder, indent=4)
