from __future__ import annotations # prevent type hints needing import at runtime
from typing import TYPE_CHECKING
if TYPE_CHECKING :
    from typing import Any

import card
import QoL
import random
import ASCII_text
import os
import sigils

class Squirrel(card.BlankCard) :
    '''
    A squirrel card, which can be used as a resource to play other cards.
    '''
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('','')) :
        super().__init__(species='Squirrel', cost=0, attack=0, life=1, sigils=sigils, blank_cost=blank_cost)

class Rabbit(card.BlankCard) :
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('lane shift right','')) :
        super().__init__(species='Rabbit', cost=0, attack=1, life=1, sigils=sigils, blank_cost=blank_cost)
    
class OppositeRabbit(card.BlankCard) : # only for Leshy
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('lane shift left','')) :
        super().__init__(species='Rabbit', cost=0, attack=1, life=1, sigils=sigils, blank_cost=blank_cost)

class Shrew(card.BlankCard) :
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('lane shift left','')) :
        super().__init__(species='Shrew', cost=0, attack=1, life=1, sigils=sigils, blank_cost=blank_cost)

class OppositeShrew(card.BlankCard) : # only for Leshy
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('lane shift right','')) :
        super().__init__(species='Shrew', cost=0, attack=1, life=1, sigils=sigils, blank_cost=blank_cost)

class DumpyTF(card.BlankCard) :
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('','')) :
        super().__init__(species='Dumpy Tree Frog', cost=1, attack=2, life=2, sigils=sigils, blank_cost=blank_cost)

class Turtle(card.BlankCard) :
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('','')) :
        super().__init__(species='Turtle', cost=1, attack=0, life=4, sigils=sigils, blank_cost=blank_cost)

class Asp(card.BlankCard) :
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('venom','')) :
        super().__init__(species='Asp', cost=2, attack=2, life=2, sigils=sigils, blank_cost=blank_cost)

class Falcon(card.BlankCard) :
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('airborne','')) :
        super().__init__(species='Falcon', cost=2, attack=3, life=1, sigils=sigils, blank_cost=blank_cost)

class Lobster(card.BlankCard) :
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('bifurcate','')) :
        super().__init__(species='Lobster', cost=3, attack=2, life=3, sigils=sigils, blank_cost=blank_cost)

class BoppitW(card.BlankCard) :
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('split','')) :
        super().__init__(species='Boppit Worm', cost=4, attack=3, life=5, sigils=sigils, blank_cost=blank_cost)

class Ouroboros(card.BlankCard) :
    oro_level = QoL.read_data([['progress markers', 'ouro level']])[0]

    @classmethod
    def set_level(cls) -> None :
        cls.oro_level = QoL.read_data([['progress markers', 'ouro level']])[0]
    
    @classmethod
    def increase_level(cls) -> None :
        cls.oro_level += 1

    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('unkillable','')) :
        Ouroboros.set_level()
        super().__init__(species='Ouroboros', cost=2, attack=Ouroboros.oro_level, life=Ouroboros.oro_level, sigils=sigils, blank_cost=blank_cost)

    def level_up(self) -> None :
        self.base_attack += 1
        self.base_life += 1
        Ouroboros.increase_level()
        self.reset_stats()
        self.update_ASCII()
        QoL.write_data([(['progress markers', 'ouro level'], Ouroboros.oro_level)])

    def die(self) -> None :
        self.level_up()
        super().die()

class Cockroach(card.BlankCard) :
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('unkillable','')) :
        super().__init__(species='Cockroach', cost=2, attack=1, life=1, sigils=sigils, blank_cost=blank_cost)

class Stoat(card.BlankCard) :
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('','')) :
        super().__init__(species='Stoat', cost=1, attack=1, life=3, sigils=sigils, blank_cost=blank_cost)

class Wolf(card.BlankCard) :
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('','')) :
        super().__init__(species='Wolf', cost=2, attack=3, life=2, sigils=sigils, blank_cost=blank_cost)

class Grizzly(card.BlankCard) :
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('','')) :
        super().__init__(species='Grizzly', cost=3, attack=4, life=6, sigils=sigils, blank_cost=blank_cost)

class Urayuli(card.BlankCard) :
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('','')) :
        super().__init__(species='Urayuli', cost=4, attack=7, life=7, sigils=sigils, blank_cost=blank_cost)

class Raven(card.BlankCard) :
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('airborne','')) :
        super().__init__(species='Raven', cost=2, attack=2, life=3, sigils=sigils, blank_cost=blank_cost)

class Bee(card.BlankCard) : # only given by a sigil
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('airborne','')) :
        super().__init__(species='Bee', cost=0, attack=1, life=1, sigils=sigils, blank_cost=blank_cost)

class Bullfrog(card.BlankCard) :
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('mighty leap','')) :
        super().__init__(species='Bullfrog', cost=1, attack=1, life=2, sigils=sigils, blank_cost=blank_cost)

class BlackGoat(card.BlankCard) :
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('worthy sacrifice','')) :
        super().__init__(species='Black Goat', cost=1, attack=0, life=1, sigils=sigils, blank_cost=blank_cost)

class Beehive(card.BlankCard) :
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('bees within','')) :
        super().__init__(species='Beehive', cost=1, attack=0, life=2, sigils=sigils, blank_cost=blank_cost)

class Cat(card.BlankCard) :
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('many lives','')) :
        super().__init__(species='Cat', cost=1, attack=0, life=1, sigils=sigils, blank_cost=blank_cost)
        self.spent_lives: int = 0
    
    def reset_stats(self) -> None :
        super().reset_stats()
        self.spent_lives = 0

class UndeadCat(card.BlankCard) :
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('','')) :
        super().__init__(species='Undead Cat', cost=1, attack=3, life=6, sigils=sigils, blank_cost=blank_cost)

class MooseBuck(card.BlankCard) :
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('hefty (left)','')) :
        if sigils[0] in ['hefty (left)', 'hefty (right)']:
            if random.randint(0,1) == 0 :
                sigils = ('hefty (left)', sigils[1])
            else :
                sigils = ('hefty (right)', sigils[1])
        super().__init__(species='Moose Buck', cost=4, attack=3, life=7, sigils=sigils, blank_cost=blank_cost)

class Dam(card.BlankCard) : # only given by a sigil
    def __init__(self, blank_cost: bool=True, sigils: tuple[str, str]=('','')) :
        super().__init__(species='Dam', cost=0, attack=0, life=2, sigils=sigils, blank_cost=blank_cost)

class Vole(card.BlankCard) : # only given by a sigil
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('','')) :
        super().__init__(species='Vole', cost=0, attack=0, life=1, sigils=sigils, blank_cost=blank_cost)

class Warren(card.BlankCard) :
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('vole hole','')) :
        super().__init__(species='Warren', cost=1, attack=0, life=2, sigils=sigils, blank_cost=blank_cost)

class Beaver(card.BlankCard) :
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('dam builder','')) :
        super().__init__(species='Beaver', cost=2, attack=1, life=3, sigils=sigils, blank_cost=blank_cost)

class Adder(card.BlankCard) :
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('touch of death','')) :
        super().__init__(species='Adder', cost=2, attack=1, life=1, sigils=sigils, blank_cost=blank_cost)

class CorpseMaggots(card.BlankCard) : # in Leshy's 1 cost and the player's 2 cost groups due to the 3 cost mainly being a deterrent for the player
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('corpse eater','')) :
        super().__init__(species='Corpse Maggots', cost=3, attack=1, life=2, sigils=sigils, blank_cost=blank_cost)

class Otter(card.BlankCard) :
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('waterborne','')) :
        super().__init__(species='Otter', cost=1, attack=1, life=1, sigils=sigils, blank_cost=blank_cost)

class BullShark(card.BlankCard) :
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('waterborne','')) :
        super().__init__(species='Bull Shark', cost=3, attack=4, life=2, sigils=sigils, blank_cost=blank_cost)

class Kingfisher(card.BlankCard) :
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('airborne','waterborne')) :
        super().__init__(species='Kingfisher', cost=1, attack=1, life=1, sigils=sigils, blank_cost=blank_cost)

class Pronghorn(card.BlankCard) :
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('lane shift right', 'bifurcate')) :
        if sigils in [
            ('lane shift right', 'bifurcate'),
            ('lane shift left', 'bifurcate')
        ] :
            if random.randint(0,1) == 0 :
                sigils = ('lane shift right', 'bifurcate')
            else :
                sigils = ('lane shift left', 'bifurcate')
        super().__init__(species='Pronghorn', cost=2, attack=1, life=3, sigils=sigils, blank_cost=blank_cost)

class Salmon(card.BlankCard) : 
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('waterborne', 'lane shift right')) :
        if sigils in [
            ('waterborne', 'lane shift right'),
            ('waterborne', 'lane shift left')
        ] :
            if random.randint(0,1) == 0 :
                sigils = ('waterborne', 'lane shift right')
            else :
                sigils = ('waterborne', 'lane shift left')
        super().__init__(species='Salmon', cost=2, attack=2, life=2, sigils=sigils, blank_cost=blank_cost)

class Louis(card.BlankCard) : # death card
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('waterborne', 'lane shift right')) :
        if sigils in [
            ('waterborne', 'lane shift right'),
            ('waterborne', 'lane shift left')
        ] :
            if random.randint(0,1) == 0 :
                sigils = ('waterborne', 'lane shift right')
            else :
                sigils = ('waterborne', 'lane shift left')
        super().__init__(species='Louis', cost=1, attack=1, life=1, sigils=sigils, blank_cost=blank_cost)

class FlawPeacock(card.BlankCard) : # death card, referencing Flawed Peacock's video on Inscryption, which is how I found out about it
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('bees within','many lives')) :
        super().__init__(species='Flaw Peacock', cost=3, attack=3, life=2, sigils=sigils, blank_cost=blank_cost)

class PlyrDeathCard1(card.BlankCard) : # death card
    def __init__(self, blank_cost: bool=False) :
        data_to_read = [
                    ['death cards', 'first', 'name'],
                    ['death cards', 'first', 'attack'],
                    ['death cards', 'first', 'life'],
                    ['death cards', 'first', 'cost'],
                    ['death cards', 'first', 'sigils'],
                    ['death cards', 'first', 'easter']
                ]
        [death_name, death_attack, death_life, death_cost, death_sigils, death_easter] = QoL.read_data(data_to_read)
        super().__init__(species=death_name, cost=death_cost, attack=death_attack, life=death_life, sigils=death_sigils, blank_cost=blank_cost)
        self.easter: bool = death_easter

class PlyrDeathCard2(card.BlankCard) : # death card
    def __init__(self, blank_cost: bool=False) :
        data_to_read = [
                    ['death cards', 'second', 'name'],
                    ['death cards', 'second', 'attack'],
                    ['death cards', 'second', 'life'],
                    ['death cards', 'second', 'cost'],
                    ['death cards', 'second', 'sigils'],
                    ['death cards', 'second', 'easter']
                ]
        [death_name, death_attack, death_life, death_cost, death_sigils, death_easter] = QoL.read_data(data_to_read)
        super().__init__(species=death_name, cost=death_cost, attack=death_attack, life=death_life, sigils=death_sigils, blank_cost=blank_cost)
        self.easter: bool = death_easter

class PlyrDeathCard3(card.BlankCard) : # death card
    def __init__(self, blank_cost: bool=False) :
        data_to_read = [
                    ['death cards', 'third', 'name'],
                    ['death cards', 'third', 'attack'],
                    ['death cards', 'third', 'life'],
                    ['death cards', 'third', 'cost'],
                    ['death cards', 'third', 'sigils'],
                    ['death cards', 'third', 'easter']
                ]
        [death_name, death_attack, death_life, death_cost, death_sigils, death_easter] = QoL.read_data(data_to_read)
        super().__init__(species=death_name, cost=death_cost, attack=death_attack, life=death_life, sigils=death_sigils, blank_cost=blank_cost)
        self.easter: bool = death_easter

class RabbitPelt(card.BlankCard) : # only given in campaign
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('','')) :
        super().__init__(species='Rabbit Pelt', cost=0, attack=0, life=1, sigils=sigils, blank_cost=blank_cost)

class WolfPelt(card.BlankCard) : # only given in campaign
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('','')) :
        super().__init__(species='Wolf Pelt', cost=0, attack=0, life=2, sigils=sigils, blank_cost=blank_cost)

class GoldenPelt(card.BlankCard) : # only given in campaign
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('','')) :
        super().__init__(species='Golden Pelt', cost=0, attack=0, life=3, sigils=sigils, blank_cost=blank_cost)

class Smoke(card.BlankCard) : # only given in campaign
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('worthy sacrifice', '')) : # will have the bone king sigil once bones are implemented
        super().__init__(species='The Smoke', cost=0, attack=0, life=1, sigils=sigils, blank_cost=blank_cost)

class Coyote(card.BlankCard) : # only used by prospector until bones are implemented
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('','')) :
        super().__init__(species='Coyote', cost=2, attack=2, life=1, sigils=sigils, blank_cost=blank_cost)

class PackMule(card.BlankCard) : # only used by prospector
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('lane shift right','')) :
        super().__init__(species='Pack Mule', cost=0, attack=0, life=5, sigils=sigils, blank_cost=blank_cost)

class Bloodhound(card.BlankCard) : 
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('','')) : # will have guardian sigil once implimented
        super().__init__(species='Bloodhound', cost=2, attack=2, life=3, sigils=sigils, blank_cost=blank_cost)

class GoldNugget(card.BlankCard) : # only used by prospector
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('','')) :
        super().__init__(species='Gold Nugget', cost=0, attack=0, life=2, sigils=sigils, blank_cost=blank_cost)

class BaitBucket(card.BlankCard) : # only used by angler
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('','')) :
        super().__init__(species='Bait Bucket', cost=0, attack=0, life=1, sigils=sigils, blank_cost=blank_cost)

class StrangeFrog(card.BlankCard) : # only used by trapper
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('mighty leap','')) :
        super().__init__(species='Strange Frog', cost=1, attack=1, life=2, sigils=sigils, blank_cost=blank_cost)

class LeapingTrap(card.BlankCard) : # only used by trapper
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('mighty leap','steel trap')) :
        super().__init__(species='Leaping Trap', cost=0, attack=0, life=1, sigils=sigils, blank_cost=blank_cost)

class MoleMan(card.BlankCard) : # lane shift will be replaced with burrower sigil once implemented
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('lane shift left','mighty leap')) :
        super().__init__(species='Mole Man', cost=1, attack=0, life=6, sigils=sigils, blank_cost=blank_cost)

class Stump(card.BlankCard) : # terrain card
    def __init__(self, blank_cost: bool=False, sigils: tuple[str, str]=('','')) :
        super().__init__(species='Stump', cost=0, attack=0, life=3, sigils=sigils, blank_cost=blank_cost)

class Tree(card.BlankCard) : # terrain card
    def __init__(self, blank_cost: bool=False, sigils: None|tuple[str, str]=None, level: int=0):
        if sigils is None :
            sigils = ('mighty leap','')
        match level :
            case _ if level in [0,3] : area_type = 'Grand Fir'
            case 2 : area_type = 'Snowy Fir'
            case _ : area_type = 'Tree'
        super().__init__(species=area_type, cost=0, attack=0, life=3, sigils=sigils, blank_cost=blank_cost)
        self.level: int = level

class Moon(card.BlankCard) :
    # class attributes
    sigils: tuple[str, str] = ('mighty leap','')
    is_poisened: bool = False
    hooked: bool = False
    species: str = 'The Moon'
    saccs: int = 0
    base_attack: int = 1
    current_attack: int = 1
    base_life:int = 40
    current_life: int = 40
    status: str = 'alive'

    def __init__(self, row: int, column: int) :
        self.zone: int = column
        self.coords: tuple[int, int] = (row, column)
        self.ASCII: str = ASCII_text.moon_parts[self.coords[0]][self.coords[1]]
        self.update_ASCII()
    
    def text_by_line(self)  -> str:
        text = self.ASCII.split('\n')[self.line_cursor].format(moon_lines=self.moon_lines, life_lines=ASCII_text.moon_life_lines(Moon.current_life))
        self.line_cursor: int = (self.line_cursor + 1) % 11
        return text.ljust(15)[:15]

    def update_ASCII(self) -> None :
        # reset line cursor
        self.line_cursor: int = 0

        # update ASCII art for card
        inner_str: str = ASCII_text.moon_inner_str()
        split_ASCII: list[list[str]] = ASCII_text.split_moon_lines(inner_str)['cards']
        self.moon_lines: list[str] = [split_ASCII[n][self.coords[1] - 1] for n in range(20)][0+(self.coords[0] == 1)*10:10+(self.coords[0] == 1)*10]

    def explain(self) -> None :
        ### sigils, in order, are : mighty leap, tidal lock, and omni strike

        # set up variables
        tidal_lock_desc = 'Will pull small creatures into its orbit at the start of its turn.'
        omni_strike_desc = 'Will attack every opposing creature. It will attack directly if there are no opposing creatures.'

        # get terminal size
        term_cols = os.get_terminal_size().columns
        card_gaps = (term_cols*55 // 100) // 5 - 15

        # get parameters for sigil descriptions
        s1_max_desc_first = term_cols - 32 - max(card_gaps + 2, 2) - len('mighty leap:')
        s2_max_desc_first = term_cols - 32 - max(card_gaps + 2, 2) - len('tidal lock:')
        s3_max_desc_first = term_cols - 32 - max(card_gaps + 2, 2) - len('omni strike:')
        max_desc_rest = term_cols - 31 - max(card_gaps + 6, 6)

        # split sigil descriptions
        [s1_desc_1, s1_desc_2, s1_desc_3] = QoL.split_nicely(sigils.Dict['mighty leap'][1], s1_max_desc_first, max_desc_rest, max_lines=3, add_blank_lines=True)
        [s2_desc_1, s2_desc_2, s2_desc_3] = QoL.split_nicely(tidal_lock_desc, s2_max_desc_first, max_desc_rest, max_lines=3, add_blank_lines=True)
        [s3_desc_1, s3_desc_2, s3_desc_3] = QoL.split_nicely(omni_strike_desc, s3_max_desc_first, max_desc_rest, max_lines=3, add_blank_lines=True)

        # create display text
        explanation = r"""{card_gap},-----------------------------,
{card_gap}|The Moon                     |{card_gap}  Mighty Leap: {s1_desc_1}
{card_gap}|                             |{card_gap}      {s1_desc_2}
{card_gap}|    _____           ˏ--/ˎ    |{card_gap}      {s1_desc_3}
{card_gap}|    ʅ   ʃ           | / |    |{card_gap}  Tidal Lock: {s2_desc_1}
{card_gap}|    ɩð_ʃ    ,---,   ῾/--᾽    |{card_gap}      {s2_desc_2}
{card_gap}|            |   |            |{card_gap}      {s2_desc_3}
{card_gap}|           /'---'\           |{card_gap}  Omni Strike: {s3_desc_1}
{card_gap}|          /  / \  \    {p} /   |{card_gap}      {s3_desc_2}
{card_gap}|         \/ \/ \/ \/    / {l} |{card_gap}      {s3_desc_3}
{card_gap}'-----------------------------'""".format(card_gap=' '*(card_gaps), s1_desc_1=s1_desc_1, s1_desc_2=s1_desc_2, s1_desc_3=s1_desc_3, s2_desc_1=s2_desc_1, s2_desc_2=s2_desc_2, s2_desc_3=s2_desc_3, s3_desc_1=s3_desc_1, s3_desc_2=s3_desc_2, s3_desc_3=s3_desc_3, p=1, l=str(Moon.current_life).ljust(2))
        
        # print display text
        print(explanation)

    def attack(self, front_left_card: card.BlankCard, front_card: card.BlankCard, front_right_card: card.BlankCard, hand: list[card.BlankCard], is_players: bool=False, bushes: dict[int, card.BlankCard]={}) -> int :
        # set up variables
        points = 0

        # attack cards
        if front_card.species != '' :
            points = front_card.take_damage(Moon.current_attack, hand, in_opp_field=is_players, bushes=bushes)
        
        # if poisoned, deal 1 damage to self
        if Moon.is_poisoned :
            self.take_damage(1, hand)

        return points

    def reset_stats(self) -> None :
        self.zone = 0
        Moon.status = 'alive'
        Moon.is_poisoned = False
        Moon.hooked = False
        Moon.current_attack = Moon.base_attack
        Moon.current_life = Moon.base_life
        self.update_ASCII()

    def take_damage(self, damage: int, hand: list[card.BlankCard], from_air: bool=False, in_opp_field: bool=False, in_bushes: bool=False, bushes: dict[int, card.BlankCard]={}, deathtouch: bool=False) -> int :
        # set up variables
        teeth = 0

        # take damage (mighty leap is hardcoded due to the moon's unique nature)
        if Moon.species == '' or Moon.status == 'dead' :
            teeth = damage
        else :
            prev_life = Moon.current_life
            Moon.current_life -= damage
            self.update_ASCII()
            if Moon.current_life <= 0 or deathtouch :
                Moon.status = 'dead'
        
        return teeth   

    def play(self, zone: int) -> None :
        if zone not in range (1, 5) : # error handling
            raise ValueError('Zone must be between 1 and 4')
        self.reset_stats()
        self.zone = zone
        self.update_ASCII()

    def sigil_in_category(self, category: list[str] | dict[int, str], sigil_slot: int=-1) -> bool :
        sigils_ = ['mighty leap', 'tidal lock', 'omni strike']

        return any([sigil in sigils_ for sigil in category])

    def has_sigil(self, sigil_name: str) -> bool :
        sigils_ = ['mighty leap', 'tidal lock', 'omni strike']

        return any([sigil == sigil_name for sigil in sigils_])

    def hook(self) -> None :
        Moon.hooked = not Moon.hooked
        self.update_ASCII()

# Allowed cards:
Poss_Playr: dict[int, list[type[card.BlankCard]]] = {
    0 : [Rabbit, Shrew],
    1 : [DumpyTF, Turtle, Stoat, Bullfrog, Beehive, Cat, Warren, Otter, Kingfisher, MoleMan, BlackGoat],
    2 : [Ouroboros, Asp, Falcon, Cockroach, Wolf, Raven, Beaver, Adder, CorpseMaggots, Pronghorn, Salmon, Bloodhound],
    3 : [Lobster, Grizzly, BullShark],
    4 : [BoppitW, Urayuli, MooseBuck]
}
Poss_Leshy: dict[int, list[type[card.BlankCard]]] = {
    0 : [OppositeRabbit, OppositeShrew],
    1 : [DumpyTF, Turtle, Stoat, Bullfrog, CorpseMaggots, Otter, Kingfisher, MoleMan],
    2 : [Asp, Falcon, Cockroach, Wolf, Raven, Adder, Pronghorn, Salmon, Bloodhound],
    3 : [Lobster, Grizzly, BullShark, BoppitW]
}
Poss_Death: list[type[card.BlankCard]] = [Louis, FlawPeacock, PlyrDeathCard1, PlyrDeathCard2, PlyrDeathCard3]
Rare_Cards: list[type[card.BlankCard]] = [Ouroboros, Urayuli, MooseBuck, BullShark, BoppitW, MoleMan]
Terrain_Cards: list[type[card.BlankCard]] = [Stump, Tree]

# Tribes
Reptiles: list[type[card.BlankCard]] = [Bullfrog, DumpyTF, Turtle, Adder, Asp, Ouroboros, StrangeFrog] # also includes amphibians for accuracy to Inscryption
Insects: list[type[card.BlankCard]] = [BoppitW, Beehive, Bee, Cockroach, CorpseMaggots]
Avians: list[type[card.BlankCard]] = [Kingfisher, Falcon, Raven]
Canines: list[type[card.BlankCard]] = [Wolf, Bloodhound, Coyote]
Hooved: list[type[card.BlankCard]] = [BlackGoat, MooseBuck, Pronghorn, PackMule]
Squirrels: list[type[card.BlankCard]] = [Squirrel]

# categories for Leshy's AI
AI_categories: list[dict[str, Any]] = [
    # good against airbornes (glass cannons and those with mighty leap)
    {
        'category' : 'anti_air', 
        'self sigils' : ['mighty leap'],
        'opp sigils' : ['airborne'],
        'stats' : (lambda self_attack, self_life, opp_attack, opp_life : self_attack >= 3 and self_life <= opp_attack)
        },
    # good against deathtouch (waterbornes and those with deathtouch)
    {
        'category' : 'anti_deathtouch',
        'self sigils' : ['waterborne','touch of death'],
        'opp sigils' : ['touch of death'],
        'stats' : (lambda self_attack, self_life, opp_attack, opp_life : False)
        },
    # good against waterbornes (tanks and those with waterborne)
    {
        'category' : 'anti_water',
        'self sigils' : ['waterborne'],
        'opp sigils' : ['waterborne'],
        'stats' : (lambda self_attack, self_life, opp_attack, opp_life : self_life >= opp_attack * 3)
        },
    # good against bifurcates (glass cannons)
    {
        'category' : 'anti_bifurcate',
        'self sigils' : ['touch of death','venom'],
        'opp sigils' : ['bifurcate'],
        'stats' : (lambda self_attack, self_life, opp_attack, opp_life : self_attack >= 3 and self_life <= opp_attack)
        },
    # good against those with on hurt effects (pure tanks, airbornes, and bifurcates)
    {
        'category' : 'wont_hurt',
        'self sigils' : ['airborne','bifurcate'],
        'opp sigils' : ['bees within','split','unkillable', 'steel trap'],
        'stats' : (lambda self_attack, self_life, opp_attack, opp_life : self_attack == 0)
        },
    # good against those with venom (tanks and waterbornes)
    {
        'category' : 'anti_venom',
        'self sigils' : ['waterborne'],
        'opp sigils' : ['venom'],
        'stats' : (lambda self_attack, self_life, opp_attack, opp_life : self_life >= opp_attack * 2 + 2)
        },
    # good against those moving right (heavy hitters, moves with, and bifurcate)
    {
        'category' : 'anti_right',
        'self sigils' : ['lane shift right','hefty (right)', 'bifurcate'],
        'opp sigils' : ['lane shift right','hefty (right)'],
        'stats' : (lambda self_attack, self_life, opp_attack, opp_life : self_attack >= opp_life)
        },
    # good against those moving left (heavy hitters, moves with, and bifurcate)
    {
        'category' : 'anti_left',
        'self sigils' : ['lane shift left','hefty (left)', 'bifurcate'],
        'opp sigils' : ['lane shift left','hefty (left)'],
        'stats' : (lambda self_attack, self_life, opp_attack, opp_life : self_attack >= opp_life)
        },
]

if __name__ == '__main__' :
    import deck
    Leshy_cardlist = deck.Deck([])
    for cost in Poss_Leshy :
        for card_ in Poss_Leshy[cost] :
            Leshy_cardlist.add_card(card_(True)) # type: ignore

    Player_cardlist = deck.Deck([])
    for cost in Poss_Playr :
        for card_ in Poss_Playr[cost] :
            if card_ not in Player_cardlist.cards :
                Player_cardlist.add_card(card_())

    QoL.clear()
    print(QoL.center_justified('Leshy Card List'))
    print()
    print(Leshy_cardlist)
    print()
    print(QoL.center_justified('Player Card List'))
    print()
    print(Player_cardlist)