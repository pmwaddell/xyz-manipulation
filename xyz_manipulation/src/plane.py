#!/usr/bin/env python3
"""
A class representing a plane in 3-space.
"""
__author__ = "Peter Waddell"
__copyright__ = "Copyright 2023"
__credits__ = ["Peter Waddell"]
__version__ = "0.0.1"
__date__ = "2023/07/16"
__maintainer__ = "Peter Waddell"
__email__ = "pmwaddell9@gmail.com"
__status__ = "Prototype"

from typing import List


class Plane:
    """
    A class representing a plane in 3D, defined by a point and normal vector.
    """
    def __init__(self, point: List, normal_vector: List):
        """
        Parameters
        ----------
        point : List
            List of three floats corresponding to the point.
        normal_vector : List
            List of three floats corresponding to the normal vector's coords.
        """
        assert (len(point) == 3)
        assert (len(normal_vector) == 3)
        self.point = point
        self.normal_vector = normal_vector

    def get_point(self) -> List:
        """
        Getter that returns the point which defines the plane in part.

        Returns
        -------
        List
            List of three floats corresponding to the point.
        """
        return self.point.copy()

    def get_normal_vector(self) -> List:
        """
        Getter that returns the normal vector which defines the plane in part.

        Returns
        -------
        List
            List of three floats corresponding to the normal vector's coords.
        """
        return self.normal_vector.copy()
