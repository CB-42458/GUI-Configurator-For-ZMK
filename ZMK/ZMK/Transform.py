"""
This module houses the MatrixTransform class which is used to represent a matrix transform
"""
from __future__ import annotations

__all__ = ['RowCol', 'MatrixTransform']

from dataclasses import dataclass
import typing

from .CustomDataStructures import Array

if typing.TYPE_CHECKING:
    from . import Config


# noinspection PyMissingOrEmptyDocstring
@dataclass
class RowCol:
    """
    Class RowCol represents a row and a column
    """
    row: int
    """store for the row of a key"""
    col: int
    """store for the column of a key"""

    def __eq__(self, other: RowCol) -> bool:
        """
        Method to compare two RowCol objects
        """
        if not isinstance(other, RowCol):
            return False
        return self.row == other.row and self.col == other.col


class MatrixTransform:
    """
    Class MatrixTransform represents a matrix transform
    """

    def __init__(self):
        """
        The list will store None values if the key has not been set yet
        """
        self.__matrix: Array([None | RowCol]) = Array()

    def get_matrix(self) -> Array([None | RowCol]):
        """
        Getter for the matrix
        """
        return self.__matrix.copy()

    def add_key(self, row: int, col: int, index=None):
        """
        Method to add a key to the matrix
        """
        if not isinstance(row, int):
            raise TypeError(f"parameter 'row' of type {type(row)} is not an int")
        if not isinstance(col, int):
            raise TypeError(f"parameter 'col' of type {type(col)} is not an int")

        if not isinstance(index, int | None):
            raise TypeError(f"parameter 'index' of type {type(index)} is not an int or None")

        if index is None:
            self.__matrix.append(RowCol(row, col))
            return

        self.__matrix.insert(index, RowCol(row, col))

    def get_key(self, index: int) -> RowCol or None:
        """
        Method to get a key from the matrix
        """
        if not isinstance(index, int):
            raise TypeError(f"parameter 'index' of type {type(index)} is not an int")
        if not 0 <= index < len(self.__matrix):
            raise IndexError(f"index {index} is out of range")
        return self.__matrix[index]

    # noinspection PyUnusedLocal
    def build(self, zmk_config: Config.ZMKConfig) -> dict:
        """
        Method returns a dictionary which contains bits of code at the part of code in the files
        """
        if None in self.__matrix:
            raise ValueError("MatrixTransform is not complete")
        return {
            'matrix_transform': self.__matrix.__list__()
        }

    #
    def export(self) -> dict:
        """
        Method returns a dictionary which represents the matrix transform, so that it can be exported to a json file.
        """
        return {
            'matrix_transform': self.__matrix
        }

    #
    def __len__(self):
        """
        Length of the matrix
        """
        return len(self.__matrix)


if __name__ == '__main__':
    test_matrix_transform = MatrixTransform()
    test_matrix_transform.add_key(1, 2)
    print(test_matrix_transform.get_matrix())
