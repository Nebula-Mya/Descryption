Dict = {    
    '' : [ # sigil name
        ["     ","     ","     "], # sigil icon
        '', # sigil description
        '''''' # sigil code
        ],
        
    '???' : [
        ["?????","?????","?????"],
        '???',
        '''
pass
'''
    ],

    'bifurcate' : [
        ["_   _"," \ / ","  |  "],
        'Attacks diagonally, dealing damage to two targets.',
        '''
for target_card in [front_left_card, front_right_card] :
    if (target_card.zone % 6) != 0 :
        points += target_card.take_damage(self.current_attack, hand, in_opp_field=is_players, bushes=bushes)
'''
        ],

    'lane shift right' : [
        [",-,  ","| |->","'-'  "], 
        'Moves to the right.',
        '''
import card
import QoL

if attacking_field[zone].sigils[0] == 'lane shift right' :
    changed_direction = ['lane shift left', attacking_field[zone].sigils[1]]
else :
    changed_direction = [attacking_field[zone].sigils[0], 'lane shift left']

if zone == 5 or QoL.hefty_check(attacking_field, zone + 1, 'right') == 0 :
    attacking_field[zone].sigils = changed_direction
    attacking_field[zone].update_ASCII()
elif attacking_field[zone+1].species == '' :
    attacking_field[zone+1] = attacking_field[zone]
    attacking_field[zone+1].zone = zone+1
    attacking_field[zone] = card.BlankCard()
    attacking_field[zone].play(zone)
    did_shift = True
'''
        ],

    'lane shift left' : [
        ["  ,-,","<-| |","  '-'"],
        'Moves to the left.',
        '''
import card
import QoL

if attacking_field[zone].sigils[0] == 'lane shift left' :
    changed_direction = ['lane shift right', attacking_field[zone].sigils[1]]
else :
    changed_direction = [attacking_field[zone].sigils[0], 'lane shift right']

if zone == 1 or QoL.hefty_check(attacking_field, zone - 1, 'left') == 0 :
    attacking_field[zone].sigils = changed_direction
    attacking_field[zone].update_ASCII()
elif attacking_field[zone-1].species == '' :
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
import sigils

if applicables == sigils.on_deaths and current_field[zone].status == 'dead' :
    import card
    import copy

    split_card = copy.deepcopy(current_field[zone])

    # play a copy to the left and right if possible
    if split_card.base_life > 1 :
        if zone == 1 :
            poss_zones = [2]
        elif zone == 5 :
            poss_zones = [4]
        else :
            poss_zones = [zone-1, zone+1]
        for shifted_zone in poss_zones :
            if current_field[shifted_zone].species == '' :
                current_field[shifted_zone] = card.BlankCard(species=split_card.species, cost=split_card.saccs, attack=split_card.base_attack//2, life=split_card.base_life//2, sigil=split_card.sigils, zone=shifted_zone, blank_cost=True)
    
    # remove the original card
    current_field[zone].die()
    self.graveyard.insert(0, current_field[zone])
    current_field[zone] = card.BlankCard()
    current_field[zone].play(zone)
    corpses.append((zone, current_field))
'''
        ],

    'unkillable' : [
        [",->-,","| X |","'-<-'"],
        'Returns to hand on death.',
        '''
import sigils
if applicables == sigils.on_deaths :
    import card

    if current_field[zone].status == 'dead' and current_field == self.player_field :
        current_field[zone].die()
        current_field[zone].status = 'alive'
        self.hand.append(current_field[zone])
        current_field[zone] = card.BlankCard()
        current_field[zone].play(zone)
    elif current_field[zone].status == 'dead' :
        current_field[zone].die()
        current_field[zone] = card.BlankCard()
        current_field[zone].play(zone)
        corpses.append((zone, current_field))

elif applicables == sigils.on_sacrifices :
    self.hand.append(self.player_field[ind])
    self.player_field[ind] = card.BlankCard()
'''
        ],

    'venom' : [
        [" ___ "," \\ / "," ·V· "],
        'Poisons target on attack.',
        ''' 
points += front_card.take_damage(self.current_attack, hand, in_opp_field=is_players, bushes=bushes)
front_card.is_poisoned = True
'''
        ],

    'airborne' : [
        ["  _  ","ɩΞΞɭ "," ɩΞΞð"],
        'Attacks from the air, ignoring other creatures.',
        '''
points += front_card.take_damage(self.current_attack, hand, from_air=True, in_opp_field=is_players, bushes=bushes)
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
    self.update_ASCII()
    if self.current_life <= 0 or deathtouch :
        self.status = 'dead'
        if in_opp_field and self.current_life <= 0 :
            excess_damage = damage - prev_life
            bushes[self.zone].take_damage(excess_damage, hand, from_air, in_bushes=True)
'''
        ],

    'worthy sacrifice' : [
        ["(C)  "," (C) ","  (C)"],
        'Worth three sacrifices.',
        '''
pass
'''
        ],

    'bees within' : [
        [" /‾\\ ","|___|","  Ʈ->"],
        'Adds a bee to your hand when damaged.',
        '''
import card_library

# other_sigil = ['airborne'] + [sigil for sigil in self.sigils if sigil not in ['bees within','airborne', '']
# if other_sigil == ['airborne'] :
#     other_sigil = ['airborne', '']

other_sigil = ['airborne'] + [sigil for sigil in self.sigils if sigil != 'bees within']
if other_sigil == ['airborne', 'airborne'] :
    other_sigil = ['airborne','']

if self.species == '' or self.status == 'dead' or from_air:
    teeth = damage
else :
    prev_life = self.current_life
    self.current_life -= damage
    self.update_ASCII()
    if not (in_opp_field or in_bushes) : # only if opponent is attacking, as leshy's bees within wont do anything; he doesnt have a hand to add to
        hand.append(card_library.Bee(sigil=other_sigil))
    if self.current_life <= 0 or deathtouch :
        self.status = 'dead'
        if in_opp_field and self.current_life <= 0 :
            excess_damage = damage - prev_life
            bushes[self.zone].take_damage(excess_damage, hand, from_air, in_bushes=True)
'''
        ],

    'hefty (right)' : [ 
        [". >>>","|)_[]","'———'"],
        'Moves to the right, pushing other creatures with it.',
        '''
import QoL
import card

if attacking_field[zone].sigils[0] == 'hefty (right)' :
    changed_direction = ['hefty (left)', attacking_field[zone].sigils[1]]
else :
    changed_direction = [attacking_field[zone].sigils[0], 'hefty (left)']

if zone == 5 :
    attacking_field[zone].sigils = changed_direction
    attacking_field[zone].update_ASCII()
else :
    push_count = QoL.hefty_check(attacking_field, zone + 1, 'right')
    if push_count == 0 :
        attacking_field[zone].sigils = changed_direction
        attacking_field[zone].update_ASCII()
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

if attacking_field[zone].sigils[0] == 'hefty (left)' :
    changed_direction = ['hefty (right)', attacking_field[zone].sigils[1]]
else :
    changed_direction = [attacking_field[zone].sigils[0], 'hefty (right)']

if zone == 1 :
    attacking_field[zone].sigils = changed_direction
    attacking_field[zone].update_ASCII()
else :
    push_count = QoL.hefty_check(attacking_field, zone - 1, 'left')
    if push_count == 0:
        attacking_field[zone].sigils = changed_direction
        attacking_field[zone].update_ASCII()
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
pass
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
import card_library

other_sigil = [sigil for sigil in self.sigils if sigil != 'vole hole'] + ['']

self.hand.append(card_library.Vole(sigil=other_sigil))
'''
        ],

    'touch of death' : [
        ["\\´‾`/","|°Δ°|","/\'\"\'\\"],
        'Always kills the card it attacks, regardless of health.',
        '''
points += front_card.take_damage(self.current_attack, hand, deathtouch=True, in_opp_field=is_players, bushes=bushes)
'''
        ],

    'dam builder' : [
        ["~~/\\ ","~/\\_\\","/__\\ "],
        'Builds dams on either side when played.',
        '''
import card_library

if zone == 1 :
    poss_zones = [2]
elif zone == 5 :
    poss_zones = [4]
else :
    poss_zones = [zone-1, zone+1]
for shifted_zone in poss_zones :
    if self.player_field[shifted_zone].species == '' :
        self.player_field[shifted_zone] = card_library.Dam()
        self.player_field[shifted_zone].play(zone=shifted_zone)
'''
        ],

    'corpse eater' : [
        ["ᴦ==ͽ ","L(Ō) "," \'\"\' "],
        'Plays itself to a zone a card died in.',
        '''
'''
        ],
}

Combos = {
    ('bifurcate', 'venom') : '''
for target_card in [front_left_card, front_right_card] :
    if (target_card.zone % 5) != 1 :
        points += target_card.takeDamage(self.current_attack, hand, in_opp_field=is_players, bushes=bushes)
        target_card.is_poisoned = True
''',
    ('bifurcate', 'touch of death') : '''
for target_card in [front_left_card, front_right_card] :
    if (target_card.zone % 6) != 0 :
        points += front_card.take_damage(self.current_attack, hand, deathtouch=True, in_opp_field=is_players, bushes=bushes)
''',
    ('airborne', 'bifurcate') : '''
for target_card in [front_left_card, front_right_card] :
    if (target_card.zone % 6) != 0 :
        points += target_card.take_damage(self.current_attack, hand, from_air=True, in_opp_field=is_players, bushes=bushes)
''',
    ('touch of death', 'venom') : '''
points += front_card.take_damage(self.current_attack, hand, deathtouch=True, in_opp_field=is_players, bushes=bushes)
front_card.is_poisoned = True
''',
    ('airborne', 'venom') : '''
points += front_card.take_damage(self.current_attack, hand, from_air=True, in_opp_field=is_players, bushes=bushes)
front_card.is_poisoned = True
''',
    ('airborne', 'touch of death') : '''
points += front_card.take_damage(self.current_attack, hand, deathtouch=True, from_air=True, in_opp_field=is_players, bushes=bushes)
''', 
    ('split', 'unkillable') : ''' # this is only called when applicable is on_deaths
import card
import copy

if current_field[zone].status == 'dead' and current_field == self.player_field :
    split_card = copy.deepcopy(current_field[zone])

    # play a copy to the left and right if possible
    if split_card.base_life > 1 :
        if zone == 1 :
            poss_zones = [2]
        elif zone == 5 :
            poss_zones = [4]
        else :
            poss_zones = [zone-1, zone+1]
        for shifted_zone in poss_zones :
            if current_field[shifted_zone].species == '' :
                current_field[shifted_zone] = card.BlankCard(species=split_card.species, cost=split_card.saccs, attack=split_card.base_attack//2, life=split_card.base_life//2, sigil=split_card.sigils, zone=shifted_zone, blank_cost=True)

    # remove the original card to hand
    current_field[zone].die()
    current_field[zone].status = 'alive'
    self.hand.append(current_field[zone])
    current_field[zone] = card.BlankCard()
    current_field[zone].play(zone)

elif current_field[zone].status == 'dead' :
    split_card = copy.deepcopy(current_field[zone])

    # play a copy to the left and right if possible
    if split_card.base_life > 1 :
        if zone == 1 :
            poss_zones = [2]
        elif zone == 5 :
            poss_zones = [4]
        else :
            poss_zones = [zone-1, zone+1]
        for shifted_zone in poss_zones :
            if current_field[shifted_zone].species == '' :
                current_field[shifted_zone] = card.BlankCard(species=split_card.species, cost=split_card.saccs, attack=split_card.base_attack//2, life=split_card.base_life//2, sigil=split_card.sigils, zone=shifted_zone, blank_cost=True)
                
    # remove the original card
    current_field[zone].die()
    self.graveyard.insert(0, current_field[zone])
    current_field[zone] = card.BlankCard()
    current_field[zone].play(zone)
    corpses.append((zone, current_field))
''',
    ('dam builder', 'vole hole') : '''
import card_library

self.hand.append(card_library.Vole(sigils=['dam builder', '']))

if zone == 1 :
    poss_zones = [2]
elif zone == 5 :
    poss_zones = [4]
else :
    poss_zones = [zone-1, zone+1]
for shifted_zone in poss_zones :
    if self.player_field[shifted_zone].species == '' :
        self.player_field[shifted_zone] = card_library.Dam()
        self.player_field[shifted_zone].play(zone=shifted_zone)
''',
    ('many lives', 'unkillable') : ''' # this is only called when applicable is on_sacrifices
import card

self.hand.append(self.player_field[ind])
self.hand[-1].saccs = 0
self.hand[-1].update_ASCII()
self.player_field[ind] = card.BlankCard()
''',
    ('mighty leap', 'waterborne') : '''
if from_air :
    prev_life = self.current_life
    self.current_life -= damage
    self.update_ASCII()
    if self.current_life <= 0 or deathtouch :
        self.status = 'dead'
        if in_opp_field and self.current_life <= 0 :
            excess_damage = damage - prev_life
            bushes[self.zone].take_damage(excess_damage, hand, from_air, in_bushes=True)
else :
    teeth = damage
''',
    ('bees within', 'mighty leap') : '''
import card_library

if self.species == '' or self.status == 'dead' :
    teeth = damage
else :
    prev_life = self.current_life
    self.current_life -= damage
    self.update_ASCII()
    if not (in_opp_field or in_bushes) : # only if opponent is attacking, as leshy's bees within wont do anything; he doesnt have a hand to add to
        hand.append(card_library.Bee(sigils=['airborne', 'mighty leap']))
    if self.current_life <= 0 or deathtouch :
        self.status = 'dead'
        if in_opp_field and self.current_life <= 0 :
            excess_damage = damage - prev_life
            bushes[self.zone].take_damage(excess_damage, hand, from_air, in_bushes=True)
''',
    ('bees within', 'touch of death') : '''
teeth = damage
''',
    ('lane shift left', 'lane shift right') : '''
pass
''',
    ('hefty (right)', 'lane shift right') : '''
import QoL
import card

if self.sigils[0] == 'hefty (right)' :
    changed_direction = ['hefty (left)', self.sigils[1]]
else :
    changed_direction = [self.sigils[0], 'hefty (left)']

if zone == 5 :
    attacking_field[zone].sigils = changed_direction
    attacking_field[zone].update_ASCII()
else :
    push_count = QoL.hefty_check(attacking_field, zone + 1, 'right')
    if push_count == 0 :
        attacking_field[zone].sigils = changed_direction
        attacking_field[zone].update_ASCII()
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
''',
    ('hefty (right)', 'lane shift left') : '''
pass
''',
    ('hefty (left)', 'lane shift left') : '''
import QoL
import card

if self.sigils[0] == 'hefty (left)' :
    changed_direction = ['hefty (right)', self.sigils[1]]
else :
    changed_direction = [self.sigils[0], 'hefty (right)']

if zone == 1 :
    attacking_field[zone].sigils = changed_direction
    attacking_field[zone].update_ASCII()
else :
    push_count = QoL.hefty_check(attacking_field, zone - 1, 'left')
    if push_count == 0:
        attacking_field[zone].sigils = changed_direction
        attacking_field[zone].update_ASCII()
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
''',
    ('hefty (left)', 'lane shift right') : '''
pass
''',
}

on_attacks = ['bifurcate','venom','touch of death', 'airborne']
on_deaths = ['split','unkillable']
on_plays = ['vole hole','dam builder']
on_damages = ['mighty leap', 'waterborne', 'bees within']
on_sacrifices = ['many lives', 'unkillable']
movers = ['lane shift right','lane shift left','hefty (right)','hefty (left)']
misc = ['corpse eater', 'worthy sacrifice'] # these need to be hardcoded

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
        example = card.BlankCard(sigils=[key, ''])
        example.species = 'EXAMPLE CARD'
        example.explain()
        print()