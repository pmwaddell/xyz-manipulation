import os
from typing import List


def get_filename_input() -> str:
    while True:
        print('Input the filename of the .xyz file you would like to '
              'translate ("q" to quit): ', end='')
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


def get_focus_line_input(last_line_num: int) -> int:
    while True:
        print("Input the number of the line in the file which contains the "
              "atom you would like to translate (all other atoms will be "
              "moved relative to this atom's new position) "
              "(\"q\" to restart): ", end='')
        raw_input = input()
        if raw_input == 'q' or raw_input == 'Q':
            print('\n\n')
            main()
            quit()
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


def get_new_coords_input() -> List:
    while True:
        print("Input the x, y and z coordinates of the point to which you "
              "would like to translate this atom, in that order, separated by "
              "spaces (if any are omitted, they will be substituted with 0; "
              "empty input will move the atom to the origin) "
              "(\"q\" to restart): ", end='')
        raw_input = input()
        if raw_input == 'q' or raw_input == 'Q':
            print('\n\n')
            main()
            quit()
        new_coords = raw_input.split()
        if len(new_coords) > 3:
            print('Please input only up to three coordinates.\n')
            continue
        for coord in new_coords:
            try:
                # This merely tests that coord can be converted properly to a float.
                float(coord)
            except ValueError:
                print('Please use numbers for the new coordinates.')
                continue
        if len(new_coords) < 3:
            for i in range(3 - len(new_coords)):
                new_coords.append('0')
        return new_coords


def format_elem(elem: str) -> str:
    assert((len(elem) <= 2) and (len(elem) > 0))
    if len(elem) == 1:
        return elem + " "
    return elem


def format_coord(coord: float, d: float, total_spaces: int) -> str:
    new_coord = "{:.6f}".format(coord + d)
    spaces_needed = total_spaces - len(new_coord)
    assert(spaces_needed >= 0)
    result = ""
    for i in range(spaces_needed):
        result += " "
    return result + new_coord


def format_x(coord: float, d: float) -> str:
    return format_coord(coord, d, 14)


def format_y_or_z(coord: float, d: float) -> str:
    return format_coord(coord, d, 12)


def main():
    filename = get_filename_input()
    filename_no_xyz = filename[:-4]
    with open(filename) as file_object:
        contents = file_object.read()
    lines = contents.split('\n')

    # 'focus line' means the line containing the atom that will be translated to the coordinates input by the user
    focus_line_num = get_focus_line_input(len(lines) - 1)

    new_coords = get_new_coords_input()
    focus_line = lines[focus_line_num - 1].split()
    dx, dy, dz = \
        float(new_coords[0]) - float(focus_line[1]), \
        float(new_coords[1]) - float(focus_line[2]), \
        float(new_coords[2]) - float(focus_line[3])

    translated_contents = lines[0] + "\n" + lines[1] + "\n"
    for i in range(2, len(lines)):
        split_line = lines[i].split()
        if split_line:
            assert (len(split_line) == 4)
            x, y, z = \
                float(split_line[1]), float(split_line[2]), float(split_line[3])
            new_elem = format_elem(split_line[0])
            new_x, new_y, new_z = \
                format_x(x, dx), format_y_or_z(y, dy), format_y_or_z(z, dz)
            translated_contents += new_elem + new_x + new_y + new_z + "\n"

    result_filename = filename_no_xyz + " translated.xyz"
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
