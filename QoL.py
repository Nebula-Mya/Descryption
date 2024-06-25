import os
import sys
import json

def clear() :
    '''
    clears the console
    '''
    if os.name == 'nt' : # windows
        os.system('cls')
    else : # mac/linux
        os.system('clear')

def read_data(data_to_read) :
    '''
    reads the specified data from the config file

    Arguments:
        data_to_read: the data to read, where subsequent keys are ordered by depth in a sublist (list[list])
    
    Returns:
        the specified data from the config file (list)
    '''
    def get_data_value(data_keys, data) :
        '''
        gets the value from the config file using a list of subsequent keys
    
        Arguments:
            data_keys: the list of subsequent keys (list)
            data: the data to search (dict)

        Returns:
            the value at the specified path in the config file, or None if the path is invalid (any)
        '''
        if data_keys == [] : # base case: all keys have been processed
            return data
        
        key = data_keys[0] # get the next key

        if key in data : # recursive call with the next level
            return get_data_value(data_keys[1:], data[key])
        
        raise KeyError(f'Key not found: {key}') # key not found
    
    # get path to config file
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS') :
        data_file = "Descryption_Data/config.json"
    else:
        data_file = "config.json"

    # get data from config file
    with open(data_file, 'r') as file :
        data = json.load(file)
        data_to_return = [get_data_value(data_path, data) for data_path in data_to_read]
        return data_to_return

def write_data(data_to_write) :
    '''
    writes the specified data to the config file
    
    Arguments:
        data_to_write: the data to write, where subsequent keys are ordered by depth (list[tuple][list, any])
    '''
    def set_data_value(data_keys, value_to_set, data) :
        '''
        sets a value in the config file using a list of subsequent keys

        Arguments:
            data_keys: the list of subsequent keys leading to the value (list)
            value_to_set: the value to set at the specified path (any)
            data: the data dictionary to update (dict)
        '''
        for key in data_keys[:-1] :  # navigate to the last key's parent dictionary
            if key not in data:
                data[key] = {}  # create a new dict if the key doesn't exist

            data = data[key] # move to the next value
        
        data[data_keys[-1]] = value_to_set  # set the value

    # get path to config file
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS') :
        data_file = "Descryption_Data/config.json"
    else:
        data_file = "config.json"

    # get data from config file
    try :
        with open(data_file, 'r') as file :
            data = json.load(file)
    except FileNotFoundError :
        data = {}

    # write data to dictionary
    for data_path, value in data_to_write :
        set_data_value(data_path, value, data)

    # write dictionary to config file
    with open(data_file, 'w') as file :
        json.dump(data, file, indent=4)

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
    # set up variables
    lines = []

    if len(text) > first_line_length :
        if text[:first_line_length][-1] == ' ' : # if the first line is too long, split it
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
            if text[:gen_line_length][-1] == ' ' : # if the text is too long, split it
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

    if len(lines) > max_lines : # add ellipsis if text is too long
        lines = lines[:max_lines]
        lines[-1] = lines[-1][:-3] + '...'

    if add_blank_lines and len(lines) < max_lines : # add blank lines if needed
        for i in range(max_lines - len(lines)) :
            lines.append('')

    return lines

def title_case(string) :
    '''
    converts a string to title case

    Arguments:
        string: the string to convert (str)
    
    Returns:
        the title cased string (str)
    '''
    # set up variables
    words = string.split()
    lower_words = ['and', 'or', 'the', 'a', 'an', 'of', 'in', 'on', 'at', 'to', 'with', 'from', 'by', 'as', 'for', 'but', 'nor', 'so', 'yet']

    # convert to title case
    title_cased_words = [words[0].capitalize()] + [word.capitalize() if word not in lower_words else word for word in words[1:]]
    return ' '.join(title_cased_words)

def exec_sigil_code(current_card, applicables, global_vars=None, local_vars=None, vars_to_return=[]) :
    '''
    executes sigil code
    
    Arguments:
        current_card: the card to execute the sigil code for (Card)
        applicables: the sigils to execute (list)
        global_vars: the global variables to use (dict)
        local_vars: the local variables to use (dict)
        vars_to_return: the variables to return (list[str])
    
    Returns:
        the variables to return (list)
    '''
    
    def get_combo_code(sigil) :
        '''
        get the code block for a combination of sigils
        
        Arguments:
            sigil: the sigils to combine (list[str])
        
        Returns:
            the code block (str)
        '''
        # imports
        import sigils

        # sort sigils
        combo = tuple(sorted(sigil))

        # get code block
        return sigils.Combos.get(combo, None)
    
    # imports
    import sigils

    # get code to execute
    if len(current_card.sigil) == 2 and all(x in applicables for x in current_card.sigil) :
        code_block = get_combo_code(current_card.sigil)
    else :
        for sigil in current_card.sigil :
            if sigil in applicables :
                code_block = sigils.Dict[sigil][2]
                break

    if code_block != '' :
        exec(code_block, global_vars, local_vars)

    returned_vars = [local_vars[var] for var in vars_to_return]

    return returned_vars

def hefty_check(field, zone, direction) :
    '''
    recursively checks how many cards can be pushed by a card with hefty sigil

    Arguments:
        field: the field to check (dict)
        zone: the zone to check (int)
        direction: the direction to check (str)
    
    Returns:
        the number of cards that can be pushed, -1 being an open zone adjacent to the card with hefty (int)
    '''
    # set up variables
    match direction :
        case 'right' :
            edge_check = zone < 5
            dir_shift = 1
        case 'left' :
            edge_check = zone > 1
            dir_shift = -1
        case _ :
            raise ValueError('Invalid direction')

    # get number of cards that can be pushed
    if field[zone].species == '' : # only when the card after the card with hefty is empty
        return -1
    match field[zone + dir_shift].species : # check the next card
        case '' if edge_check :
            return 1
        case _ if edge_check :
            hefty_count = hefty_check(field, zone + dir_shift, direction)
            if hefty_count == 0 :
                return 0
            return 1 + hefty_count
        case _ :
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
    chunked = [deck[i:i + cards_per_row] for i in range(0, len(deck), cards_per_row)]
    
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
        whether the string is an integer (bool), the integer (int)
    '''
    try : # check if the string is an integer
        return True, int(string) + increment
    except ValueError : # if not, default to 0 and return False
        return False, 0

def sigil_in_category(sigil, category) :
    '''
    checks if a sigil is in a category

    Arguments:
        sigil: the sigil(s) to check (list[str])
        category: the category to check (dict)
    
    Returns:
        whether the sigil is in the category (bool)
    '''
    match len(sigil) :
        case 1 :
            return sigil[0] in category
        case 2 :
            return sigil[0] in category or sigil[1] in category
        case _ :
            raise ValueError('Sigil must be a list of length 1 or 2')

def ping(locals={'ping':'pong'}) : # for testing
    '''
    writes local variables to ping.txt

    Arguments:
        locals: the local variables to write (dict)
    '''
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS') : # guard clause to prevent pinging after compilation
        return
    
    # get string of local variables
    data_to_write = '\n\n'.join(f"{key}: {value}" for key, value in locals.items()).rstrip()
    
    with open('ping.txt', 'w') as file :
        file.write(data_to_write)

if __name__ == '__main__' :
    clear()

    # get original values
    [play_var, oro_attack] = read_data([['settings', 'difficulty', 'leshy plays variance'], ['ouroboros', 'attack']])

    # change values
    data_to_write = [
        (['settings', 'difficulty', 'leshy plays variance'], 5),
        (['ouroboros', 'attack'], 10)
    ]
    write_data(data_to_write)

    read_data([['settings']])
    read_data([['settings', 'hand size'], ['ouroboros', 'attack']])

    # return to original values
    data_to_write = [
        (['settings', 'difficulty', 'leshy plays variance'], play_var),
        (['ouroboros', 'attack'], oro_attack)
    ]
    write_data(data_to_write)