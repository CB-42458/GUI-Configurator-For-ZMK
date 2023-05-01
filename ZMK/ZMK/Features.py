"""
Module for ZMK containing the parent class 'Feature' and its children.
"""
from __future__ import annotations
__all__ = ['AbstractFeature']

class AbstractFeature:
    """
    Class Feature will be an abstract class allowing for a specific feature and its properties to be implemented
    """

    def __init__(self):
        pass

    def build_feature(self) -> dict:
        """
        Method will return strings as a dictionary containing the necessary bits of code at the right parts of the code
        to build the feature.
        """
        pass

    def get_feature_config_properties(self) -> list:
        """
        Method will return a list of properties for the configuration,
        each element in the list will be of this structure:
        {'property_name': name, 'data_type': data_type, 'current_value': 'name'}
        """

    def set_feature_config_property(self, property_name: str, value: any) -> None:
        """Method will set the configuration property"""
        pass
