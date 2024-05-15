import os
import sys

def clear() :
    '''
    clears the console
    '''
    if os.name == 'nt' : # windows
        os.system('cls')
    else : # mac/linux
        os.system('clear')

def read_file(file_name, relative_path) :
    '''
    opens a file and returns its contents

    Arguments:
        file_name: the name of the file (str)
        relative_path: the relative path to the file when frozen (str)
    
    Returns:
        the contents of the file (list)
    '''
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        data_file = relative_path
    else:
        data_file = file_name
    with open(data_file, 'r') as file: 
        return file.read().split('\n')

def write_file(file_name, relative_path, data) :
    '''
    writes data to a file

    Arguments:
        file_name: the name of the file (str)
        relative_path: the relative path to the file when frozen (str)
        data: the lines of data to write to the file (list)
    '''
    to_write = ''
    for line in range(len(data)) :
        to_write += data[line]
        if line != len(data) - 1 :
            to_write += '\n'
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        data_file = relative_path
    else:
        data_file = file_name
    with open(data_file, 'w') as file :
        file.write(to_write)

def center_justified(text) :
    '''
    centers text in the console

    Arguments:
        text: the text to center (str)
    
    Returns:
        the centered text (str)
    '''
    width = os.get_terminal_size().columns
    return text.center(width)

if __name__ == '__main__' :
    clear()
    [deck_size, hand_size] = read_file('config.txt', 'Descryption_Data/config.txt')
    print(deck_size, hand_size)
    write_file('config.txt', 'Descryption_Data/config.txt', ['heelo', 'thure!'])