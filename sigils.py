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

if self.active == 'player' :
    if self.player_field[zone].zone != 5 and self.player_field[zone+1].species == '' :
        self.player_field[zone+1] = self.player_field[zone]
        self.player_field[zone+1].zone = zone+1
        self.player_field[zone] = card.BlankCard()
        did_shift = True
if self.active == 'opponent' :
    if self.opponent_field[zone].zone != 5 and self.opponent_field[zone+1].species == '' :
        self.opponent_field[zone+1] = self.opponent_field[zone]
        self.opponent_field[zone+1].zone = zone+1
        self.opponent_field[zone] = card.BlankCard()
        did_shift = True
'''
        ],

    'lane shift left' : [
        ["  ,-,","<-| |","  '-'"],
        'Moves left after attacking if possible.',
        '''
import card

if self.active == 'player' :
    if self.player_field[zone].zone != 1 and self.player_field[zone-1].species == '' :
        self.player_field[zone-1] = self.player_field[zone]
        self.player_field[zone-1].zone = zone-1
        self.player_field[zone] = card.BlankCard()
        did_shift = True
if self.active == 'opponent' :
    if self.opponent_field[zone].zone != 1 and self.opponent_field[zone-1].species == '' :
        self.opponent_field[zone-1] = self.opponent_field[zone]
        self.opponent_field[zone-1].zone = zone-1
        self.opponent_field[zone] = card.BlankCard()
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

if self.active == 'player' :
    if zone == 5 :
        self.player_field[zone].sigil = 'hefty (left)'
        self.player_field[zone].updateASCII()
    else :
        push_count = QoL.hefty_check(self.player_field, zone + 1, 'right')
        if push_count == 0 :
            self.player_field[zone].sigil = 'hefty (left)'
            self.player_field[zone].updateASCII()
        elif push_count == -1 :
            self.player_field[zone+1] = self.player_field[zone]
            self.player_field[zone+1].zone = zone+1
            self.player_field[zone] = card.BlankCard()
            did_shift = True
        elif push_count >= 1 :
            did_shift = True
            for n in range(zone + push_count, zone - 1, -1) :
                self.player_field[n+1] = self.player_field[n]
                self.player_field[n+1].zone = n+1
                self.player_field[n] = card.BlankCard()
elif self.active == 'opponent' :
    if zone == 5 :
        self.opponent_field[zone].sigil = 'hefty (left)'
        self.opponent_field[zone].updateASCII()
    else :
        push_count = QoL.hefty_check(self.opponent_field, zone + 1, 'right')
        if push_count == 0 :
            self.opponent_field[zone].sigil = 'hefty (left)'
            self.opponent_field[zone].updateASCII()
        elif push_count == -1 :
            self.opponent_field[zone+1] = self.opponent_field[zone]
            self.opponent_field[zone+1].zone = zone+1
            self.opponent_field[zone] = card.BlankCard()
            did_shift = True
        elif push_count >= 1 :
            did_shift = True
            for n in range(zone + push_count, zone - 1, -1) :
                self.opponent_field[n+1] = self.opponent_field[n]
                self.opponent_field[n+1].zone = n+1
                self.opponent_field[n] = card.BlankCard()
'''
        ],
    
    'hefty (left)' : [
        ["<<< .","[]_(|","'———'"],
        'Moves to the left, pushing other creatures with it.',
        '''
import QoL
import card

if self.active == 'player' :
    if zone == 1 :
        self.player_field[zone].sigil = 'hefty (right)'
        self.player_field[zone].updateASCII()
    else :
        push_count = QoL.hefty_check(self.player_field, zone - 1, 'left')
        if push_count == 0:
            self.player_field[zone].sigil = 'hefty (right)'
            self.player_field[zone].updateASCII()
        elif push_count == -1 :
                self.player_field[zone-1] = self.player_field[zone]
                self.player_field[zone-1].zone = zone-1
                self.player_field[zone] = card.BlankCard()
                did_shift = True
        elif push_count >= 1 :
            did_shift = True
            for n in range(zone - push_count, zone + 1) :
                self.player_field[n-1] = self.player_field[n]
                self.player_field[n-1].zone = n-1
                self.player_field[n] = card.BlankCard()
elif self.active == 'opponent' :
    if zone == 1 :
        self.opponent_field[zone].sigil = 'hefty (right)'
        self.opponent_field[zone].updateASCII()
    else :
        push_count = QoL.hefty_check(self.opponent_field, zone - 1, 'left')
        if push_count == 0:
            self.opponent_field[zone].sigil = 'hefty (right)'
            self.opponent_field[zone].updateASCII()
        elif push_count == -1 :
                self.opponent_field[zone-1] = self.opponent_field[zone]
                self.opponent_field[zone-1].zone = zone-1
                self.opponent_field[zone] = card.BlankCard()
                did_shift = True
        elif push_count >= 1 :
            did_shift = True
            for n in range(zone - push_count, zone + 1) :
                self.opponent_field[n-1] = self.opponent_field[n]
                self.opponent_field[n-1].zone = n-1
                self.opponent_field[n] = card.BlankCard()
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