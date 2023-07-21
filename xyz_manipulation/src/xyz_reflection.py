#!/usr/bin/env python3
"""
A script which reflects sets of coordinates in .xyz files.

The user is prompted for the filename of the .xyz file they wish to reflect,
and the plane (in terms of a point and normal vector) they want to reflect
through.  Then, a new .xyz file is prepared which contains the same structure
as the original file but with all coordinates reflected in this manner.
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
from inputs import input_filename, input_point, input_normal_vector
from xyz_operate import cross, calc_magnitude, calc_angle_between_vectors, \
    transform_lines
from xyz_rotation import rotate, get_compound_rotation_matrices
from plane import Plane


def restart():
    """
    Restarts the program after adding some space in the shell.
    """
    print('\n\n')
    main()
    quit()


def input_reflection_plane() -> Plane:
    """
    Takes input from the user for a point and normal vector and returns a
    corresponding instance of the Plane class.

    Returns
    -------
    Plane
        Instance of Plane class with desired point and normal vector.
    """
    print('Define the plane of reflection with a point and (relative) '
          'normal vector. First, input the coordinates of the point '
          '(if any coordinates are omitted, they will be substituted '
          'with 0) (\"q\" to restart): ', end='')
    point = input_point(restart)

    print('Now, input the x, y and z components of the normal vector to '
          'this point (if any components are omitted, they will be '
          'substituted with 0) (\"q\" to restart): ', end='')
    normal_vector = [0, 0, 0]
    while normal_vector == [0, 0, 0]:
        normal_vector = input_normal_vector(restart)
        if normal_vector == [0, 0, 0]:
            print('Please provide a vector with nonzero magnitude.\n')
    return Plane(point, normal_vector)


def xy_reflect(point: List) -> List:
    """
    Reflects a point through the xy plane.

    Parameters
    ----------
    point : List
        List of three floats corresponding to the point that will be reflected.

    Returns
    -------
    List
        List of three floats corresponding to the point after reflection.
    """
    return [point[0], point[1], -1 * point[2]]


def reflect(point: List, plane: Plane) -> List:
    """
    Reflects a point through a given plane.

    Parameters
    ----------
    point : List
        List of three floats corresponding to the point that will be reflected.
    plane : Plane
        Plane through which the point will be reflected.

    Returns
    -------
    List
        List of three floats corresponding to the point after reflection.
    """
    from xyz_translation import translate
    plane_point = plane.get_point()
    plane_vector = plane.get_normal_vector()
    # Translate Plane's point to origin, move target point as well.
    d_vector = [-1 * plane_point[0], -1 * plane_point[1], -1 * plane_point[2]]
    translated_point = translate(point, d_vector)
    # Rotate normal vector to align with xy plane.
    theta = calc_angle_between_vectors(plane.get_normal_vector(), [0, 0, 1])
    cross_pdt = cross(plane_vector, [0, 0, 1])

    # In the case where the plane's normal vector is (0, 0, 1), don't rotate.
    if calc_magnitude(cross_pdt) != 0:
        rot_matrices = get_compound_rotation_matrices(cross_pdt, theta)
        rotated_point = rotate(translated_point, rot_matrices)
    else:
        rotated_point = translated_point
    # Reflect through the xy plane.
    reflected_point = xy_reflect(rotated_point)

    # Undo the first 2 steps
    if calc_magnitude(cross_pdt) != 0:
        unrot_matrices = get_compound_rotation_matrices(cross_pdt, -1 * theta)
        unrotated_point = rotate(reflected_point, unrot_matrices)
    else:
        unrotated_point = reflected_point
    return translate(unrotated_point, plane_point)


def main():
    filename = input_filename('reflect')
    with open(filename) as file_object:
        lines = file_object.read().split('\n')
    reflection_plane = input_reflection_plane()
    # TODO: consider abstracting each type of transformation as a class that associates the matrices with the angle, for example?
    reflected_contents = transform_lines(lines, reflect, reflection_plane)

    result_filename = filename[:-4] + " reflected.xyz"
    with open(result_filename, 'w') as result_file:
        result_file.write(reflected_contents)
    print(f'Process complete, result saved as {result_filename}.\n')

    print('If you would like to reflect additional files, input "y": ', end='')
    ctn = input()
    if ctn == 'y' or ctn == 'Y':
        print('\n')
        main()


if __name__ == "__main__":
    main()
