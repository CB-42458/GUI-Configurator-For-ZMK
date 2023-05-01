"""
Setup File for the ZMK Package
"""
from setuptools import setup, find_packages

setup(
    name='ZMK',
    version='0.1',
    description='ZMK Python Package allows you to create a ZMK config using a Python interface.',
    packages=find_packages(include=['ZMK', 'ZMK.*']),
    include_package_data=True,
    install_requires=["ListUnion"],
    package_data={'ZMK': ['*.json']},
)
