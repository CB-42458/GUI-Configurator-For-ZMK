"""
stores functions which are used in the application, when it makes the code more readable.
"""
from __future__ import annotations

__all__ = ["add_vectors", "subtract_vectors", "calculate_angle"]

from math import pi, atan


def add_vectors(vector_a: tuple, vector_b: tuple) -> tuple:
    """
    Adds two vectors together A + B

    @param vector_a: A tuple containing two numbers of the x and y components of the A vector respectively  
    @param vector_b: A tuple containing two numbers of the x and y components of the B vector respectively  
    @return: The result of A + B as a tuple
    """
    return vector_a[0] + vector_b[0], vector_a[1] + vector_b[1]


def subtract_vectors(vector_a: tuple, vector_b: tuple) -> tuple:
    """
    Subtracts two vectors A - B

    @param vector_a: A tuple containing two numbers of the x and y components of the A vector respectively  
    @param vector_b: A tuple containing two numbers of the x and y components of the B vector respectively  
    @return: The result of A - B as a tuple
    """
    return vector_a[0] - vector_b[0], vector_a[1] - vector_b[1]


def magnitude(vector: tuple) -> float:
    """
    Calculates the magnitude of a vector

    @param vector: A tuple containing two numbers of the x and y components of the vector respectively  
    @return The magnitude of the vector
    """
    return (vector[0] ** 2 + vector[1] ** 2) ** 0.5


def calculate_angle(pos_vector: tuple) -> float:
    """
    Calculates the angle of a vector

    @param pos_vector: A tuple containing two numbers of the x and y components of the vector respectively  
    @return: Calculates the angle of a vector where 0 is up from -pi to pi and the angle increases clockwise
    """
    if 0 in pos_vector:
        if pos_vector[0] == 0:
            return 0
        elif pos_vector[0] > 0:
            return pi / 2
        else:
            return -pi / 2
    elif pos_vector[1] > 0:
        return atan(pos_vector[0] / pos_vector[1])
    else:
        atan_theta = atan(pos_vector[0] / pos_vector[1])
        if atan_theta <= 0:
            return pi + atan_theta
        else:
            return atan_theta - pi
