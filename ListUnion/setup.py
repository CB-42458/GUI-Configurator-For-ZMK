"""
Setup file for ListUnion
"""
from setuptools import setup, find_packages

setup(
    name='ListUnion',
    version='0.1',
    description='Library which merges two lists into one, without duplicates',
    packages=find_packages(include=['ListUnion', 'ListUnion.*']),
)
