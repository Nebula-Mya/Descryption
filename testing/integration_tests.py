from __future__ import annotations
import random
import unittest
from typing import TYPE_CHECKING
if TYPE_CHECKING :
    from typing import Callable

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import sigils
import card
import card_library
import duel
import QoL
import rogue
import bosses
import ASCII_text

class Test_ASCII(unittest.TestCase):

    def test_title(self) -> None:
        print()
        ASCII_text.print_title()

    def test_win(self) -> None:
        print()
        ASCII_text.print_win(3)

    def test_lose(self) -> None:
        print()
        ASCII_text.print_lose()
        
    def test_score(self) -> None:
        print()
        term_cols = os.get_terminal_size().columns
        card_gaps = (term_cols*55 // 100) // 5 - 15
        if card_gaps <= 0 :
            score_gap = 28
        else :
            score_gap = card_gaps*9 + 28
        ASCII_text.print_scales({'player': 6, 'opponent': 2}, score_gap)

    def test_WiP(self) -> None:
        print()
        ASCII_text.print_WiP()

    def test_lives(self) -> None:
        print()
        ASCII_text.print_candelabra((2,3,0))

    def test_sigils(self) -> None:
        print()
        sigil_cards: list[card.BlankCard] = []

        for sigil in sigils.Dict.keys():
            sigil_cards.append(card.BlankCard(sigils=(sigil,"")))
        
        QoL.print_deck(sigil_cards)
        
class Test_Bosses(unittest.TestCase):

    def setUp(self) -> None: #REMINDME: maybe use a set deck
        deck_size = 20
        self.campaign = rogue.rogue_campaign(duel.deck_gen(card_library.Poss_Playr, deck_size).cards, 0, 2)
        
        print()
        print(QoL.center_justified('Current deck: '))
        self.campaign.print_deck()

        input(QoL.center_justified('Press enter to continue...').rstrip())

    def tearDown(self) -> None:
        print()
        print(QoL.center_justified('Current deck: '))
        self.campaign.print_deck()

    def test_prospector(self) -> None:
        print(bosses.boss_fight_prospector(self.campaign))

    def test_angler(self) -> None: 
        print(bosses.boss_fight_angler(self.campaign))

    def test_janus(self) -> None:
        print(bosses.boss_fight_janus(self.campaign))

    def test_leshy(self) -> None:
        print(bosses.boss_fight_leshy(self.campaign))

class Test_Events(unittest.TestCase):

    def setUp(self) -> None:
        # deck_size = random.randint(2,16)
        self.campaign = rogue.rogue_campaign(duel.deck_gen(card_library.Poss_Playr, 20).cards, 0, 2)

        data_to_read = [
            ['death cards', 'first', 'name'],
            ['death cards', 'first', 'attack'],
            ['death cards', 'first', 'life'],
            ['death cards', 'first', 'cost'],
            ['death cards', 'first', 'sigils'],
            ['death cards', 'first', 'easter'],
            ['death cards', 'second', 'name'],
            ['death cards', 'second', 'attack'],
            ['death cards', 'second', 'life'],
            ['death cards', 'second', 'cost'],
            ['death cards', 'second', 'sigils'],
            ['death cards', 'second', 'easter'],
            ['death cards', 'third', 'name'],
            ['death cards', 'third', 'attack'],
            ['death cards', 'third', 'life'],
            ['death cards', 'third', 'cost'],
            ['death cards', 'third', 'sigils'],
            ['death cards', 'third', 'easter']
        ]
        death_card_data = QoL.read_data(data_to_read)
        self.death_card_write = [(data_to_read[ind], death_card_data[ind]) for ind in range(len(data_to_read))]

    def tearDown(self) -> None:
        current_death_cards: list[card.BlankCard] = [card_library.PlyrDeathCard1(), card_library.PlyrDeathCard2(), card_library.PlyrDeathCard3()]

        # print the menu
        print()
        print(QoL.center_justified('Current death cards: '))
        QoL.print_deck(current_death_cards, centered=True)
                
        print()
        print(QoL.center_justified('Current deck: '))
        self.campaign.print_deck()

        input(QoL.center_justified('Press Enter to restore death cards...').rstrip())
        QoL.write_data(self.death_card_write)

    def gen_setUp(self) -> None: 
        print()
        print(QoL.center_justified('Current deck: '))
        self.campaign.print_deck()

        input(QoL.center_justified('Press enter to continue...').rstrip())

    def buy_split_setUp(self) -> None:
        print()
        print(QoL.center_justified('Current deck: '))
        self.campaign.print_deck()

        self.campaign.add_card(card_library.RabbitPelt())
        self.campaign.add_card(card_library.WolfPelt())
        self.campaign.add_card(card_library.GoldenPelt())
        self.campaign.add_teeth(10)
        
        input(QoL.center_justified('Press enter to continue...').rstrip())

    def end_setUp(self) -> None:
        current_death_cards: list[card.BlankCard] = [card_library.PlyrDeathCard1(), card_library.PlyrDeathCard2(), card_library.PlyrDeathCard3()]

        # print the menu
        print()
        print(QoL.center_justified('Current death cards: '))
        QoL.print_deck(current_death_cards, centered=True)

        input(QoL.center_justified('Press enter to continue...').rstrip())

    def test_battle(self) -> None:
        self.gen_setUp()
        rogue.card_battle(self.campaign)

    def test_card_choice(self) -> None:
        self.gen_setUp()
        rogue.card_choice(self.campaign)

    def test_sac(self) -> None:
        self.gen_setUp()
        rogue.sigil_sacrifice(self.campaign)

    def test_merge(self) -> None:
        self.gen_setUp()
        rogue.merge_cards(self.campaign)

    def test_buy_pelts(self) -> None:
        self.buy_split_setUp()
        rogue.pelt_shop(self.campaign)

    def test_buy_cards(self) -> None:
        self.buy_split_setUp()
        rogue.card_shop(self.campaign)

    def test_rocks(self) -> None:
        self.gen_setUp()
        rogue.break_rocks(self.campaign)

    def test_campfire(self) -> None:
        self.gen_setUp()
        rogue.campfire(self.campaign)

    def test_death_card(self) -> None:
        self.end_setUp()
        rogue.add_death_card(self.campaign)

    def test_lose(self) -> None:
        self.end_setUp()
        rogue.lost_run(self.campaign)

    def test_win(self) -> None:
        self.end_setUp()
        rogue.beat_leshy(self.campaign)

    def test_split(self) -> None:
        self.buy_split_setUp()
        rogue.split_road(self.campaign)

    def test_map(self) -> None:
        
        def event_choice(campaign: rogue.rogue_campaign, prev: list[rogue.Event_Type]) -> rogue.Event_Type:
            bool_to_bin: Callable[[bool, int], int] = lambda bool_, int_=1 : int_ if bool_ else 0

            weights: list[int] = [
                bool_to_bin(rogue.Event_Type.CARD_CHOICE not in prev),

                bool_to_bin(rogue.Event_Type.SIGIL_SACRIFICE not in prev),

                bool_to_bin(rogue.Event_Type.MERGE_CARDS not in prev),
                
                bool_to_bin(rogue.Event_Type.PELT_SHOP not in prev),
                
                bool_to_bin(rogue.Event_Type.CARD_SHOP not in prev),
                
                bool_to_bin(rogue.Event_Type.BREAK_ROCKS not in prev),
                
                bool_to_bin(rogue.Event_Type.CAMPFIRE not in prev)
            ]

            weights.append(bool_to_bin(rogue.Event_Type.CARD_BATTLE not in prev, int_=sum(weights)))

            return rogue.Event_Type(random.choices(range(1,9), weights=weights)[0])

        start_node = rogue.map_gen(self.campaign, event_choice)

        QoL.ping({"rows": start_node[1]} | start_node[0].var_tree())

class Test_Deck(unittest.TestCase):
    def test_print(self) -> None :
        test_deck_player = duel.deck_gen(card_library.Poss_Playr, 16)
        test_deck_opponent = duel.deck_gen(card_library.Poss_Leshy, 16)

        # display decks
        QoL.clear()
        print('Possible player deck:')
        print(test_deck_player)
        print()
        print('Possible opponent deck:')
        print(test_deck_opponent)

# Run the tests
if __name__ == '__main__':
    unittest.main()