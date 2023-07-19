#!/usr/bin/env python3
"""
A script which translates sets of coordinates in .xyz files.

The user is prompted for the filename of the .xyz file they wish to translate,
the line in that file of the atom they would like to move, and the coordinates
of the new point to which they would like to move that atom. Then, a new .xyz
file is prepared which contains the same structure as the original file but
with all coordinates translated relative to the specified atom, effectively
translating the entire structure.
"""
__author__ = "Peter Waddell"
__copyright__ = "Copyright 2023"
__credits__ = ["Peter Waddell"]
__version__ = "0.0.1"
__date__ = "2023/03/06"
__maintainer__ = "Peter Waddell"
__email__ = "pmwaddell9@gmail.com"
__status__ = "Prototype"

from xyz_manipulation.src.inputs import input_filename
from xyz_operate import operate_on_lines
from typing import List


def restart():
    """
    Restarts the program after adding some space in the shell.
    """
    print('\n\n')
    main()
    quit()


def input_focus_line(last_line_num: int) -> int:
    """
    Asks the user to input the number of the 'focus line' of the .xyz file. The
    user is prompted until they provide a valid input or request to restart.

    The 'focus line' is the line containing the atom which the user wants to
    move to their specified point; all other atoms are moved relative to it.

    Parameters
    ----------
    last_line_num : int
        Number of the last line in the .xyz file, used to validate that the
        input from the user is not beyond the number of lines in the file.

    Returns
    -------
    int
        Number of the 'focus line' specified by the user.
    """
    while True:
        print("Input the number of the line in the file which contains the "
              "atom you would like to translate (all other atoms will be "
              "moved relative to this atom's new position) "
              "(\"q\" to restart): ", end='')
        raw_input = input()
        if raw_input == 'q' or raw_input == 'Q':
            restart()
        try:
            focus_line_num = int(raw_input)
        except ValueError:
            print('Please input an integer between 3 and the line of the last '
                  'atom in the .xyz file.\n')
            continue
        if focus_line_num < 3 or focus_line_num > last_line_num:
            print('Please input an integer between 3 and the line of the last '
                  'atom in the .xyz file.\n')
            continue
        return focus_line_num


def input_new_coords() -> List:
    """
    Asks the user to input the coordinates of the point to which the atom from
    the previously-specified 'focus line' will be translated. The user is
    prompted until they provide a valid input or request to restart.

    The input is taken as space-separated floats; if any are omitted, 0 is used.

    Returns
    -------
    List
        List of three floats representing coordinates of the new point.
    """
    while True:
        print("Input the x, y and z coordinates of the point to which you "
              "would like to translate this atom, in that order, separated by "
              "spaces (if any are omitted, they will be substituted with 0; "
              "empty input will move the atom to the origin) "
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
        return new_coords


def translate(point: List, d_vector: List) -> List:
    """
    Translates a point according to an input vector w/ the change in each coord.

    Parameters
    ----------
    point : List
        Coordinates of the point to be translated.
    d_vector : List
        Vector containing the desired change in each coordinate for translation.

    Returns
    -------
    List
        Coordinates of the translated point.
    """
    assert (len(point) == 3 and len(d_vector) == 3)
    return [point[0] + d_vector[0],
            point[1] + d_vector[1],
            point[2] + d_vector[2]]


def main():
    filename = input_filename('translate')
    with open(filename) as file_object:
        lines = file_object.read().split('\n')
    focus_line_num = input_focus_line(len(lines) - 1)
    new_coords = input_new_coords()
    focus_line = lines[focus_line_num - 1].split()
    d_vector = [new_coords[0] - float(focus_line[1]),
                new_coords[1] - float(focus_line[2]),
                new_coords[2] - float(focus_line[3])]
    translated_contents = operate_on_lines(lines, translate, d_vector)

    result_filename = filename[:-4] + " translated.xyz"
    with open(result_filename, 'w') as result_file:
        result_file.write(translated_contents)
    print(f'Process complete, result saved as {result_filename}.\n')

    print('If you would like to translate additional files, '
          'input "y": ', end='')
    ctn = input()
    if ctn == 'y' or ctn == 'Y':
        print('\n')
        main()


if __name__ == "__main__":
    main()
