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

def split_nicely(text, first_line_length, gen_line_length, max_lines=10, add_blank_lines=False) :
    '''
    splits text into lines of a certain length

    Arguments:
        text: the text to split (str)
        first_line_length: the length of the first line (int)
        gen_line_length: the length of the general lines (int)
        max_lines: the maximum number of lines, defaults to 10 (int)
        add_blank_lines: whether to add blank lines to the end of the text to reach the maximum number of lines, defaults to False (bool)
    
    Returns:
        the split text (list)
    '''
    lines = []

    if len(text) > first_line_length :
        # if the first line is too long, split it
        if text[:first_line_length][-1] == ' ' :
            lines.append(text[:first_line_length])
            text = text[first_line_length:]
        elif text[first_line_length:][0] != ' ': # hyphenate last word if needed
            lines.append(text[:(first_line_length - 1)] + '-')
            text = text[(first_line_length - 1):]
        else : # cut off leading space from next line
            lines.append(text[:first_line_length])
            text = text[(first_line_length + 1):]
    else :
        lines.append(text)
        text = ''

    while text !='' :
        if len(text) > gen_line_length :
            # if the text is too long, split it
            if text[:gen_line_length][-1] == ' ' :
                lines.append(text[:gen_line_length])
                text = text[gen_line_length:]
            elif text[gen_line_length:][0] != ' ' : # hyphenate last word if needed
                lines.append(text[:(gen_line_length - 1)] + '-')
                text = text[(gen_line_length - 1):]
            else : # cut off leading space from next line
                lines.append(text[:gen_line_length])
                text = text[(gen_line_length + 1):]
        else : # add the last line
            lines.append(text)
            text = ''

    if len(lines) > max_lines :
        # add ellipsis if text is too long
        lines = lines[:max_lines]
        lines[-1] = lines[-1][:-3] + '...'

    if len(lines) < max_lines and add_blank_lines :
        # add blank lines if needed
        for i in range(max_lines - len(lines)) :
            lines.append('')

    return lines

def chunk(iterable, n) :
    '''
    chunks an iterable into n-sized chunks

    Arguments:
        iterable: the iterable to chunk (iterable)
        n: the size of the chunks (int)
    
    Returns:
        Chunks: a list of the chunks in order (list)
    '''
    chunks = []

    for i in range(0, len(iterable), n) :
        chunks.append(iterable[i:i + n])

    return chunks

def title_case(string) :
    '''
    converts a string to title case

    Arguments:
        string: the string to convert (str)
    
    Returns:
        the title cased string (str)
    '''
    words = string.split()
    title_cased = ''
    for i in range(len(words)) :
        if i == 0 :
            title_cased += words[i].capitalize() + ' '
        elif words[i] not in ['and', 'or', 'the', 'a', 'an', 'of', 'in', 'on', 'at', 'to', 'with', 'from', 'by', 'as', 'for', 'but', 'nor', 'so', 'yet'] :
            title_cased += words[i].capitalize() + ' '
        else :
            title_cased += words[i] + ' '
    return title_cased


if __name__ == '__main__' :
    clear()
    [deck_size, hand_size] = read_file('config.txt', 'Descryption_Data/config.txt')
    print(deck_size, hand_size)
    write_file('config.txt', 'Descryption_Data/config.txt', ['heelo', 'thure!'])