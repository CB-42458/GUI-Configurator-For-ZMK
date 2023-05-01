"""
Setup file for pykle_serial
"""
from setuptools import setup, find_packages

setup(
    name='pykle_serial',
    version='0.1',
    description='Library for parsing serialized data from keyboard layout editor',
    packages=find_packages(include=['pykle_serial', 'pykle_serial.*']),
)
