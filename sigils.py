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
for target_card in [front_left_card, front_right_card] :
    if (target_card.zone % 6) != 0 :
        points += target_card.take_damage(self.current_attack, hand, in_opp_field=is_players, bushes=bushes)
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
import card
import copy

if current_field[zone].status == 'dead' :
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
                current_field[shifted_zone] = card.BlankCard(species=split_card.species, cost=split_card.saccs, attack=split_card.base_attack//2, life=split_card.base_life//2, sigil=split_card.sigil, zone=shifted_zone, blank_cost=True)
    
                
    # remove the original card
    current_field[zone].die()
    self.graveyard.insert(0, current_field[zone])
    current_field[zone] = card.BlankCard()
    current_field[zone].play(zone)
    corpses.append(zone)
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
        corpses.append(zone)

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
    self.update_ASCII()
    if not (in_opp_field or in_bushes) : # only if opponent is attacking, as leshy's bees within wont do anything; he doesnt have a hand to add to
        hand.append(card_library.Bee())
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

if zone == 5 :
    attacking_field[zone].sigil = 'hefty (left)'
    attacking_field[zone].update_ASCII()
else :
    push_count = QoL.hefty_check(attacking_field, zone + 1, 'right')
    if push_count == 0 :
        attacking_field[zone].sigil = 'hefty (left)'
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

if zone == 1 :
    attacking_field[zone].sigil = 'hefty (right)'
    attacking_field[zone].update_ASCII()
else :
    push_count = QoL.hefty_check(attacking_field, zone - 1, 'left')
    if push_count == 0:
        attacking_field[zone].sigil = 'hefty (right)'
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

self.hand.append(card_library.Vole())
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
        example = card.BlankCard(sigil=key)
        example.species = 'EXAMPLE CARD'
        example.explain()
        print()