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
            title_cased += words[i].capitalize()
        elif words[i] not in ['and', 'or', 'the', 'a', 'an', 'of', 'in', 'on', 'at', 'to', 'with', 'from', 'by', 'as', 'for', 'but', 'nor', 'so', 'yet'] :
            title_cased += words[i].capitalize()
        else :
            title_cased += words[i]
        if i != len(words) - 1 :
            title_cased += ' '
    return title_cased

def exec_sigil_code(current_card, applicables, global_vars=None, local_vars=None, vars_to_return=[]) :
    '''
    executes sigil code
    
    Arguments:
        current_card: the card to execute the sigil code for (Card)
        applicables: the sigils to execute (list)
        global_vars: the global variables to use (dict)
        local_vars: the local variables to use (dict)
        vars_to_return: the variables to return (list of str)
    
    Returns:
        the variables to return (list)
    '''
    # imports
    import sigils

    # set up variables
    returned_vars = []

    if current_card.sigil in applicables :
        exec(sigils.Dict[current_card.sigil][2], global_vars, local_vars)

    for var in vars_to_return :
        returned_vars.append(local_vars[var])

    return returned_vars

def hefty_check(field, zone, direction) :
    '''
    recursively checks how many cards can be pushed by a card with hefty sigil

    Arguments:
        field: the field to check (dict)
        zone: the zone to check (int)
        direction: the direction to check (str)
    
    Returns:
        the number of cards that can be pushed, -1 being the card after the hefty one is open (int)
    '''
    # issue, will return positive values when it should return 0 because its just adding
    if direction == 'right' :
        if field[zone].species == '' : # only when the card after the card with hefty is empty
            return -1
        if field[zone+1].species != '' and zone < 5 :
            if hefty_check(field, zone+1, direction) == 0 :
                return 0
            return 1 + hefty_check(field, zone+1, direction)
        elif field[zone+1].species == '' and zone < 5 :
            return 1
        else :
            return 0
    elif direction == 'left' :
        if field[zone].species == '' : # only when the card after the card with hefty is empty
            return -1
        if field[zone-1].species != '' and zone > 1 :
            if hefty_check(field, zone-1, direction) == 0 :
                return 0
            return 1 + hefty_check(field, zone-1, direction)
        if field[zone-1].species == '' and zone > 1 :
            return 1
        else :
            return 0

def sort_deck(deck) :
    '''
    sorts a deck by cost and name

    Arguments:
        deck: the deck to sort (list)
    
    Returns:
        the sorted deck (list)
    '''
    deck = sorted(deck, key=lambda x: x.name) # sort by name (will be sub-sorting under cost)
    return sorted(deck, key=lambda x: x.cost)

def print_deck(deck, sort=False, fruitful=False) :
    '''
    prints a list of cards in a deck, with optional sorting

    Arguments:
        deck: deck to print (list)
        sort: whether to sort the deck before printing (bool)
        fruitful: whether to return the deck string instead of printing it (bool)
    '''
    # sort deck if needed
    if sort :
        deck = sort_deck(deck)
    
    # get terminal size
        term_cols = os.get_terminal_size().columns
        card_gaps = (term_cols*55 // 100) // 5 - 15
        card_gaps_space = ' ' * card_gaps

        # get number of cards per row
        cards_per_row = term_cols // (card_gaps + 15) 
        if cards_per_row >= 9 :
            cards_per_row = 8
    
        # split deck into rows
        chunked = chunk(deck, cards_per_row)
        
        # generate deck string
        deck_string = '\n'.join(
            '\n'.join(
                card_gaps_space + card_gaps_space.join(card.text_by_line() for card in row)
                for _ in range(11)
            )
            for row in chunked
        )
        if fruitful :
            return deck_string
        print(deck_string)

def reps_int(string, increment=0) :
    '''
    checks if a string represents an integer and returns it

    Arguments:
        string: the string to convert (str)
        increment: the increment to add to the integer, defaults to 0 (int)
    
    Returns:
        is_int: whether the string is an integer (bool)
        int_value: the integer, will default to 0 (int)
    '''
    try :
        int_value = int(string) + increment
        is_int = True
    except ValueError :
        int_value = 0
        is_int = False
    return is_int, int_value

if __name__ == '__main__' :
    clear()
    [deck_size, hand_size] = read_file('config.txt', 'Descryption_Data/config.txt')
    print(deck_size, hand_size)
    write_file('config.txt', 'Descryption_Data/config.txt', ['heelo', 'thure!'])