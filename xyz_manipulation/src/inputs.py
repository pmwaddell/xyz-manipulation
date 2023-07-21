#!/usr/bin/env python3
"""
This file contains utilities related to taking information from the user.
"""
__author__ = "Peter Waddell"
__copyright__ = "Copyright 2023"
__credits__ = ["Peter Waddell"]
__version__ = "0.0.1"
__date__ = "2023/07/16"
__maintainer__ = "Peter Waddell"
__email__ = "pmwaddell9@gmail.com"
__status__ = "Prototype"

import os
from typing import List, Callable


def input_filename(operation: str) -> str:
    """
    Asks the user to input the name of a .xyz file in the cwd. The user is
    prompted until they provide a valid input or request to quit.

    Returns
    -------
    str
        String of the filename of a .xyz file.
    """
    while True:
        print('Input the filename of the .xyz file you would like to '
              f'{operation} ("q" to quit): ', end='')
        filename = input()
        if filename == 'q' or filename == 'Q':
            quit()
        if not os.path.isfile(os.getcwd() + "\\" + filename):
            print('No file with name ' + filename +
                  ' found in current working directory: ' + os.getcwd() + '\n')
            continue
        if filename[-4:] != '.xyz':
            print(f'Invalid filename {filename}: please input a .xyz file.\n')
            continue
        return filename


def input_coordinates(identity: str, restart: Callable) -> List:
    """
    Takes input from the user for coordinates in 3-space.

    Parameters
    ----------
    identity : str
        Name of the thing (e.g. point, vector) which the input is for.
    restart : Callable
        Reference to the restart function to be called if the user decides.

    Returns
    -------
    List
        List of floats corresponding to the point input by the user.
    """
    while True:
        raw_input = input()
        if raw_input == 'q' or raw_input == 'Q':
            restart()
        raw_vector = raw_input.split()
        coords = []
        if len(raw_vector) > 3:
            print(f'Please input only up to three coordinates for '
                  f'the {identity}: ', end='')
            continue

        hit_value_error = False
        for comp in raw_vector:
            try:
                coords.append(float(comp))
            except ValueError:
                print(f'Please use numbers for the coordinates of the '
                      f'{identity}: ', end='')
                hit_value_error = True
                break
        if hit_value_error:
            continue
        if len(coords) < 3:
            for i in range(3 - len(coords)):
                coords.append(0)
        return coords


def input_point(restart: Callable) -> List:
    """
    Takes input from the user for a point.

    Parameters
    ----------
    restart : Callable
        Reference to the restart function to be called if the user decides.

    Returns
    -------
    List
        List of floats corresponding to the point input by the user.
    """
    return input_coordinates('point', restart)


def input_normal_vector(restart: Callable) -> List:
    """
    Takes input from the user for a normal vector.

    Parameters
    ----------
    restart : Callable
        Reference to the restart function to be called if the user decides.

    Returns
    -------
    List
        List of floats corresponding to the normal vector input by the user.
    """
    return input_coordinates('normal vector', restart)
