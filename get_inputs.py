import os


def get_filename_input(operation: str) -> str:
    """
    Asks the user to input the name of a .xyz file in the cwd. The user is
    prompted until they provide a valid input or request to quit.

    Returns
    -------
    str
        String of the filename of a .xyz file.
    """
    while True:
        print('Input the filename of the .xyz file you would like to '
              f'{operation} ("q" to quit): ', end='')
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
