import os
from get_inputs import get_filename_input
from format_xyz import format_coord, format_elem
from typing import List


def main():
    filename = get_filename_input('rotate')
    filename_no_xyz = filename[:-4]
    with open(filename) as file_object:
        contents = file_object.read()
    lines = contents.split('\n')

    # Establish the line w two points
    # Ask for # of degrees
    # Create rotation matrix
    # Do matrix multiplication for each point
    # Format and add to the rotated_contents
    """
    rotated_contents = lines[0] + "\n" + lines[1] + "\n"
    for i in range(2, len(lines)):
        split_line = lines[i].split()
        if split_line:
            assert (len(split_line) == 4)
            x, y, z = \
                float(split_line[1]), float(split_line[2]), float(split_line[3])
            new_elem = format_elem(split_line[0])
            # GET THE NEW COORDINATES
            rotated_contents += new_elem + \
                                   format_coord(new_x) + \
                                   format_coord(new_y) + \
                                   format_coord(new_z) + "\n"

    result_filename = filename_no_xyz + " rotated.xyz"
    with open(result_filename, 'w') as result_file:
        result_file.write(rotated_contents)
    print(f'Process complete, result saved as {result_filename}.\n')
    """
    print('If you would like to rotate additional files, input "y": ', end='')
    ctn = input()
    if ctn == 'y' or ctn == 'Y':
        print('\n')
        main()


if __name__ == "__main__":
    main()
