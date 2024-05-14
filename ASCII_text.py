import QoL
import os

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
{spc}        ______\\///____\\///_______\\///////////__\\///_____\\/////_____\\///_____
'''.format(spc=' '*31)
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
{spc}        _\\///////////////_______\\/////_________\\///////////_____\\///////////////_____\\///__________
'''.format(spc=' '*31)


(term_cols, term_rows) = os.get_terminal_size()
card_gaps = (term_cols*55 // 100) // 5 - 15
if card_gaps <= 0 :
    score_gap = 28
else :
    score_gap = card_gaps*9 + 28
def print_scales(player_weight, opponent_weight) :
    scales = '''{spc} PLAYER      LESHY
{spc}{plr} {lsh}
{spc}‾‾‾‾‾‾‾‾/‾\\‾‾‾‾‾‾‾‾
{spc}       /___\\'''.format(plr=player_weight, lsh=opponent_weight, spc=' '*score_gap)
    print(scales)

if __name__ == '__main__' :
    QoL.clear()
    print(win)
    print('-'*120)
    print(lose)
    print('-'*120)
    player_weight = '▄▄▄__' 
    opponent_weight = '_____'
    print_scales(player_weight, opponent_weight)