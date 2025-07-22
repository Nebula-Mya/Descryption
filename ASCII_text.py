from __future__ import annotations
from typing import Callable # prevent type hints needing import at runtime

import QoL
import os
import math

def print_title() -> None :
    title = '''
████████▄     ▄████████    ▄████████   ▄████████    ▄████████  ▄██   ▄      ▄███████▄     ███      ▄█   ▄██████▄   ███▄▄▄▄  
███   ▀███   ███    ███   ███    ███  ███    ███   ███    ███  ███   ██▄   ███    ███ ▀█████████▄ ███  ███    ███  ███▀▀▀██▄
███    ███   ███    █▀    ███    █▀   ███    █▀    ███    ███  ███▄▄▄███   ███    ███    ▀███▀▀██ ███▌ ███    ███  ███   ███
███    ███  ▄███▄▄▄       ███         ███         ▄███▄▄▄▄██▀  ▀▀▀▀▀▀███   ███    ███     ███   ▀ ███▌ ███    ███  ███   ███
███    ███ ▀▀███▀▀▀     ▀█████████▄   ███        ▀▀███▀▀▀▀▀    ▄██   ███ ▀█████████▀      ███     ███▌ ███    ███  ███   ███
███    ███   ███    █▄          ▀███  ███    █▄  ▀█████████▄   ███   ███   ███            ███     ███  ███    ███  ███   ███
███   ▄███   ███    ███    ▄█    ███  ███    ███   ███   ▀███  ███   ███   ███            ███     ███  ███    ███  ███   ███
████████▀    ██████████  ▄████████▀   ████████▀    ███    ███   ▀█████▀   ▄████▀         ▄████▀   █▀    ▀██████▀    ▀█   █▀ 
                                                   █▀     ██▀                                                               
{gap}An MS-DOS style demake of Daniel Mullins' "Inscryption"'''.format(gap=' '*66)

    print(QoL.center_justified(title, blocked=True))

def print_scales(score: dict[str, int], score_gap: int) -> None :
    player_adv = max(0, score['player'] - score['opponent'])
    opponent_adv = max(0, score['opponent'] - score['player'])
    if player_adv :
        player_weight = 'O'*player_adv + ' '*(5-player_adv)
        if len(player_weight) > 5 :
            player_weight = 'O'*5
        opponent_weight = ' '*5
    else :
        player_weight = ' '*5
        opponent_weight = ' '*(5-opponent_adv) + 'O'*opponent_adv
        if len(opponent_weight) > 5 :
            opponent_weight = 'O'*5
    

    scales = '''{spc}PLAYER  LESHY
{spc}{plr}   {lsh}
{spc}‾‾‾‾‾/‾\\‾‾‾‾‾
{spc}    /___\\'''.format(plr=player_weight, lsh=opponent_weight, spc=' '*score_gap)
    print(scales)

def print_win(overkill: int=0)  -> None:
    '''
    Prints the ASCII art for the win screen.
    
    Arguments:
        overkill: the amount of overkill damage, defaults to 0 (int)
    '''
    if overkill <= 0 :
        overkill_display = ''
    else :
        overkill_display = 'Overkill: {}\nTeeth: +{}'.format(overkill, overkill)
    win = '''
__/\\\\\\________/\\\\\\_______/\\\\\\\\\\_______/\\\\\\________/\\\\\\___________
 _\\///\\\\\\____/\\\\\\/______/\\\\\\///\\\\\\____\\/\\\\\\_______\\/\\\\\\___________
  ___\\///\\\\\\/\\\\\\/______/\\\\\\/__\\///\\\\\\__\\/\\\\\\_______\\/\\\\\\___________
   _____\\///\\\\\\/_______/\\\\\\______\\//\\\\\\_\\/\\\\\\_______\\/\\\\\\___________
    _______\\/\\\\\\_______\\/\\\\\\_______\\/\\\\\\_\\/\\\\\\_______\\/\\\\\\___________
     _______\\/\\\\\\_______\\//\\\\\\______/\\\\\\__\\/\\\\\\_______\\/\\\\\\___________
      _______\\/\\\\\\________\\///\\\\\\__/\\\\\\____\\//\\\\\\______/\\\\\\____________
       _______\\/\\\\\\__________\\///\\\\\\\\\\/______\\///\\\\\\\\\\\\\\\\\\/_____________
        _______\\///_____________\\/////__________\\/////////_______________
__/\\\\\\______________/\\\\\\__/\\\\\\\\\\\\\\\\\\\\\\__/\\\\\\\\\\_____/\\\\\\_____/\\\\\\____
 _\\/\\\\\\_____________\\/\\\\\\_\\/////\\\\\\///__\\/\\\\\\\\\\\\___\\/\\\\\\___/\\\\\\\\\\\\\\__
  _\\/\\\\\\_____________\\/\\\\\\_____\\/\\\\\\_____\\/\\\\\\/\\\\\\__\\/\\\\\\__/\\\\\\\\\\\\\\\\\\_
   _\\//\\\\\\____/\\\\\\____/\\\\\\______\\/\\\\\\_____\\/\\\\\\//\\\\\\_\\/\\\\\\_\\//\\\\\\\\\\\\\\__
    __\\//\\\\\\__/\\\\\\\\\\__/\\\\\\_______\\/\\\\\\_____\\/\\\\\\\\//\\\\\\\\/\\\\\\__\\//\\\\\\\\\\___
     ___\\//\\\\\\/\\\\\\/\\\\\\/\\\\\\________\\/\\\\\\_____\\/\\\\\\_\\//\\\\\\/\\\\\\___\\//\\\\\\____
      ____\\//\\\\\\\\\\\\//\\\\\\\\\\_________\\/\\\\\\_____\\/\\\\\\__\\//\\\\\\\\\\\\____\\///_____
       _____\\//\\\\\\__\\//\\\\\\_______/\\\\\\\\\\\\\\\\\\\\\\_\\/\\\\\\___\\//\\\\\\\\\\_____/\\\\\\____
        ______\\///____\\///_______\\///////////__\\///_____\\/////_____\\///_____
        
    {ovr}
'''.format(ovr=overkill_display)
    
    print(QoL.center_justified(win, blocked=True))

def print_lose(deck_out: bool=False)  -> None:
    '''
    Prints the ASCII art for the lose screen.
    
    Arguments:
        deck_out: whether the deck was emptied, defaults to False (bool)
    '''
    if deck_out :
        deck_out_display = 'You have been decked out.'
    else :
        deck_out_display = ''
    lose = '''
 ____________/\\\\\\________/\\\\\\_______/\\\\\\\\\\_______/\\\\\\________/\\\\\\___________
  ___________\\///\\\\\\____/\\\\\\/______/\\\\\\///\\\\\\____\\/\\\\\\_______\\/\\\\\\___________
   _____________\\///\\\\\\/\\\\\\/______/\\\\\\/__\\///\\\\\\__\\/\\\\\\_______\\/\\\\\\___________
    _______________\\///\\\\\\/_______/\\\\\\______\\//\\\\\\_\\/\\\\\\_______\\/\\\\\\___________
     _________________\\/\\\\\\_______\\/\\\\\\_______\\/\\\\\\_\\/\\\\\\_______\\/\\\\\\___________
      _________________\\/\\\\\\_______\\//\\\\\\______/\\\\\\__\\/\\\\\\_______\\/\\\\\\___________
       _________________\\/\\\\\\________\\///\\\\\\__/\\\\\\____\\//\\\\\\______/\\\\\\____________
        _________________\\/\\\\\\__________\\///\\\\\\\\\\/______\\///\\\\\\\\\\\\\\\\\\/_____________
         _________________\\///_____________\\/////__________\\/////////_______________
__/\\\\\\___________________/\\\\\\\\\\__________/\\\\\\\\\\\\\\\\\\\\\\____/\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_____/\\\\\\_________
 _\\/\\\\\\_________________/\\\\\\///\\\\\\______/\\\\\\/////////\\\\\\_\\/\\\\\\///////////____/\\\\\\\\\\\\\\_______
  _\\/\\\\\\_______________/\\\\\\/__\\///\\\\\\___\\//\\\\\\______\\///__\\/\\\\\\______________/\\\\\\\\\\\\\\\\\\______
   _\\/\\\\\\______________/\\\\\\______\\//\\\\\\___\\////\\\\\\_________\\/\\\\\\\\\\\\\\\\\\\\\\_____\\//\\\\\\\\\\\\\\_______
    _\\/\\\\\\_____________\\/\\\\\\_______\\/\\\\\\______\\////\\\\\\______\\/\\\\\\///////_______\\//\\\\\\\\\\________
     _\\/\\\\\\_____________\\//\\\\\\______/\\\\\\__________\\////\\\\\\___\\/\\\\\\_______________\\//\\\\\\_________
      _\\/\\\\\\______________\\///\\\\\\__/\\\\\\_____/\\\\\\______\\//\\\\\\__\\/\\\\\\________________\\///__________
       _\\/\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\____\\///\\\\\\\\\\/_____\\///\\\\\\\\\\\\\\\\\\\\\\/___\\/\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_____/\\\\\\_________
        _\\///////////////_______\\/////_________\\///////////_____\\///////////////_____\\///__________
        
    {deck}
'''.format(deck=deck_out_display)
    
    print(QoL.center_justified(lose, blocked=True))

def print_WiP() -> None :
    WiP = '''
 __________________________
|System             |–|‡‡|×|
|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|
|This feature is still     |
|in development. Sorry!    |
|                    - Neb |
 ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
'''

    print(QoL.center_justified(WiP, blocked=True))

def print_candelabra(wick_states: tuple[int, int, int])  -> None:
    '''
    Prints the ASCII art for the candelabra.
    
    Arguments:
        wick_states: the states of the wicks in the order middle, right, left (int, int, int)
            0 = unlit
            1 = lit (newly)
            2 = lit (continuing)
            3 = extinguished
    '''

    for state in wick_states :
        if state not in range(0,4) :
            raise ValueError
        
    wick_sprites = [
        [ # unlit
            '       ',
            '       ',
            '   |   ',
            'ˏ₋-|-₋ˎ',
            '|ˋ⁻⁻⁻ˊ|',
            '|     |'
        ],
        [ # lit (newly)
            '  /(   ',
            ' ( ;)ˎ ',
            ' \\(_)/ ',
            'ˏ₋-|-₋ˎ',
            '|ˋ⁻⁻⁻ˊ|',
            '|     |'
        ],
        [ # lit (continuing)
            '  /(   ',
            ' ( ;)ˎ ',
            ' \\(_)/ ',
            'ˏ₋-|-₋ˎ',
            '|ˋʅȷᵕȣ|',
            '| ₍₎ ᵕ|'
        ],
        [ # extinguished
            '       ',
            '     ʃ ',
            '   Ϛ᾽  ',
            'ˏ₋-|-₋ˎ',
            '|ˋ⁻⁻⁻ˊ|',
            '|     |'
        ]
    ]

    candelabra = r'''                       {0[0]}
                       {0[1]}
                       {0[2]}
                       {0[3]}
                       {0[4]}             {1[0]}
                       {0[5]}             {1[1]}
                       |     |             {1[2]}
                       |     |             {1[3]}
   {2[0]}             |     |             {1[4]}
   {2[1]}             |     |             {1[5]}
   {2[2]}             |     |             |     |
   {2[3]}             |     |             |     |
   {2[4]}             |     |             |     |
   {2[5]}            ˏ|     |ˎ            |     |
   |     |            |ˋ⁻⁻⁻⁻⁻ˊ|            |     |
   |     |            |       |            |     |
   |     |            |       |            |     |
   |     |            |       |\          ˏ|     |ˎ
   |     |            |       | 'ˌ        |ˋ⁻⁻⁻⁻⁻ˊ|
   |     |            |       |   ʽˎ      |       |
   |     |            |       |·ˌ   ˋ·.ˍ__|       |
  ˏ|     |ˎ          /|       |  ʽ.ˎ      |       |
  |ˋ⁻⁻⁻⁻⁻ˊ|        ˌ' |       |     ˋ·.ˍ__|       |
  |       |      ˏʼ   |       |           |       |
  |       |__ˍ.·ˊ   ˌ·|       |           |       |
  |       |      ˏ.ʼ  |       |           |       |
  |       |__ˍ.·ˊ     |       |           |       |
  |       |           |       |            ˋ⁻⁻⁻⁻⁻ˊ
  |       |           |       |
  |       |           |       |
  |       |           |       |
   ˋ⁻⁻⁻⁻⁻ˊ            |       |
                      |       |
                      |       |
                      |       |
                      |       |
                     ʃˋ⁻--―--⁻ˊʅ
 ˏ₋₋₋--------⁻⁻⁻⁻⁻⁻⁻ˊˋ⁻--―――--⁻ˊˋ⁻⁻⁻⁻⁻⁻⁻--------₋₋₋ˎ
ʃ                                                   ʅ
ˋ⁻⁻⁻-------₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋-------⁻⁻⁻ˊ
'''

    wicks = [wick_sprites[wick_states[0]], wick_sprites[wick_states[1]], wick_sprites[wick_states[2]]]

    print(QoL.center_justified(candelabra.format(*wicks), blocked=True))

def split_moon_lines(string: str) -> dict[str, list[list[str]]]:
    '''
    splits the moon card's inside into 20 lines of various characters

    Arguments:
        string: the string to split (str)
    
    Returns:
        split_lines: the dictionary of split lines
        {
            'cards': [
                [card_1, card_2, card_3, card_4],
                ...
            ],
            'connectors': [
                [connector_1, connector_2, connector_3, connector_4],
                ...
            ]
        }
    '''
    # get the terminal width
    term_cols = os.get_terminal_size().columns
    gaps = (term_cols*55 // 100) // 5 - 15

    split_string: Callable[[str, int], tuple[str, str]] = lambda string, length : (string[:max(length, 0)], string[max(length, 0):])

    # set up variables
    split_lines: dict[str, list[list[str]]] = {
        'cards' : [],
        'connectors' : []
    }
    lines = string.split('\n')

    for line in lines :
        (card_1, line) = split_string(line, 13)
        card_1 = card_1.ljust(13)
        (connections_1, line) = split_string(line, gaps*3)
        connections_1 = connections_1.ljust(gaps*3)
        (card_2, line) = split_string(line, 15)
        card_2 = card_2.ljust(15)
        (connections_2, line) = split_string(line, gaps*3)
        connections_2 = connections_2.ljust(gaps*3)
        (card_3, line) = split_string(line, 15)
        card_3 = card_3.ljust(15)
        (connections_3, line) = split_string(line, gaps*3)
        connections_3 = connections_3.ljust(gaps*3)
        (card_4, line) = split_string(line, 13)
        card_4 = card_4.ljust(13)
        split_lines['cards'].append([card_1, card_2, card_3, card_4])
        split_lines['connectors'].append([' '*gaps*3, connections_1, connections_2, connections_3])
    
    return split_lines

def moon_inner_str() -> str:
    gap_num = (os.get_terminal_size().columns*55 // 100) // 5 - 15
    gap = ' '*gap_num
    gap_half = ' '*(gap_num // 2)
    gap_center = gap*4 + gap_half
    gap_half_up = ' '*math.ceil(gap_num / 2)
    connect = gap*3
    moon_str = r'''——————              ,—,  ,—,
‾‾][‾‾ || || |[⁼⁼   ||\\//|| ,¡˭˭¡, ,¡˭˭¡, |[\ ||
  ||   |[=]| |[==   || \/ || ||  || ||  || ||\\||
  ||   || || |[₌₌   ||    || '!‗‗!' '!‗‗!' || \]|
{connect}{connect}                                                 _
 {connect}      ˌ___/\___ˌ           {connect}                    //,
 {connect} ʅ——₋ˎ|        |           {connect}                .-⁻⁻//.
 {connect}  ʅ_  ‾‾ˋ·ˎ    |           {connect}               ʃ   // ʅ
 {connect}   ʅ_(‾∂  :    /           {connect}               ʅ  //  ʃ
 {connect}      `⁻ˎˊ   ˏʼ            {connect}                ·//--·
 {connect}         ˋ··ˊ              {connect}               //’
                {gap_center}         .-⁻⁻-.         {gap}{gap_half_up}   ‾
                {gap_center}        ʃ      ʅ        {gap_center}
                {gap_center}      _ ʅ      ʃ _      {gap_center}
                {gap_center}     /ʃ  ·-₋₋-·  ʅ\     {gap_center}
                {gap_center}     ||  /|  |\  ||     {gap_center}
                {gap_center}     ||  ||  ||  ||     {gap_center}
                {gap_center}    \‾‾/\‾‾/\‾‾/\‾‾/    {gap_center}
                {gap_center}     \/  \/  \/  \/     {gap_center}
'''

    return moon_str.format(gap=gap, gap_half=gap_half, gap_half_up=gap_half_up, gap_center=gap_center, connect=connect)
    
def moon_life_lines(life: int) -> list[str] :
    '''
    generates a 7x3 ASCII representation of the moon's life (2 digits)

    bounds the value between 0 and 99 (inclusive)

    Arguments:
        life: the moon's life (int)
    
    Returns:
        life_lines: the ASCII representation of the moon's life (list)
    '''
    number_ASCII_lines = {
        0: ['ˌ_ˌ', '| |', '|_|'],
        1: [' ˌ ', '/| ', '_|_'],
        2: ['ˌ_ ', ' _|', '|_ˌ'],
        3: ['ˌ_ ', ' _|', 'ˌ_|'],
        4: ['ˌ ˌ', '|_|', '  |'],
        5: ['ˌ_ˌ', '|_ ', 'ˌ_|'],
        6: [' _ˌ', '|_ ', '|_|'],
        7: ['__ˌ', '  /', ' / '],
        8: [' _ ', '|_|', '|_|'],
        9: [' _ ', '|_|', 'ˌ_|']
    }
    
    life = max(0, min(life, 99))

    tens = life // 10
    ones = life % 10

    if tens == 0 :
        left_ASCII_lines = number_ASCII_lines[ones]
        right_ASCII_lines = [' '*3]*2
    else :
        left_ASCII_lines = number_ASCII_lines[tens]
        right_ASCII_lines = number_ASCII_lines[ones]

    life_lines = [line_l + ' ' + line_r for line_l, line_r in zip(left_ASCII_lines, right_ASCII_lines)]

    return life_lines

moon_parts = { # organized by row (2=bushes, 1=field) then column (1=left - 4=right)
    2 : {
        1 : r''',--------------
| {moon_lines[0]}
| {moon_lines[1]}
| {moon_lines[2]}
| {moon_lines[3]}
| {moon_lines[4]}
| {moon_lines[5]}
| {moon_lines[6]}
| {moon_lines[7]}
| {moon_lines[8]}
| {moon_lines[9]}''',
        2 : r'''---------------
{moon_lines[0]}
{moon_lines[1]}
{moon_lines[2]}
{moon_lines[3]}
{moon_lines[4]}
{moon_lines[5]}
{moon_lines[6]}
{moon_lines[7]}
{moon_lines[8]}
{moon_lines[9]}''',
        3 : r'''---------------
{moon_lines[0]}
{moon_lines[1]}
{moon_lines[2]}
{moon_lines[3]}
{moon_lines[4]}
{moon_lines[5]}
{moon_lines[6]}
{moon_lines[7]}
{moon_lines[8]}
{moon_lines[9]}''',
        4 : r'''--------------,
{moon_lines[0]} |
{moon_lines[1]} |
{moon_lines[2]} |
{moon_lines[3]} |
{moon_lines[4]} |
{moon_lines[5]} |
{moon_lines[6]} |
{moon_lines[7]} |
{moon_lines[8]} |
{moon_lines[9]} |'''
    },
    1 : {
        1 : r'''| {moon_lines[0]}
| {moon_lines[1]}
| {moon_lines[2]}
| {moon_lines[3]}
| {moon_lines[4]}
| {moon_lines[5]}
| {moon_lines[6]}
| {moon_lines[7]}
| {moon_lines[8]}
| {moon_lines[9]}
'--------------''',
        2 : r'''{moon_lines[0]}
{moon_lines[1]}
{moon_lines[2]}
{moon_lines[3]}
{moon_lines[4]}
{moon_lines[5]}
{moon_lines[6]}
{moon_lines[7]}
{moon_lines[8]}
{moon_lines[9]}
---------------''',
        3 : r'''{moon_lines[0]}
{moon_lines[1]}
{moon_lines[2]}
{moon_lines[3]}
{moon_lines[4]}
{moon_lines[5]}
{moon_lines[6]}
{moon_lines[7]}
{moon_lines[8]}
{moon_lines[9]}
---------------''',
        4 : r"""{moon_lines[0]} |
{moon_lines[1]} |
{moon_lines[2]} |
{moon_lines[3]} |
{moon_lines[4]} |
 ˌ    //      |
/|   //       |
_|_ //{life_lines[0]} |
   // {life_lines[1]} |
  //  {life_lines[2]} |
--------------'""",
    }
}