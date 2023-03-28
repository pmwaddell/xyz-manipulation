#!/usr/bin/env python3
"""
A script which rotates sets of coordinates in .xyz files.

The user is prompted for the filename of the .xyz file they wish to translate,
the axis about which they would like to rotate the structure, and the number of
degrees they would like to rotate it by. Then, a new .xyz file is prepared
which contains the same structure as the original file but with all coordinates
rotated in this manner.
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


def normalize(v: List) -> List:
    """
    Returns a normalized version of the input vector (i.e. same direction but
    magnitude of 1).

    Parameters
    ----------
    v : List
        List of three floats: coordinates to the vector that will be normalized.

    Returns
    -------
    List
        List of three floats corresponding to the point after normalization.
    """
    return [i / get_magnitude(v) for i in v]


def get_magnitude(v: List) -> float:
    """
    Returns the magnitude of the input vector.

    Parameters
    ----------
    v : List
        List of  floats: coordinates of the vector.

    Returns
    -------
    float
        Magnitude of the vector.
    """
    return math.sqrt(sum([i ** 2 for i in v]))


def dot(u: List, v: List) -> float:
    """
    Computes the dot product of two vectors.

    Parameters
    ----------
    v : List
        List of  floats: coordinates of the vector.
    u : List
        List of  floats: coordinates of the vector.

    Returns
    -------
    float
        Dot product of the two vectors.
    """
    assert (len(u) == 3 and len(v) == 3)
    result = 0
    for i in range(3):
        result += u[i] * v[i]
    return result


def get_angle_between_vectors(u: List, v: List) -> float:
    """
    Computes the angle between two vectors.

    Parameters
    ----------
    v : List
        List of  floats: coordinates of the vector.
    u : List
        List of  floats: coordinates of the vector.

    Returns
    -------
    float
        Angle between the two vectors, in degrees.
    """
    return math.degrees(
        math.acos(dot(u, v) / (get_magnitude(u) * get_magnitude(v)))
    )


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


def get_rotation_matrices(theta: float) -> List:
    """
    Asks the user to input a point that, along with the origin, defines the
    desired axis of rotation. The name of one of the principle axes can also be
    input (x, y or z). The user is prompted until they provide a valid input or
    request to restart.

    Returns
    -------
    List
        List of rotation matrices for the desired rotation.
    """
    while True:
        print('Input the coordinates of the point which, along with the '
              'origin, defines the axis you would like to rotate around '
              '(input "x", "y" or "z" to rotate around those axes; if any '
              'coordinates are omitted, they will be substituted with 0) '
              '(\"q\" to restart): ', end='')
        raw_input = input()

        if raw_input == 'q' or raw_input == 'Q':
            restart()
        if raw_input == 'x' or raw_input == 'X':
            return [get_x_rotation_matrix(theta)]
        elif raw_input == 'y' or raw_input == 'Y':
            return [get_y_rotation_matrix(theta)]
        elif raw_input == 'z' or raw_input == 'Z':
            return [get_z_rotation_matrix(theta)]

        raw_point = raw_input.split()
        point = []
        if len(raw_point) > 3:
            print('Please input only up to three coordinates.\n')
            continue
        for coord in raw_point:
            try:
                point.append(float(coord))
            except ValueError:
                print('Please use numbers for the coordinates of the point.\n')
                continue
        if point == [0, 0, 0]:
            print('Please select a point other than the origin.\n')
            continue
        if len(point) < 3:
            for i in range(3 - len(point)):
                point.append(0)
        return get_compound_rotation_matrices(point, theta)


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


def get_compound_rotation_matrices(rotation_axis: List, theta: float) -> List:
    """
    Returns a list of rotation matrices (around x, y and z) which represent a
    rotation around an arbitrary axis by the input degrees.

    Parameters
    ----------
    rotation_axis : List
        List of  floats: coordinates of the rotation axis (which is taken to be
        between the origin and this input point).
    theta : float
        Number of degrees for the rotation.

    Returns
    -------
    List
        List of rotation matrices which accomplish the desired rotation.
    """
    unit_vector = normalize(rotation_axis)
    alpha = get_angle_between_vectors([0, unit_vector[1], unit_vector[2]],
                                      [0, 0, 1])
    step_1_matrix = get_x_rotation_matrix(alpha)
    q = rotate(unit_vector, [step_1_matrix])
    beta = get_angle_between_vectors(q, [0, 0, 1])

    return [get_x_rotation_matrix(alpha),
            get_y_rotation_matrix(-1 * beta),
            get_z_rotation_matrix(theta),
            get_y_rotation_matrix(beta),
            get_x_rotation_matrix(-1 * alpha)]


def rotate(point: List, rotation_matrices: List) -> List:
    """
    Performs a rotation on a point via matrix multiplication, returns the new
    coordinates of the rotated point.

    Parameters
    ----------
    point : List
        List of three floats corresponding to the point that will be rotated.
    rotation_matrices : List
        List of 3 x 3 matrices representing the transformation matrices for
        a rotation.

    Returns
    -------
    List
        List of three floats corresponding to the point after rotation.
    """
    assert (len(point) == 3)
    for rotation_matrix in rotation_matrices:
        assert (len(rotation_matrix) == 3
                and len(rotation_matrix[0]) == 3
                and len(rotation_matrix[1]) == 3
                and len(rotation_matrix[2]) == 3)
    result = point.copy()
    for rotation_matrix in rotation_matrices:
        old_point = result.copy()
        result = []
        for i in range(3):
            coord = 0
            for j in range(3):
                coord += rotation_matrix[i][j] * old_point[j]
            result.append(coord)
    return result


def main():
    filename = get_filename_input('rotate')
    filename_no_xyz = filename[:-4]
    with open(filename) as file_object:
        contents = file_object.read()
    lines = contents.split('\n')
    theta = get_rotation_degrees()
    rotation_matrices = get_rotation_matrices(theta)

    # TODO: make this into its own function?
    rotated_contents = lines[0] + "\n" + lines[1] + "\n"
    for i in range(2, len(lines)):
        split_line = lines[i].split()
        if split_line:
            assert (len(split_line) == 4)
            x, y, z = \
                float(split_line[1]), float(split_line[2]), float(split_line[3])
            new_x, new_y, new_z = rotate([x, y, z], rotation_matrices)
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
