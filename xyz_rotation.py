#!/usr/bin/env python3
"""
A script which rotates sets of coordinates in .xyz files.

The user is prompted for the filename of the .xyz file they wish to translate,
the name of the axis about which they would like to rotate the structure, and
the number of degrees they would like to rotate it by. Then, a new .xyz file is
prepared which contains the same structure as the original file but
with all coordinates rotated in this manner.
"""
__author__ = "Peter Waddell"
__copyright__ = "Copyright 2023"
__credits__ = ["Peter Waddell"]
__version__ = "0.0.1"
__date__ = "2023/03/06"
__maintainer__ = "Peter Waddell"
__email__ = "pmwaddell9@gmail.com"
__status__ = "Prototype"

import math
from get_inputs import get_filename_input
from format_for_xyz import format_coord, format_elem
from typing import List


def restart():
    """
    Restarts the program after adding some space in the shell.
    """
    print('\n\n')
    main()
    quit()


# TODO: rotation wrt arbitrary axis: https://www.youtube.com/watch?v=XqNCbe2flb8
# see also https://www.eng.uc.edu/~beaucag/Classes/Properties/OptionalProjects/CoordinateTransformationCode/Rotate%20about%20an%20arbitrary%20axis%20(3%20dimensions).html
def get_new_coords_input() -> List:
    """
    Asks the user to input the coordinates of the point to which the atom from
    the previously-specified 'focus line' will be translated. The user is
    prompted until they provide a valid input or request to restart.

    The input is taken as space-separated floats; if any are omitted, 0 is
    used. Any point other than the origin is accepted.

    Returns
    -------
    List
        List of three floats representing coordinates of the new point.
    """
    while True:
        print("Input the x, y and z coordinates, in that order, of the point "
              "which defines the axis of rotation separated by spaces (if any "
              "are omitted, they will be substituted with 0) which will be the "
              "line between this point and the origin. "
              "(\"q\" to restart): ", end='')
        raw_input = input()
        if raw_input == 'q' or raw_input == 'Q':

            restart()
        raw_new_coords = raw_input.split()
        new_coords = []
        if len(raw_new_coords) > 3:
            print('Please input only up to three coordinates.\n')
            continue
        for coord in raw_new_coords:
            try:
                new_coords.append(float(coord))
            except ValueError:
                print('Please use numbers for the new coordinates.')
                continue
        if len(new_coords) < 3:
            for i in range(3 - len(new_coords)):
                new_coords.append(0)
        if new_coords == [0, 0, 0]:
            print('Please use any point other than the origin.')
            continue
        return new_coords


def get_axis_input() -> str:
    """
    Asks the user to input the name of the desired axis of rotation
    (x, y or z). The user is prompted until they provide a valid input or
    request to restart.

    Returns
    -------
    str
        String of the name of the desired axis of rotation (x, y or z).
    """
    while True:
        print('Input the axis you would like to rotate around '
              '(x, y or z) (\"q\" to restart): ', end='')
        axis = input()
        if axis == 'q' or axis == 'Q':
            restart()
        good_axes = {'x', 'y', 'z', 'X', 'Y', 'Z'}
        if axis not in good_axes:
            print('Please input one of x, y or z for the rotation axis.\n')
            continue
        return axis


def get_rotation_degrees() -> float:
    """
    Asks the user to input the desired number of degrees for the rotation. The
    user is prompted until they provide a valid input or request to restart.

    Returns
    -------
    float
        Float corresponding to degrees of the desired rotation.
    """
    while True:
        print('Input how many degrees you would like to rotate: ', end='')
        theta = input()
        if theta == 'q' or theta == 'Q':
            restart()
        try:
            return float(theta)
        except ValueError:
            print('Please use numbers for the new coordinates.')
            continue


def get_x_rotation_matrix(theta: float) -> List:
    """
    Returns the matrix for rotation around the x axis by theta degrees.

    Returns
    -------
    List
        3 x 3 matrix for rotation around the x axis by theta degrees.
    """
    return [[1, 0, 0],
            [0,
             math.cos(math.radians(theta)),
             -1 * math.sin(math.radians(theta))],
            [0,
             math.sin(math.radians(theta)),
             math.cos(math.radians(theta))]]


def get_y_rotation_matrix(theta: float) -> List:
    """
    Returns the matrix for rotation around the y axis by theta degrees.

    Returns
    -------
    List
        3 x 3 matrix for rotation around the y axis by theta degrees.
    """
    return [[math.cos(math.radians(theta)),
             0,
             math.sin(math.radians(theta))],
            [0, 1, 0],
            [-1 * math.sin(math.radians(theta)),
             0,
             math.cos(math.radians(theta))]]


def get_z_rotation_matrix(theta: float) -> List:
    """
    Returns the matrix for rotation around the z axis by theta degrees.

    Returns
    -------
    List
        3 x 3 matrix for rotation around the z axis by theta degrees.
    """
    return [[math.cos(math.radians(theta)),
             -1 * math.sin(math.radians(theta)),
             0],
            [math.sin(math.radians(theta)),
             math.cos(math.radians(theta)),
             0],
            [0, 0, 1]]


def rotate(point: List, rotation_matrix: List) -> List:
    """
    Performs a rotation on a point via matrix multiplication, returns the new
    coordinates of the rotated point.

    Parameters
    ----------
    point : List
        List of three floats corresponding to the point that will be rotated.
    rotation_matrix : List
        3 x 3 matrix representing the transformation matrix for a rotation.

    Returns
    -------
    List
        List of three floats corresponding to the point after rotation.
    """
    assert (len(point) == 3)
    assert (len(rotation_matrix) == 3 and len(rotation_matrix[0]) == 3
            and len(rotation_matrix[1]) == 3 and len(rotation_matrix[2]) == 3)
    result = []
    for i in range(3):
        coord = 0
        for j in range(3):
            coord += rotation_matrix[i][j] * point[j]
        result.append(coord)
    return result


def main():
    filename = get_filename_input('rotate')
    filename_no_xyz = filename[:-4]
    with open(filename) as file_object:
        contents = file_object.read()
    lines = contents.split('\n')
    axis = get_axis_input()
    theta = get_rotation_degrees()

    rotation_matrix = []
    if axis == 'x' or axis == 'X':
        rotation_matrix = get_x_rotation_matrix(theta)
    elif axis == 'y' or axis == 'Y':
        rotation_matrix = get_y_rotation_matrix(theta)
    elif axis == 'z' or axis == 'Z':
        rotation_matrix = get_z_rotation_matrix(theta)

    rotated_contents = lines[0] + "\n" + lines[1] + "\n"
    for i in range(2, len(lines)):
        split_line = lines[i].split()
        if split_line:
            assert (len(split_line) == 4)
            x, y, z = \
                float(split_line[1]), float(split_line[2]), float(split_line[3])
            new_x, new_y, new_z = rotate([x, y, z], rotation_matrix)
            new_elem = format_elem(split_line[0])
            rotated_contents += new_elem + \
                                format_coord(new_x) + \
                                format_coord(new_y) + \
                                format_coord(new_z) + "\n"

    result_filename = filename_no_xyz + " rotated.xyz"
    with open(result_filename, 'w') as result_file:
        result_file.write(rotated_contents)
    print(f'Process complete, result saved as {result_filename}.\n')

    print('If you would like to rotate additional files, input "y": ', end='')
    ctn = input()
    if ctn == 'y' or ctn == 'Y':
        print('\n')
        main()


if __name__ == "__main__":
    main()
