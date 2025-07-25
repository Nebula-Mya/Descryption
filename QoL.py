from __future__ import annotations # prevent type hints needing import at runtime
from typing import TYPE_CHECKING, Callable
if TYPE_CHECKING:
    import card
    from typing import Any

import math
import os
import sys
import json
import random
import copy

def clear() -> None :
    '''
    clears the console
    '''
    if os.name == 'nt' : # windows
        os.system('cls')
    else : # mac/linux
        os.system('clear')

def read_data(data_to_read: list[list[str]]) -> list[Any]:
    '''
    reads the specified data from the config file

    Arguments:
        data_to_read: the data to read, where subsequent keys are ordered by depth in a sublist (list[list])
    
    Returns:
        the specified data from the config file (list)
    '''
    def get_data_value(data_keys: list[str], data: dict[str, Any]) -> Any :
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

def write_data(data_to_write: list[tuple[list, Any]]) -> None :
    '''
    writes the specified data to the config file
    
    Arguments:
        data_to_write: the data to write, where subsequent keys are ordered by depth (list[tuple][list, any])
    '''
    def set_data_value(data_keys: list[str], value_to_set: Any, data: dict[str, Any]) -> None :
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

def center_justified(text: str, blocked: bool=False, shift: int=0) -> str :
    '''
    centers text in the console

    Arguments:
        text: the text to center (str)
        blocked: whether to center the text in a blocked manner, defaults to False (bool)
        shift: the amount to shift the text to the right, defaults to 0 (int)
    
    Returns:
        the centered text (str)
    '''
    # set up variables
    text_lines = text.split('\n')
    # text_lines = [line.lstrip() for line in text.split('\n')]
    term_width = os.get_terminal_size().columns
    center_space: Callable[[int], int] = lambda line_width : (term_width - line_width) // 2
    centered_text = ''

    if blocked :
        text_width = max([len(line) for line in text_lines])

        for line in text_lines :
            centered_text += ' ' * (center_space(text_width) + shift) + line + '\n'
    
    else :
        for line in text_lines :
            text_width = len(line)

            centered_text += ' ' * (center_space(text_width) + shift) + line + '\n'
    
    return centered_text

def split_nicely(text: str, first_line_length: int, gen_line_length: int, max_lines: int=10, add_blank_lines: bool=False) -> list[str] :
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

def title_case(string: str) -> str :
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

def exec_sigil_code(current_card: card.BlankCard, applicables: list[str], global_vars: None|dict[str, Any]=None, local_vars: dict[str, Any] = {}, vars_to_return: list[Any]=[]) -> list[Any]:
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
    
    def get_combo_code(sigil: tuple[str, str]) -> str :
        '''
        get the code block for a combination of sigils
        
        Arguments:
            sigil: the sigils to combine (list[str])
        
        Returns:
            the code block (str)
        '''
        if len(sigil) != 2 : raise ValueError

        # imports
        import sigils

        # sort sigils
        combo: tuple[str, str] = tuple(sorted(sigil)) # type: ignore (error prevents this)

        # get code block
        return sigils.Combos.get(combo, "")
    
    # imports
    import sigils

    # set up variables
    code_block = ''
    local_vars['applicables'] = applicables

    # get code to execute
    if all(x in applicables for x in current_card.sigils) :
        code_block = get_combo_code(current_card.sigils)
    else :
        for sigil in current_card.sigils :
            if sigil in applicables :
                code_block = sigils.Dict[sigil][2]
                break

    if code_block != '' :
        exec(code_block, global_vars, local_vars)

    returned_vars = [local_vars[var] for var in vars_to_return]

    return returned_vars

def hefty_check(field: dict[int, card.BlankCard], zone: int, direction: str) -> int :
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
            edge_check = zone < 4
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

def sort_deck(deck: list[card.BlankCard]) -> list[card.BlankCard] :
    '''
    sorts a deck by cost and name

    Arguments:
        deck: the deck to sort (list)
    
    Returns:
        the sorted deck (list)
    '''
    deck = sorted(deck, key=lambda x: x.sigils) # sort by sigils
    deck = sorted(deck, key=lambda x: x.name) # sort by name (will be sub-sorting under cost)
    return sorted(deck, key=lambda x: x.saccs)

def print_deck(deck: list[card.BlankCard], sort: bool=False, numbered: bool=False, centered: bool=False, blocked: bool=False, silent: bool=False, exact_card_gap: None | int = None, beginning_space: bool = True, max_card_width: int = 6) -> str:
    '''
    prints a list of cards in a deck, with optional sorting

    Arguments:
        deck: deck to print (list)
        sort: whether to sort the deck before printing (bool)
        numbered: whether to number the cards (bool)
        centered: whether to center the deck (bool)
        blocked: whether to block the deck when centered (bool)
        silent: whether to prevent the str from being printed (bool)
    '''
    def card_gap_numbered(card_gaps: int, number: int) -> str :
        number_str = str(number)
        return ' ' * (card_gaps - len(number_str) - 1) + number_str + ' '
    
    def line_str(line: int, card_gaps: int, row: list[card.BlankCard], numbered: bool) -> str:
        if numbered :
            card_gaps = max(card_gaps, 4)
        card_gaps_space: str = ' ' * card_gaps

        if line == 0 and numbered :
            text: str = ''
            for card in row :
                text += card_gap_numbered(card_gaps, card_number[0]) + card.text_by_line()
                card_number[0] += 1
        else :
            if numbered or beginning_space : text = card_gaps_space
            else : text = ""
            text += card_gaps_space.join(card.text_by_line() for card in row)

        if centered or numbered :
            return text
        return text
    
    # set up variables
    card_number = [1]
    
    # get terminal size
    term_cols = os.get_terminal_size().columns
    max_width = term_cols*80 // 100
    indent = min((term_cols - max_width) // 2, 4)
    if numbered :
        cards_per_row = min(max_width // 19, max_card_width)
    else :
        cards_per_row = min(max_width // 15, max_card_width)
    if exact_card_gap == None:
        card_gaps = max_width // cards_per_row - 15
    else : card_gaps = exact_card_gap

    # sort deck if needed
    if sort :
        deck = sort_deck(deck)

    # split deck into rows
    chunked = [deck[i:i + cards_per_row] for i in range(0, len(deck), cards_per_row)]

    # generate deck string
    deck_string = ''
    for row in chunked :
        line_strings = [line_str(line, card_gaps, row, numbered) for line in range(11)]
        prefix = '\n' + ' '*indent
        deck_string += prefix + prefix.join(line_strings)

    if centered :
        deck_string = center_justified(deck_string, blocked, -2)
        
    if not silent :
        print(deck_string)

    return deck_string
    
def reps_int(string: str, increment: int=0) -> tuple[bool, int] :
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

def bind_int(value: int, lower_bound: float|int=-math.inf, upper_bound: float|int=math.inf) -> int:
    '''
    binds an integer to a range (inclusive)

    when one unspecified bound is given, it is taken as the floor
    when two unspecified bounds are given, the first is taken as the floor and the second as the ceiling

    Arguments:
        value: the integer to bind (int)
        lower_bound: the lower bound to bind to, defaults to -math.inf (int)
        upper_bound: the upper bound to bind to, defaults to math.inf (int)
    '''
    # error handling
    if type(value) != int :
        raise TypeError('value must be an integer')
    if lower_bound > upper_bound :
        raise ValueError('lower bound must be less than or equal to upper bound')
    if lower_bound != -math.inf and type(lower_bound) != int :
        raise TypeError('lower bound must be an integer')
    if upper_bound != math.inf and type(upper_bound) != int :
        raise TypeError('upper bound must be an integer')
    
    match (lower_bound != -math.inf, upper_bound != math.inf) :
        case (True, False) : # only lower bound
            return int(max(value, lower_bound))
        case (False, True) : # only upper bound
            return int(min(value, upper_bound))
        case (True, True) : # both bounds
            return int(min(max(value, lower_bound), upper_bound))
        case _ : # misc errors
            raise ValueError('invalid bounds')

def ping(dict: dict[Any, Any]={'ping':'pong'}) -> None : # for testing
    '''
    writes variables to ping.txt

    Arguments:
        dict: the variables to write (dict)
    '''
    def depth(object: Any) -> int:
        '''
        gets the depth of a list or dictionary

        1 is a flat list or dictionary

        Arguments:
            object: the object to check

        Returns:
            the depth of the object (int)
        '''
        if type(object) not in [dict, list] :
            return 0

        return 1 + max([depth(value) for value in object.values()])

    def format_list(list: list[Any]) -> list[str] :
        '''
        formats a list as a string with lines and indentation

        Arguments:
            list: the list to format (list)

        Returns:
            the formatted list (str)
        '''
        lines = ['[']
        for item in list :
            if item == list[-1] : comma = ''
            else : comma = ','

            if type(item) == type({}) : 
                item = format_dict(item)
            elif type(item) == type([]) : 
                item = format_list(item)
            elif type(item) == type("") :
                item = [f"\'{item}\'"]
            else :
                item = [item]
            
            for line in item :
                if line == item[0] and len(item) != 1 :
                    lines.append(f"    {line}")
                elif line == item[-1] :
                    lines.append(f"    {line}{comma}")
                else :
                    lines.append(f"    {line}")

        lines.append(']')

        return lines

    def format_dict(dictionary: dict[Any, Any])  -> list[str] :
        '''
        formats a dictionary as a string with lines and indentation

        Arguments:
            dictionary: the dictionary to format (dict)

        Returns:
            the formatted dictionary (str)
        '''
        lines = ['{']
        for key in dictionary :
            if key == list(dictionary.keys())[-1] : comma = ''
            else : comma = ','

            if type(dictionary[key]) == type({}) :
                value = format_dict(dictionary[key])
            elif type(dictionary[key]) == type([]) :
                value = format_list(dictionary[key])
            elif type(dictionary[key]) == type("") :
                value = [f"\'{dictionary[key]}\'"]
            else :
                value = [dictionary[key]]
            
            for line in value :
                if line == value[0] and len(value) == 1 :
                    lines.append(f"    {key}: {line}{comma}")
                elif line == value[0] :
                    lines.append(f"    {key}: {line}")
                elif line == value[-1] :
                    lines.append(f"    {line}{comma}")
                else : 
                    lines.append(f"    {line}")

        lines.append('}')

        return lines

    def format_values(dictionary: dict[Any, Any])  -> dict[Any, str]:
        '''
        formats the values of a dictionary as strings with lines and indentation

        Arguments:
            dictionary: the dictionary to format (dict)
        '''
        for key in dictionary :
            if type(dictionary[key]) == type({}) :
                dictionary[key] = '\n'.join(format_dict(dictionary[key]))
            elif type(dictionary[key]) == type([]) :
                dictionary[key] = '\n'.join(format_list(dictionary[key]))
        
        return dictionary

    ### to do: clean the output (split dicts and lists across lines, indent, etc.)
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS') : # guard clause to prevent pinging after compilation
        return
    
    # format values for writing
    locals = format_values(dict)

    # get string of local variables
    data_to_write = '\n\n'.join(f"{key}: {value}" for key, value in locals.items()).rstrip()
    
    with open('ping.txt', 'w') as file :
        file.write(data_to_write)

def random_card(possible_cards: list[type[card.BlankCard]] | dict[int, list[type[card.BlankCard]]], weighted: bool=True, alpha: float=2.2, beta: float=3.3, few_rare: bool=True, hidden_cost: bool=False) -> card.BlankCard:
    '''
    gets a random card from a set of possible cards

    Arguments:
        possible_cards: the cards to choose from (list or dict)
        weighted: whether to weight the chances of cards based on cost, defaults to True (bool)
        alpha: the alpha value for the beta distribution, defaults to 2.2 (float)
        beta: the beta value for the beta distribution, defaults to 3.3 (float)
        few_rare: whether to lower the chances of rare cards, defaults to True (bool)
        hidden_cost: whether to hide the cost of the card, defaults to False (bool)

    Returns:
        the randomly chosen card (Card object)
    '''
    # imports (to prevent circular imports)
    import card_library
    import math

    # set up variables
    if type(possible_cards)==list :
            card_dict = {0: [card_ for card_ in possible_cards]}
    elif type(possible_cards)==dict :
        if weighted :
            card_dict = possible_cards
        else :
            all_cards = []
            for key in possible_cards :
                all_cards += [card for card in possible_cards[key]]
            card_dict = {0: [card_ for card_ in all_cards]}
    else : raise ValueError('Invalid possible_cards type')

    # get cost
    if weighted:
        cost_values = list(card_dict)
        cost_values.sort()
        cost: Callable[[], int] = lambda : cost_values[math.floor((cost_values.__len__()) * random.betavariate(alpha, beta))]
    else : cost: Callable[[], int] = lambda : random.choice(list(card_dict.keys()))

    # get card type
    template_card: type[card.BlankCard] = random.choice(card_dict[cost()])
    if few_rare and template_card in card_library.Rare_Cards: # lower chances of rare cards
        template_card = random.choice(card_dict[cost()])

    # return
    return copy.deepcopy(template_card(blank_cost=hidden_cost))