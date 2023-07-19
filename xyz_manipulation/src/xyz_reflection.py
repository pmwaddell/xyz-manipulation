from typing import List
from xyz_manipulation.src.inputs import input_filename
from xyz_manipulation.src.xyz_operate import format_coord, format_elem, \
    calc_angle_between_vectors
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
        print('Define the Plane of reflection with a point and (relative) '
              'normal vector which define the desired rotation Plane. '
              'First, input the coordinates of the point (if any coordinates '
              'are omitted, they will be substituted with 0)'
              '(\"q\" to restart): ', end='')
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


def cross(u: List, v: List) -> List:
    return [
        [(u[2] * v[3]) - (u[3] * v[2])],
        [(u[1] * v[3]) - (u[3] * v[1])],
        [(u[1] * v[2]) - (u[2] * v[1])]
    ]


def xy_reflect(point: List) -> List:
    return [point[0], point[1], -1 * point[2]]


# TODO: make this a general transformation function instead in a shared file?
def reflect(point: List, plane: Plane) -> List:
    from xyz_translation import translate
    plane_point = plane.get_point()
    plane_vector = plane.get_normal_vector()
    # translate Plane's point to origin, move target point as well
    d_vector = [-1 * plane_point[0] - 1 * plane_point[1], -1 * plane_point[2]]
    translated_point = translate(point, d_vector)
    # rotate normal vector to align with xy Plane
    theta = calc_angle_between_vectors(plane.get_normal_vector(), [0, 0, 1])
    cross_pdt = cross(plane_vector, [0, 0, 1])
    rot_matrices = get_compound_rotation_matrices(cross_pdt, theta)
    rotated_point = rotate(translated_point, rot_matrices)
    # reflect thru xy Plane
    reflected_point = xy_reflect(rotated_point)
    # undo first 2 steps
    unrot_matrices = get_compound_rotation_matrices(cross_pdt, -1 * theta)
    unrotated_point = rotate(translated_point, unrot_matrices)
    return translate(unrotated_point, plane_point)


def main():
    filename = input_filename('reflect')
    filename_no_xyz = filename[:-4]
    with open(filename) as file_object:
        contents = file_object.read()
    lines = contents.split('\n')
    reflection_plane = input_reflection_plane()

    # TODO: make this into its own function? for all 3
    reflected_contents = lines[0] + "\n" + lines[1] + "\n"
    for i in range(2, len(lines)):
        split_line = lines[i].split()
        if not split_line:
            continue
        assert (len(split_line) == 4)
        x, y, z = \
            float(split_line[1]), float(split_line[2]), float(split_line[3])
        new_x, new_y, new_z = reflect([x, y, z], reflection_plane)
        new_elem = format_elem(split_line[0])
        reflected_contents += new_elem + \
                              format_coord(new_x) + \
                              format_coord(new_y) + \
                              format_coord(new_z) + "\n"

    result_filename = filename_no_xyz + " rotated.xyz"
    with open(result_filename, 'w') as result_file:
        result_file.write(reflected_contents)
    print(f'Process complete, result saved as {result_filename}.\n')

    print('If you would like to rotate additional files, input "y": ', end='')
    ctn = input()
    if ctn == 'y' or ctn == 'Y':
        print('\n')
        main()


if __name__ == "__main__":
    main()
