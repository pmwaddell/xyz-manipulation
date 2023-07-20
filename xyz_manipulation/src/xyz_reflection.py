from typing import List
from inputs import input_filename
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
    while True:
        print('Define the plane of reflection with a point and (relative) '
              'normal vector. First, input the coordinates of the point '
              '(if any coordinates are omitted, they will be substituted '
              'with 0) (\"q\" to restart): ', end='')
        raw_input = input()

        if raw_input == 'q' or raw_input == 'Q':
            restart()
        raw_vector = raw_input.split()
        point = []
        if len(raw_vector) > 3:
            print('Please input only up to three coordinates.\n')
            continue
        for comp in raw_vector:
            try:
                point.append(float(comp))
            except ValueError:
                print('Please use numbers for the coordinates of the point.\n')
                continue
        if point == [0, 0, 0]:
            print('Please select a point other than the origin.\n')
            continue
        if len(point) < 3:
            for i in range(3 - len(point)):
                point.append(0)
        break

    # TODO: abstract here
    while True:
        print('Now, input the x, y and z components of the normal vector to '
              'this point (if any components are omitted, they will be '
              'substituted with 0) (\"q\" to restart): ', end='')
        raw_input = input()

        if raw_input == 'q' or raw_input == 'Q':
            restart()
        raw_vector = raw_input.split()
        normal_vector = []
        if len(raw_vector) > 3:
            print('Please input only up to three components.\n')
            continue
        for comp in raw_vector:
            try:
                normal_vector.append(float(comp))
            except ValueError:
                print('Please use numbers for the components of the normal '
                      'vector.\n')
                continue
        if normal_vector == [0, 0, 0]:
            print('Please provide a vector with nonzero magnitude.\n')
            continue
        if len(normal_vector) < 3:
            for i in range(3 - len(normal_vector)):
                normal_vector.append(0)
        return Plane(point, normal_vector)


def xy_reflect(point: List) -> List:
    return [point[0], point[1], -1 * point[2]]


# TODO: make this a general transformation function instead in a shared file?
def reflect(point: List, plane: Plane) -> List:
    from xyz_translation import translate
    plane_point = plane.get_point()
    plane_vector = plane.get_normal_vector()
    # translate Plane's point to origin, move target point as well
    d_vector = [-1 * plane_point[0], -1 * plane_point[1], -1 * plane_point[2]]
    translated_point = translate(point, d_vector)
    # rotate normal vector to align with xy Plane
    theta = calc_angle_between_vectors(plane.get_normal_vector(), [0, 0, 1])
    cross_pdt = cross(plane_vector, [0, 0, 1])

    # In the case where the plane's normal vector is (0, 0, 1), don't rotate.
    # TODO: abstract this conditional rotation? or build this condition into the rotation function? or something?
    if calc_magnitude(cross_pdt) != 0:
        rot_matrices = get_compound_rotation_matrices(cross_pdt, theta)
        rotated_point = rotate(translated_point, rot_matrices)
    else:
        rotated_point = translated_point
    # reflect thru xy Plane
    reflected_point = xy_reflect(rotated_point)

    # undo first 2 steps
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
