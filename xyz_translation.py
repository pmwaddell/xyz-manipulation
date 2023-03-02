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
    # TODO: ask for filename, handle not finding it
    with open('PNPNRhCOCl.xyz') as file_object:
        contents = file_object.read()
    lines = contents.split('\n')

    # TODO: ask for which line should be the zero point
    zero_line = lines[2].split()
    dx, dy, dz = -1 * float(zero_line[1]), float(zero_line[2]), float(
        zero_line[3])

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

    with open('RESULTTT.xyz', 'w') as result_file:
        result_file.write(translated_contents)


if __name__ == "__main__":
    main()
