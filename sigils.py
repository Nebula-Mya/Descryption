Dict = { # check for applicable sigils when any may apply using the group lists at the bottom, then use the code contained in the sigil's list to apply the effect ( exec(sigils.Dict[sigil][2]) ) {see attack method in card.py for example}
    '' : [ # sigil name
        ["     ","     ","     "], # sigil icon
        '', # sigil description
        '''''' # sigil code
        ],

    'bifurcate' : [
        ["_   _"," \ / ","  |  "],
        'Attacks diagonally, dealing damage to two targets.',
        '''
if (front_left_card.zone % 5) != 1 :
    points += front_left_card.takeDamage(self.current_attack, in_opp_field=to_opp_field, bushes=bushes)
if (front_right_card.zone % 5) != 1 :
    points += front_right_card.takeDamage(self.current_attack, in_opp_field=to_opp_field, bushes=bushes)
'''
        ],

    'lane shift right' : [
        [",-,  ","| |->","'-'  "], 
        'Moves right after attacking if possible.',
        '''
'''
        ],

    'lane shift left' : [
        ["  ,-,","<-| |","  '-'"],
        'Moves left after attacking if possible.',
        '''
'''
        ],

    'split' : [
        ["  |  ","()|()","  |  "],
        'Splits into two cards when killed.',
        '''
'''
        ],

    'unkillable' : [
        [",->-,","| X |","'-<-'"],
        'Returns to hand on death.',
        '''
'''
        ],

    'venom' : [
        [" ___ "," \\ / "," ·V· "],
        'Poisons target on attack.',
        '''
points += front_card.takeDamage(self.current_attack, in_opp_field=to_opp_field, bushes=bushes)
front_card.is_poisoned = True
''' # keep an eye that poison is applied
        ],

    'airborne' : [
        ["  _  ","ɩΞΞɭ "," ɩΞΞð"],
        'Attacks from the air, ignoring other creatures.',
        '''
points += front_card.takeDamage(self.current_attack, from_air=True, in_opp_field=to_opp_field, bushes=bushes)
'''
        ],

    'mighty leap' : [
        ["_____","ʅ   ʃ"," ʅɩð "],
        'Can block airborne creatures.',
        '''
'''
        ],

    'worthy sacrifice' : [
        ["(C)  "," (C) ","  (C)"],
        'Worth three sacrifices.',
        '''
'''
        ],

    'bees within' : [
        [" /‾\\ ","|___|","  Ʈ->"],
        'Adds a bee to your hand when damaged.',
        '''
'''
        ],

    'hefty (right)' : [ 
        [". >>>","|)_[]","'———'"],
        'Moves to the right, pushing other creatures with it.',
        '''
'''
        ],
    
    'hefty (left)' : [
        ["<<< .","[]_(|","'———'"],
        'Moves to the left, pushing other creatures with it.',
        '''
'''
        ],

    'many lives' : [ 
        ["  Ω  "," CXƆ ","  V  "],
        "Doesn't die when sacrificed.",
        '''
'''
        ],

    'waterborne' : [
        ["<⁻v⁻>","ˎ\\ /ˏ","λ/λ\\λ"],
        'Attacks directed toward this card hit the owner directly.',
        '''
'''
        ],

    'vole hole' : [
        [" ___ ","/…¨…\\","‾‾‾‾‾"],
        'Adds a vole to your hand when played.',
        '''
'''
        ],

    'touch of death' : [
        ["\\´‾`/","|°Δ°|","/\'\"\'\\"],
        'Always kills the card it attacks, regardless of health.',
        '''
points += front_card.takeDamage(self.current_attack, deathtouch=True, in_opp_field=to_opp_field, bushes=bushes)
'''
        ],

    'dam builder' : [
        ["~~/\\ ","~/\\_\\","/__\\ "],
        'Builds dams on either side when played.',
        '''
'''
        ],

    'corpse eater' : [
        ["ᴦ==ͽ ","L(Ō) "," \'\"\' "],
        'Plays itself to a zone a card died in.',
        '''
'''
        ],
}

on_attacks = ['bifurcate','venom','touch of death', 'airborne']
on_deaths = ['split','unkillable','bees within']
on_plays = ['vole hole','dam builder']
on_damages = ['mighty leap', 'bees within', 'waterborne']
on_sacrifices = ['worthy sacrifice','many lives']
movers = ['lane shift right','lane shift left','hefty (right)','hefty (left)']
misc = ['corpse eater']

if __name__ == '__main__':
    import card
    import QoL
    import os
    QoL.clear()
    term_cols = os.get_terminal_size().columns
    card_gaps = (term_cols*55 // 100) // 5 - 15
    tab = ' '*(card_gaps // 2)
    for key in Dict:
        if key == '':
            continue
        print(tab + QoL.title_case(key) + ':')
        example = card.BlankCard(sigil=key)
        example.species = 'EXAMPLE CARD'
        example.explain()
        print()