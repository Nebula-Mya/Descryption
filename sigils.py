from __future__ import annotations # prevent type hints needing import at runtime

Dict = {    
    '' : [ # sigil name
        ["     ","     ","     "], # sigil icon
        '', # sigil description
        '''#py
''' # sigil code
    ],
        
    '???' : [
        ["?????","?????","?????"],
        '???',
        '''#py
pass
'''
    ],

    'bifurcate' : [
        ["_   _"," \\ / ","  |  "],
        'Attacks diagonally, dealing damage to two targets.',
        '''#py
for target_card in [front_left_card, front_right_card] :
    if (target_card.zone % 5) != 0 :
        points += target_card.take_damage(self.current_attack, hand, in_opp_field=is_players, bushes=bushes)
'''
    ],

    'lane shift right' : [
        [",-,  ","| |->","'-'  "], 
        'Moves to the right.',
        '''#py
import card
import QoL

if attacking_field[zone].sigils[0] == 'lane shift right' :
    changed_direction = ('lane shift left', attacking_field[zone].sigils[1])
else :
    changed_direction = (attacking_field[zone].sigils[0], 'lane shift left')

if zone == 4 or QoL.hefty_check(attacking_field, zone + 1, 'right') == 0 :
    attacking_field[zone].sigils = changed_direction
    attacking_field[zone].update_ASCII()
elif type(attacking_field[zone+1]) == card.BlankCard :
    attacking_field[zone+1] = attacking_field[zone]
    attacking_field[zone+1].zone = zone+1
    self.summon_card(card.BlankCard(), attacking_field, zone)
    did_shift = True
'''
    ],

    'lane shift left' : [
        ["  ,-,","<-| |","  '-'"],
        'Moves to the left.',
        '''#py
import card
import QoL

if attacking_field[zone].sigils[0] == 'lane shift left' :
    changed_direction = ('lane shift right', attacking_field[zone].sigils[1])
else :
    changed_direction = (attacking_field[zone].sigils[0], 'lane shift right')

if zone == 1 or QoL.hefty_check(attacking_field, zone - 1, 'left') == 0 :
    attacking_field[zone].sigils = changed_direction
    attacking_field[zone].update_ASCII()
elif type(attacking_field[zone-1]) == card.BlankCard :
    attacking_field[zone-1] = attacking_field[zone]
    attacking_field[zone-1].zone = zone-1
    self.summon_card(card.BlankCard(), attacking_field, zone)
    did_shift = True
'''
    ],

    'split' : [
        ["  |  ","()|()","  |  "],
        'Splits into two cards when killed.',
        '''#py
import sigils

if applicables == sigils.on_deaths and current_field[zone].status == 'dead' :
    import card
    import card_library

    if current_field[zone].base_life > 1 :if current_field == self.player_field :
            blank_cost = False
        else :
            blank_cost = True
        # make copies of the card with halved stats
        left_copy = card_library.type(current_field[zone])(sigils=current_field[zone].sigils, blank_cost=blank_cost)
        left_copy.base_life = current_field[zone].base_life // 2
        left_copy.base_attack = current_field[zone].base_attack // 2
        left_copy.saccs = current_field[zone].saccs // 2
        left_copy.reset_stats()
        left_copy.update_ASCII()

        right_copy = card_library.type(current_field[zone])(sigils=current_field[zone].sigils, blank_cost=blank_cost)
        right_copy.base_life = current_field[zone].base_life // 2
        right_copy.base_attack = current_field[zone].base_attack // 2
        right_copy.saccs = current_field[zone].saccs // 2
        right_copy.reset_stats()
        right_copy.update_ASCII()

        # play the copies to the left and right if possible
        if zone != 1 and type(current_field[zone-1]) == card.BlankCard :
            self.summon_card(left_copy, current_field, zone-1)
        if zone != 4 and type(current_field[zone+1]) == card.BlankCard :
            self.summon_card(right_copy, current_field, zone+1)

    # remove the original card
    current_field[zone].die()
    if type(current_field[zone]) != card.BlankCard and current_field == self.player_field : self.graveyard.insert(0, current_field[zone])
    self.summon_card(card.BlankCard(), current_field, zone)
    corpses.append((zone, current_field))
'''
    ],

    'unkillable' : [
        [",->-,","| X |","'-<-'"],
        'Returns to hand on death.',
        '''#py
import sigils
import card
if applicables == sigils.on_deaths :

    if current_field[zone].status == 'dead' and current_field == self.player_field :
        current_field[zone].die()
        current_field[zone].status = 'alive'
        self.hand.append(current_field[zone])
        self.summon_card(card.BlankCard(), current_field, zone)
    elif current_field[zone].status == 'dead' :
        current_field[zone].die()
        self.summon_card(card.BlankCard(), current_field, zone)
        corpses.append((zone, current_field))

elif applicables == sigils.on_sacrifices :
    import card_library

    if type(self.player_field[ind]) == card_library.Ouroboros : self.player_field[ind].level_up()
    self.hand.append(self.player_field[ind])
    self.summon_card(card.BlankCard(), self.player_field, ind)
'''
    ],

    'venom' : [
        [" ___ "," \\ / "," ·V· "],
        'Poisons target on attack.',
        '''#py
points += front_card.take_damage(self.current_attack, hand, in_opp_field=is_players, bushes=bushes)
front_card.is_poisoned = True
'''
    ],

    'airborne' : [
        ["  _  ","ɩΞΞɭ "," ɩΞΞð"],
        'Attacks from the air, ignoring other creatures.',
        '''#py
points += front_card.take_damage(self.current_attack, hand, from_air=True, in_opp_field=is_players, bushes=bushes)
'''
    ],

    'mighty leap' : [
        ["_____","ʅ   ʃ","ɩð_ʃ "],
        'Can block airborne creatures.',
        '''#py
import card
if type(self) == card.BlankCard or self.status == 'dead' :
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
        '''#py
pass
'''
    ],

    'bees within' : [
        [" /‾\\ ","|___|","  Ʈ->"],
        'Adds a bee to your hand when damaged.',
        '''#py
import card_library
import card

other_sigils = ('airborne', [sigil for sigil in self.sigils if sigil != 'bees within'][0])
if other_sigils == ('airborne', 'airborne') :
    other_sigils = ('airborne','')

if type(self) == card.BlankCard or self.status == 'dead' or from_air:
    teeth = damage
else :
    prev_life = self.current_life
    self.current_life -= damage
    self.update_ASCII()
    if (not (in_opp_field or in_bushes)) and damage > 0 : # only if opponent is attacking, as leshy's bees within wont do anything; he doesnt have a hand to add to
        hand.append(card_library.Bee(sigils=other_sigils))
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
        '''#py
import QoL
import card

if attacking_field[zone].sigils[0] == 'hefty (right)' :
    changed_direction = ('hefty (left)', attacking_field[zone].sigils[1])
else :
    changed_direction = (attacking_field[zone].sigils[0], 'hefty (left)')

if zone == 4 :
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
        self.summon_card(card.BlankCard(), attacking_field, zone)
        did_shift = True
    elif push_count >= 1 :
        for n in range(zone + push_count, zone - 1, -1) :
            attacking_field[n+1] = attacking_field[n]
            attacking_field[n+1].zone = n+1
            self.summon_card(card.BlankCard(), attacking_field, n)
        did_shift = True
'''
    ],
    
    'hefty (left)' : [
        ["<<< .","[]_(|","'———'"],
        'Moves to the left, pushing other creatures with it.',
        '''#py
import QoL
import card

if attacking_field[zone].sigils[0] == 'hefty (left)' :
    changed_direction = ('hefty (right)', attacking_field[zone].sigils[1])
else :
    changed_direction = (attacking_field[zone].sigils[0], 'hefty (right)')

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
            self.summon_card(card.BlankCard(), attacking_field, zone)
            did_shift = True
    elif push_count >= 1 :
        for n in range(zone - push_count, zone + 1) :
            attacking_field[n-1] = attacking_field[n]
            attacking_field[n-1].zone = n-1
            self.summon_card(card.BlankCard(), attacking_field, n)
        did_shift = True
'''
    ],

    'many lives' : [ 
        ["  Ω  "," CXƆ ","  V  "],
        "Doesn't die when sacrificed.",
        '''#py
pass
'''
    ],

    'waterborne' : [
        ["<⁻v⁻>","ˎ\\ /ˏ","λ/λ\\λ"],
        'Attacks directed toward this card hit the owner directly.',
        '''#py
teeth = damage
'''
    ],

    'vole hole' : [
        [" ___ ","/…¨…\\","‾‾‾‾‾"],
        'Adds a vole to your hand when played.',
        '''#py
import card_library

other_sigils = ([sigil for sigil in self.player_field[zone].sigils if sigil != 'vole hole'][0], '')

self.hand.append(card_library.Vole(sigils=other_sigils))
'''
    ],

    'touch of death' : [
        ["\\´‾`/","|°Δ°|","/\'\"\'\\"],
        'Always kills the card it attacks, regardless of health.',
        '''#py
points += front_card.take_damage(self.current_attack, hand, deathtouch=True, in_opp_field=is_players, bushes=bushes)
'''
    ],

    'dam builder' : [
        ["~~/\\ ","~/\\_\\","/__\\ "],
        'Builds dams on either side when played.',
        '''#py
import card_library
import card

other_sigils = ([sigil for sigil in self.player_field[zone].sigils if sigil != 'dam builder'][0], '')

if zone == 1 :
    poss_zones = [2]
elif zone == 4 :
    poss_zones = [3]
else :
    poss_zones = [zone-1, zone+1]
for shifted_zone in poss_zones :
    if type(self.player_field[shifted_zone]) == card.BlankCard :
        self.summon_card(card_library.Dam(sigils=other_sigils), self.player_field, shifted_zone)
'''
    ],

    'corpse eater' : [
        ["ᴦ==ͽ ","L(Ō) "," \'\"\' "],
        'Plays itself to a zone a card died in.',
        '''#py
pass
'''
    ],

    'steel trap' : [ # will never be available to players
        [" ʌ^ʌ ","(-Θ-)"," ^ʌ^ "],
        'When this card perishes, the creature opposing it perishes as well. A Pelt is created in the your hand.',
        '''#py
if current_field[zone].status == 'dead' :
    import card_library
    import card

    # remove the original card
    current_field[zone].die()
    if type(current_field[zone]) != card.BlankCard and current_field == self.player_field : self.graveyard.insert(0, current_field[zone])
    self.summon_card(card=card.BlankCard(), field=current_field, zone=zone)
    corpses.append((zone, current_field))

    # kill the opposing card
    if current_field != self.bushes :
        if current_field == self.player_field : opposing_field = self.opponent_field
        elif current_field == self.opponent_field : opposing_field = self.player_field

        if type(opposing_field[zone]) != card.BlankCard :
            opposing_field[zone].die()
            self.summon_card(card.BlankCard(), opposing_field, zone)
            self.hand.append(card_library.WolfPelt())
'''
    ],
}

Combos = {
    ('bifurcate', 'venom') : '''#py
for target_card in [front_left_card, front_right_card] :
    if (target_card.zone % 5) != 0 :
        points += target_card.takeDamage(self.current_attack, hand, in_opp_field=is_players, bushes=bushes)
        target_card.is_poisoned = True
''',
    ('bifurcate', 'touch of death') : '''#py
for target_card in [front_left_card, front_right_card] :
    if (target_card.zone % 5) != 0 :
        points += front_card.take_damage(self.current_attack, hand, deathtouch=True, in_opp_field=is_players, bushes=bushes)
''',
    ('airborne', 'bifurcate') : '''#py
for target_card in [front_left_card, front_right_card] :
    if (target_card.zone % 5) != 0 :
        points += target_card.take_damage(self.current_attack, hand, from_air=True, in_opp_field=is_players, bushes=bushes)
''',
    ('touch of death', 'venom') : '''#py
points += front_card.take_damage(self.current_attack, hand, deathtouch=True, in_opp_field=is_players, bushes=bushes)
front_card.is_poisoned = True
''',
    ('airborne', 'venom') : '''#py
points += front_card.take_damage(self.current_attack, hand, from_air=True, in_opp_field=is_players, bushes=bushes)
front_card.is_poisoned = True
''',
    ('airborne', 'touch of death') : '''#py
points += front_card.take_damage(self.current_attack, hand, deathtouch=True, from_air=True, in_opp_field=is_players, bushes=bushes)
''', 
    ('split', 'unkillable') : '''#py # this is only called when applicable is on_deaths
if current_field[zone].status == 'dead' :
    import card
    import card_library

    if current_field[zone].base_life > 1 :
        if current_field == self.player_field :
            blank_cost = False
        else :
            blank_cost = True
        # make copies of the card with halved stats
        left_copy = card_library.type(current_field[zone])(sigils=current_field[zone].sigils, blank_cost=blank_cost)
        left_copy.base_life = current_field[zone].base_life // 2
        left_copy.base_attack = current_field[zone].base_attack // 2
        left_copy.saccs = current_field[zone].saccs // 2
        left_copy.reset_stats()
        left_copy.update_ASCII()

        right_copy = card_library.type(current_field[zone])(sigils=current_field[zone].sigils, blank_cost=blank_cost)
        right_copy.base_life = current_field[zone].base_life // 2
        right_copy.base_attack = current_field[zone].base_attack // 2
        right_copy.saccs = current_field[zone].saccs // 2
        right_copy.reset_stats()
        right_copy.update_ASCII()

        # play the copies to the left and right if possible
        if zone != 1 and type(current_field[zone-1]) == card.BlankCard :
            self.summon_card(left_copy, current_field, zone-1)
        if zone != 4 and type(current_field[zone+1]) == card.BlankCard :
            self.summon_card(right_copy, current_field, zone+1)


    # move the original card to hand
    if current_field == self.player_field :
        current_field[zone].die()
        current_field[zone].status = 'alive'
        self.hand.append(current_field[zone])
        current_field[zone] = card.BlankCard()
        current_field[zone].play(zone)
    else : # remove the original card
        current_field[zone].die()
        if type(current_field[zone]) != card.BlankCard and current_field == self.player_field : self.graveyard.insert(0, current_field[zone])
        current_field[zone] = card.BlankCard()
        current_field[zone].play(zone)
        corpses.append((zone, current_field))
''',
    ('dam builder', 'vole hole') : '''#py
import card_library
import card

self.hand.append(card_library.Vole(sigils=['dam builder', '']))

if zone == 1 :
    poss_zones = [2]
elif zone == 4 :
    poss_zones = [3]
else :
    poss_zones = [zone-1, zone+1]
for shifted_zone in poss_zones :
    if type(self.player_field[shifted_zone]) == card.BlankCard :
        self.player_field[shifted_zone] = card_library.Dam(sigils=['vole hole', ''])
        self.hand.append(card_library.Vole())
        self.player_field[shifted_zone].play(zone=shifted_zone)
''',
    ('many lives', 'unkillable') : '''#py # this is only called when applicable is on_sacrifices
import card
import card_library

if type(self.player_field[ind]) == card_library.Ouroboros : self.player_field[ind].level_up()

self.hand.append(self.player_field[ind])
self.hand[-1].saccs = 0
self.hand[-1].update_ASCII()
self.player_field[ind] = card.BlankCard()
''',
    ('mighty leap', 'waterborne') : '''#py
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
    ('bees within', 'mighty leap') : '''#py
import card_library
import card

if type(self) == card.BlankCard or self.status == 'dead' :
    teeth = damage
else :
    prev_life = self.current_life
    self.current_life -= damage
    self.update_ASCII()
    if (not (in_opp_field or in_bushes)) and damage > 0 : # only if opponent is attacking, as leshy's bees within wont do anything; he doesnt have a hand to add to
        hand.append(card_library.Bee(sigils=['airborne', 'mighty leap']))
    if self.current_life <= 0 or deathtouch :
        self.status = 'dead'
        if in_opp_field and self.current_life <= 0 :
            excess_damage = damage - prev_life
            bushes[self.zone].take_damage(excess_damage, hand, from_air, in_bushes=True)
''',
    ('lane shift left', 'lane shift right') : '''#py
pass
''',
    ('hefty (right)', 'lane shift right') : '''#py
import QoL
import card

if attacking_field[zone].sigils[0] == 'hefty (right)' :
    changed_direction = ('hefty (left)', attacking_field[zone].sigils[1])
else :
    changed_direction = (attacking_field[zone].sigils[0], 'hefty (left)')

if zone == 4 :
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
    ('hefty (right)', 'lane shift left') : '''#py
pass
''',
    ('hefty (left)', 'lane shift left') : '''#py
import QoL
import card

if attacking_field[zone].sigils[0] == 'hefty (left)' :
    changed_direction = ('hefty (right)', attacking_field[zone].sigils[1])
else :
    changed_direction = (attacking_field[zone].sigils[0], 'hefty (right)')

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
    ('hefty (left)', 'lane shift right') : '''#py
pass
''',
    ('split', 'steel trap') : '''#py
import sigils

if applicables == sigils.on_deaths and current_field[zone].status == 'dead' :
    import card
    import card_library

    if current_field[zone].base_life > 1 :if current_field == self.player_field :
            blank_cost = False
        else :
            blank_cost = True
        # make copies of the card with halved stats
        left_copy = card_library.type(current_field[zone])(sigils=current_field[zone].sigils, blank_cost=blank_cost)
        left_copy.base_life = current_field[zone].base_life // 2
        left_copy.base_attack = current_field[zone].base_attack // 2
        left_copy.saccs = current_field[zone].saccs // 2
        left_copy.reset_stats()
        left_copy.update_ASCII()

        right_copy = card_library.type(current_field[zone])(sigils=current_field[zone].sigils, blank_cost=blank_cost)
        right_copy.base_life = current_field[zone].base_life // 2
        right_copy.base_attack = current_field[zone].base_attack // 2
        right_copy.saccs = current_field[zone].saccs // 2
        right_copy.reset_stats()
        right_copy.update_ASCII()

        # play the copies to the left and right if possible
        if zone != 1 and type(current_field[zone-1]) == card.BlankCard :
            self.summon_card(left_copy, current_field, zone-1)
        if zone != 4 and type(current_field[zone+1]) == card.BlankCard :
            self.summon_card(right_copy, current_field, zone+1)

    # remove the original card
    current_field[zone].die()
    if type(current_field[zone]) != card.BlankCard and current_field == self.player_field : self.graveyard.insert(0, current_field[zone])
    self.summon_card(card.BlankCard(), current_field, zone)
    corpses.append((zone, current_field))

    # kill the opposing card
    if current_field != self.bushes :
        if current_field == self.player_field : opposing_field = self.opponent_field
        elif current_field == self.opponent_field : opposing_field = self.player_field

        if type(opposing_field[zone]) != card.BlankCard :
            opposing_field[zone].die()
            self.summon_card(card.BlankCard(), opposing_field, zone)
            self.hand.append(card_library.WolfPelt())
''',
    ('steel trap', 'unkillable') : '''#py
import sigils
import card_library

if applicables == sigils.on_deaths :
    import card

    # move the original card to hand
    if current_field[zone].status == 'dead' and current_field == self.player_field :
        current_field[zone].die()
        current_field[zone].status = 'alive'
        self.hand.append(current_field[zone])
        self.summon_card(card.BlankCard(), current_field, zone)
    elif current_field[zone].status == 'dead' :
        current_field[zone].die()
        self.summon_card(card.BlankCard(), current_field, zone)
        corpses.append((zone, current_field))

    # kill the opposing card
    if current_field != self.bushes :
        if current_field == self.player_field : opposing_field = self.opponent_field
        elif current_field == self.opponent_field : opposing_field = self.player_field

        if type(opposing_field[zone]) != card.BlankCard :
            opposing_field[zone].die()
            self.summon_card(card.BlankCard(), opposing_field, zone)
            self.hand.append(card_library.WolfPelt())

elif applicables == sigils.on_sacrifices :
    if type(self.player_field[ind]) == card_library.Ouroboros : self.player_field[ind].level_up()
    self.hand.append(self.player_field[ind])
    self.summon_card(card.BlankCard(), self.player_field, ind)
''',
}

on_attacks = ['bifurcate','venom','touch of death', 'airborne']
on_deaths = ['split','unkillable','steel trap']
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
        example = card.BlankCard(sigils=(key, ''))
        example.species = 'EXAMPLE CARD'
        example.explain()
        print()