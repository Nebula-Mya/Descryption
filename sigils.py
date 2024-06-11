Dict = {
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
    points += front_left_card.takeDamage(self.current_attack, hand, in_opp_field=is_players, bushes=bushes)
if (front_right_card.zone % 5) != 1 :
    points += front_right_card.takeDamage(self.current_attack, hand, in_opp_field=is_players, bushes=bushes)
'''
        ],

    'lane shift right' : [
        [",-,  ","| |->","'-'  "], 
        'Moves right after attacking if possible.',
        '''
import card

if zone != 5 and attacking_field[zone+1].species == '' :
    attacking_field[zone+1] = attacking_field[zone]
    attacking_field[zone+1].zone = zone+1
    attacking_field[zone] = card.BlankCard()
    attacking_field[zone].play(zone)
    did_shift = True
'''
        ],

    'lane shift left' : [
        ["  ,-,","<-| |","  '-'"],
        'Moves left after attacking if possible.',
        '''
import card

if zone != 1 and attacking_field[zone-1].species == '' :
    attacking_field[zone-1] = attacking_field[zone]
    attacking_field[zone-1].zone = zone-1
    attacking_field[zone] = card.BlankCard()
    attacking_field[zone].play(zone)
    did_shift = True
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
points += front_card.takeDamage(self.current_attack, hand, in_opp_field=is_players, bushes=bushes)
front_card.is_poisoned = True
'''
        ],

    'airborne' : [
        ["  _  ","ɩΞΞɭ "," ɩΞΞð"],
        'Attacks from the air, ignoring other creatures.',
        '''
points += front_card.takeDamage(self.current_attack, hand, from_air=True, in_opp_field=is_players, bushes=bushes)
'''
        ],

    'mighty leap' : [
        ["_____","ʅ   ʃ"," ʅɩð "],
        'Can block airborne creatures.',
        '''
if self.species == '' or self.status == 'dead' :
    teeth = damage
else :
    prev_life = self.current_life
    self.current_life -= damage
    self.updateASCII()
    if self.current_life <= 0 or deathtouch :
        self.status = 'dead'
        if in_opp_field and self.current_life <= 0 :
            excess_damage = damage - prev_life
            bushes[self.zone].takeDamage(excess_damage, hand, from_air, in_bushes=True)
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
import card_library

if self.species == '' or self.status == 'dead' or from_air:
    teeth = damage
else :
    prev_life = self.current_life
    self.current_life -= damage
    self.updateASCII()
    if not (in_opp_field or in_bushes) : # only if opponent is attacking, as leshy's bees within wont do anything; he doesnt have a hand to add to
        hand.append(card_library.Bee())
    if self.current_life <= 0 or deathtouch :
        self.status = 'dead'
        if in_opp_field and self.current_life <= 0 :
            excess_damage = damage - prev_life
            bushes[self.zone].takeDamage(excess_damage, hand, from_air, in_bushes=True)
'''
        ],

    'hefty (right)' : [ 
        [". >>>","|)_[]","'———'"],
        'Moves to the right, pushing other creatures with it.',
        '''
import QoL
import card

if zone == 5 :
    attacking_field[zone].sigil = 'hefty (left)'
    attacking_field[zone].updateASCII()
else :
    push_count = QoL.hefty_check(attacking_field, zone + 1, 'right')
    if push_count == 0 :
        attacking_field[zone].sigil = 'hefty (left)'
        attacking_field[zone].updateASCII()
    elif push_count == -1 :
        attacking_field[zone+1] = attacking_field[zone]
        attacking_field[zone+1].zone = zone+1
        attacking_field[zone] = card.BlankCard()
        attacking_field[zone].play(zone)
        did_shift = True
    elif push_count >= 1 :
        for n in range(zone + push_count, zone - 1, -1) :
            attacking_field[n+1] = attacking_field[n]
            attacking_field[n+1].zone = n+1
            attacking_field[n] = card.BlankCard()
            attacking_field[n].play(n)
        did_shift = True
'''
        ],
    
    'hefty (left)' : [
        ["<<< .","[]_(|","'———'"],
        'Moves to the left, pushing other creatures with it.',
        '''
import QoL
import card

if zone == 1 :
    attacking_field[zone].sigil = 'hefty (right)'
    attacking_field[zone].updateASCII()
else :
    push_count = QoL.hefty_check(attacking_field, zone - 1, 'left')
    if push_count == 0:
        attacking_field[zone].sigil = 'hefty (right)'
        attacking_field[zone].updateASCII()
    elif push_count == -1 :
            attacking_field[zone-1] = attacking_field[zone]
            attacking_field[zone-1].zone = zone-1
            attacking_field[zone] = card.BlankCard()
            attacking_field[zone].play(zone)
            did_shift = True
    elif push_count >= 1 :
        for n in range(zone - push_count, zone + 1) :
            attacking_field[n-1] = attacking_field[n]
            attacking_field[n-1].zone = n-1
            attacking_field[n] = card.BlankCard()
            attacking_field[n].play(n)
        did_shift = True
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
teeth = damage
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
points += front_card.takeDamage(self.current_attack, hand, deathtouch=True, in_opp_field=is_players, bushes=bushes)
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

on_attacks = ['bifurcate','venom','touch of death', 'airborne'] # IMPLEMENTED
on_deaths = ['split','unkillable']
on_plays = ['vole hole','dam builder']
on_damages = ['mighty leap', 'waterborne', 'bees within'] # IMPLEMENTED
on_sacrifices = ['worthy sacrifice','many lives']
movers = ['lane shift right','lane shift left','hefty (right)','hefty (left)'] # IMPLEMENTED
on_dead_card = ['corpse eater']

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