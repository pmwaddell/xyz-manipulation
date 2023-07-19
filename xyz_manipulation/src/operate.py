from typing import List, Callable, Union
from xyz_reflection import Plane


def format_elem(elem: str) -> str:
    """
    Formats an element symbol for a .xyz file by adding an additional spaces
    after the symbol as needed in order to preserve the file's formatting.

    Parameters
    ----------
    elem : str
        String of the element symbol.

    Returns
    -------
    str
        Formatted element symbol.
    """
    assert ((len(elem) <= 2) and (len(elem) > 0))
    if len(elem) == 1:
        return elem + "   "
    return elem + "  "


def format_coord(coord: float) -> str:
    """
    Formats a coordinate for a .xyz file by representing the number to six
    decimal places and adding additional spaces in front as needed.

    The total length of each coordinate string should be 12.

    Parameters
    ----------
    coord : float
        Float of the coordinate to be formatted.

    Returns
    -------
    str
        Formatted coord., ready to add to a line in the translated .xyz file.
    """
    new_coord = "{:.6f}".format(coord)
    spaces_needed = 12 - len(new_coord)
    assert (spaces_needed >= 0)
    result = ""
    for i in range(spaces_needed):
        result += " "
    return result + new_coord


def operate_on_lines(lines: List,
                     operate: Callable,
                     operation_arg: Union[List, Plane]) -> List:
    result_contents = lines[0] + "\n" + lines[1] + "\n"
    for i in range(2, len(lines)):
        split_line = lines[i].split()
        if not split_line:
            continue
        assert (len(split_line) == 4)
        x, y, z = \
            float(split_line[1]), float(split_line[2]), float(split_line[3])
        new_point = operate([x, y, z], operation_arg)
        new_elem = format_elem(split_line[0])
        result_contents += new_elem + \
                           format_coord(new_point[0]) + \
                           format_coord(new_point[1]) + \
                           format_coord(new_point[2]) + "\n"
    return result_contents
