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
