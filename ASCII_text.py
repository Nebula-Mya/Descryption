import QoL
import os

def print_title() :
    term_cols = os.get_terminal_size().columns
    center_space = (term_cols - 124) // 2
    title = '''
{spc}████████▄     ▄████████    ▄████████   ▄████████    ▄████████  ▄██   ▄      ▄███████▄     ███      ▄█   ▄██████▄   ███▄▄▄▄  
{spc}███   ▀███   ███    ███   ███    ███  ███    ███   ███    ███  ███   ██▄   ███    ███ ▀█████████▄ ███  ███    ███  ███▀▀▀██▄
{spc}███    ███   ███    █▀    ███    █▀   ███    █▀    ███    ███  ███▄▄▄███   ███    ███    ▀███▀▀██ ███▌ ███    ███  ███   ███
{spc}███    ███  ▄███▄▄▄       ███         ███         ▄███▄▄▄▄██▀  ▀▀▀▀▀▀███   ███    ███     ███   ▀ ███▌ ███    ███  ███   ███
{spc}███    ███ ▀▀███▀▀▀     ▀█████████▄   ███        ▀▀███▀▀▀▀▀    ▄██   ███ ▀█████████▀      ███     ███▌ ███    ███  ███   ███
{spc}███    ███   ███    █▄          ▀███  ███    █▄  ▀█████████▄   ███   ███   ███            ███     ███  ███    ███  ███   ███
{spc}███   ▄███   ███    ███    ▄█    ███  ███    ███   ███   ▀███  ███   ███   ███            ███     ███  ███    ███  ███   ███
{spc}████████▀    ██████████  ▄████████▀   ████████▀    ███    ███   ▀█████▀   ▄████▀         ▄████▀   █▀    ▀██████▀    ▀█   █▀ 
{spc}                                                   █▀     ██▀                                                               
{spc}{gap}An MS-DOS style demake of Daniel Mullin's "Inscryption"   '''.format(spc=' '*center_space, gap=' '*66)
    print(title)

def print_scales(score) :
    term_cols = os.get_terminal_size().columns
    card_gaps = (term_cols*55 // 100) // 5 - 15
    if card_gaps <= 0 :
        score_gap = 28
    else :
        score_gap = card_gaps*9 + 28

    player_adv = max(0, score['player'] - score['opponent'])
    opponent_adv = max(0, score['opponent'] - score['player'])
    if player_adv :
        player_weight = 'O'*player_adv + ' '*(8-player_adv)
        opponent_weight = ' '*8
    else :
        player_weight = ' '*8
        opponent_weight = ' '*opponent_adv + 'O'*opponent_adv
    

    scales = '''{spc} PLAYER      LESHY
{spc}{plr}   {lsh}
{spc}‾‾‾‾‾‾‾‾/‾\\‾‾‾‾‾‾‾‾
{spc}       /___\\'''.format(plr=player_weight, lsh=opponent_weight, spc=' '*score_gap)
    print(scales)

def print_win(overkill=0) :
    '''
    Prints the ASCII art for the win screen.
    
    Arguments:
        overkill: the amount of overkill damage, defaults to 0 (int)
    '''
    term_cols = os.get_terminal_size().columns
    center_space = (term_cols - 85) // 2
    if overkill <= 0 :
        overkill_display = ''
    else :
        overkill_display = '\n'*2+' '*(center_space+4)+'Overkill: {}'.format(overkill)
    win = '''
{spc}__/\\\\\\________/\\\\\\_______/\\\\\\\\\\_______/\\\\\\________/\\\\\\___________
{spc} _\\///\\\\\\____/\\\\\\/______/\\\\\\///\\\\\\____\\/\\\\\\_______\\/\\\\\\___________
{spc}  ___\\///\\\\\\/\\\\\\/______/\\\\\\/__\\///\\\\\\__\\/\\\\\\_______\\/\\\\\\___________
{spc}   _____\\///\\\\\\/_______/\\\\\\______\\//\\\\\\_\\/\\\\\\_______\\/\\\\\\___________
{spc}    _______\\/\\\\\\_______\\/\\\\\\_______\\/\\\\\\_\\/\\\\\\_______\\/\\\\\\___________
{spc}     _______\\/\\\\\\_______\\//\\\\\\______/\\\\\\__\\/\\\\\\_______\\/\\\\\\___________
{spc}      _______\\/\\\\\\________\\///\\\\\\__/\\\\\\____\\//\\\\\\______/\\\\\\____________
{spc}       _______\\/\\\\\\__________\\///\\\\\\\\\\/______\\///\\\\\\\\\\\\\\\\\\/_____________
{spc}        _______\\///_____________\\/////__________\\/////////_______________
{spc}__/\\\\\\______________/\\\\\\__/\\\\\\\\\\\\\\\\\\\\\\__/\\\\\\\\\\_____/\\\\\\_____/\\\\\\____
{spc} _\\/\\\\\\_____________\\/\\\\\\_\\/////\\\\\\///__\\/\\\\\\\\\\\\___\\/\\\\\\___/\\\\\\\\\\\\\\__
{spc}  _\\/\\\\\\_____________\\/\\\\\\_____\\/\\\\\\_____\\/\\\\\\/\\\\\\__\\/\\\\\\__/\\\\\\\\\\\\\\\\\\_
{spc}   _\\//\\\\\\____/\\\\\\____/\\\\\\______\\/\\\\\\_____\\/\\\\\\//\\\\\\_\\/\\\\\\_\\//\\\\\\\\\\\\\\__
{spc}    __\\//\\\\\\__/\\\\\\\\\\__/\\\\\\_______\\/\\\\\\_____\\/\\\\\\\\//\\\\\\\\/\\\\\\__\\//\\\\\\\\\\___
{spc}     ___\\//\\\\\\/\\\\\\/\\\\\\/\\\\\\________\\/\\\\\\_____\\/\\\\\\_\\//\\\\\\/\\\\\\___\\//\\\\\\____
{spc}      ____\\//\\\\\\\\\\\\//\\\\\\\\\\_________\\/\\\\\\_____\\/\\\\\\__\\//\\\\\\\\\\\\____\\///_____
{spc}       _____\\//\\\\\\__\\//\\\\\\_______/\\\\\\\\\\\\\\\\\\\\\\_\\/\\\\\\___\\//\\\\\\\\\\_____/\\\\\\____
{spc}        ______\\///____\\///_______\\///////////__\\///_____\\/////_____\\///_____{ovr}
'''.format(spc=' '*center_space, ovr=overkill_display)
    print(win)

def print_lose(deck_out=False) :
    '''
    Prints the ASCII art for the lose screen.
    
    Arguments:
        deck_out: whether the deck was emptied, defaults to False (bool)
    '''
    term_cols = os.get_terminal_size().columns
    center_space = (term_cols - 100) // 2
    if deck_out :
        deck_out_display = '\n'*2 + ' '*(center_space+4) + 'You have been decked out.'
    else :
        deck_out_display = ''
    lose = '''
{spc} ____________/\\\\\\________/\\\\\\_______/\\\\\\\\\\_______/\\\\\\________/\\\\\\___________
{spc}  ___________\\///\\\\\\____/\\\\\\/______/\\\\\\///\\\\\\____\\/\\\\\\_______\\/\\\\\\___________
{spc}   _____________\\///\\\\\\/\\\\\\/______/\\\\\\/__\\///\\\\\\__\\/\\\\\\_______\\/\\\\\\___________
{spc}    _______________\\///\\\\\\/_______/\\\\\\______\\//\\\\\\_\\/\\\\\\_______\\/\\\\\\___________
{spc}     _________________\\/\\\\\\_______\\/\\\\\\_______\\/\\\\\\_\\/\\\\\\_______\\/\\\\\\___________
{spc}      _________________\\/\\\\\\_______\\//\\\\\\______/\\\\\\__\\/\\\\\\_______\\/\\\\\\___________
{spc}       _________________\\/\\\\\\________\\///\\\\\\__/\\\\\\____\\//\\\\\\______/\\\\\\____________
{spc}        _________________\\/\\\\\\__________\\///\\\\\\\\\\/______\\///\\\\\\\\\\\\\\\\\\/_____________
{spc}         _________________\\///_____________\\/////__________\\/////////_______________
{spc}__/\\\\\\___________________/\\\\\\\\\\__________/\\\\\\\\\\\\\\\\\\\\\\____/\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_____/\\\\\\_________
{spc} _\\/\\\\\\_________________/\\\\\\///\\\\\\______/\\\\\\/////////\\\\\\_\\/\\\\\\///////////____/\\\\\\\\\\\\\\_______
{spc}  _\\/\\\\\\_______________/\\\\\\/__\\///\\\\\\___\\//\\\\\\______\\///__\\/\\\\\\______________/\\\\\\\\\\\\\\\\\\______
{spc}   _\\/\\\\\\______________/\\\\\\______\\//\\\\\\___\\////\\\\\\_________\\/\\\\\\\\\\\\\\\\\\\\\\_____\\//\\\\\\\\\\\\\\_______
{spc}    _\\/\\\\\\_____________\\/\\\\\\_______\\/\\\\\\______\\////\\\\\\______\\/\\\\\\///////_______\\//\\\\\\\\\\________
{spc}     _\\/\\\\\\_____________\\//\\\\\\______/\\\\\\__________\\////\\\\\\___\\/\\\\\\_______________\\//\\\\\\_________
{spc}      _\\/\\\\\\______________\\///\\\\\\__/\\\\\\_____/\\\\\\______\\//\\\\\\__\\/\\\\\\________________\\///__________
{spc}       _\\/\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\____\\///\\\\\\\\\\/_____\\///\\\\\\\\\\\\\\\\\\\\\\/___\\/\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_____/\\\\\\_________
{spc}        _\\///////////////_______\\/////_________\\///////////_____\\///////////////_____\\///__________{deck}
'''.format(spc=' '*center_space, deck=deck_out_display)
    print(lose)

if __name__ == '__main__' :
    QoL.clear()
    term_cols = os.get_terminal_size().columns
    overkill = 3
    print_win(overkill)
    print('-'*term_cols)
    print_lose()
    print('-'*term_cols)
    score = {'player': 6, 'opponent': 2}
    print_scales(score)