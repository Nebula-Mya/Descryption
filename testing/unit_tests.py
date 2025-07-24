import unittest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import card
import deck
import rogue
import card_library
import QoL

class Test_Ouroboros_Level_Up(unittest.TestCase):

    def setUp(self) -> None :
        self.prev_level = QoL.read_data([['progress markers', 'ouro level']])[0]
        QoL.write_data([(['progress markers', 'ouro level'], 1)])

    def tearDown(self) -> None :
        QoL.write_data([(['progress markers', 'ouro level'], self.prev_level)])

    def test_ouroboros_level_up(self) -> None :
        # Create multiple instances of Ouroboros
        ouroboros1 = card_library.Ouroboros()
        ouroboros2 = card_library.Ouroboros()

        # Test initial values for base_attack and base_life
        with self.subTest(msg="initial values"):
            self.assertEqual(ouroboros1.base_attack, ouroboros1.oro_level)
            self.assertEqual(ouroboros1.base_life, ouroboros1.oro_level)
            self.assertEqual(ouroboros2.base_attack, ouroboros2.oro_level)
            self.assertEqual(ouroboros2.base_life, ouroboros2.oro_level)
            self.assertEqual(card_library.Ouroboros.oro_level, 1)

        # Level up the first instance
        ouroboros1.level_up()

        # Test values after level up
        with self.subTest(msg="values after 1's level up"):
            self.assertEqual(ouroboros1.base_attack, ouroboros1.oro_level)
            self.assertEqual(ouroboros1.base_life, ouroboros1.oro_level)
            self.assertEqual(card_library.Ouroboros.oro_level, 2)

        # Ensure the second instance remains unchanged
        with self.subTest(msg="2's values unchanged"):
            self.assertEqual(ouroboros2.base_attack, ouroboros2.oro_level - 1)
            self.assertEqual(ouroboros2.base_life, ouroboros2.oro_level - 1)

        # Level up the second instance
        ouroboros2.level_up()

        # Test values after level up
        with self.subTest(msg="values after 2's level up"):
            self.assertEqual(ouroboros2.base_attack, ouroboros2.oro_level - 1)
            self.assertEqual(ouroboros2.base_life, ouroboros2.oro_level - 1)
            self.assertEqual(card_library.Ouroboros.oro_level, 3)

# class Test_Events(unittest.TestCase):

#     def setUp(self) -> None:
#         self.default_deck: list[card.BlankCard] = [card_library.Rabbit(), card_library.Stoat(), card_library.Wolf(), card_library.GoldenPelt(), card_library.GoldenPelt()]
#         self.campaign = rogue.rogue_campaign(self.default_deck, 0, 2)
        
#         weights = rogue.event_weights(self.campaign, [])
#         self.assertEqual([1,1,1,1,1,1,1,7], weights)

#     def test_prev(self) -> None :
#         # odds
#         prev = [1,3,5,7]
#         weights = rogue.event_weights(self.campaign, prev)
#         self.assertEqual([0,1,0,1,0,1,0,3], weights)

#         # evens 
#         prev = [2,4,6,8]
#         weights = rogue.event_weights(self.campaign, prev)
#         self.assertEqual([1,0,1,0,1,0,1,0], weights)

#     def test_small_deck(self) -> None :
#         self.campaign.remove_card(self.default_deck[0]) # 5 -> 4

#         weights = rogue.event_weights(self.campaign, [])
#         self.assertEqual([1,0,0,1,1,1,1,5], weights)

#         self.campaign.remove_card(self.default_deck[0]) # 4 -> 3

#         weights = rogue.event_weights(self.campaign, [])
#         self.assertEqual([1,0,0,1,1,1,1,0], weights)

#     def test_full_sigils(self) -> None :
#         for i in range(0,5) :
#             _card = self.campaign.player_deck.cards[i]
#             _card.sigils = ("airborne", "venom")

#         weights = rogue.event_weights(self.campaign, [])
#         self.assertEqual([1,0,1,1,1,1,1,6], weights)

#     def test_matching(self) -> None :
#         self.campaign.remove_card(self.default_deck[4])
#         self.campaign.add_card(card_library.RabbitPelt())

#         weights = rogue.event_weights(self.campaign, [])
#         self.assertEqual([1,1,0,1,1,1,1,6], weights)

#     def test_pelts(self) -> None :
#         self.campaign.remove_card(self.default_deck[4])
#         self.campaign.remove_card(self.default_deck[3])
#         self.campaign.add_card(card_library.Bee())
#         self.campaign.add_card(card_library.Bee())

#         weights = rogue.event_weights(self.campaign, [])
#         self.assertEqual([1,1,1,1,0,1,1,6], weights)

class Test_Deck(unittest.TestCase):
    def setUp(self) -> None:
        self.known_card = card_library.Rabbit()
        self.deck = deck.Deck([self.known_card, card_library.Stoat(), card_library.Wolf(), card_library.GoldenPelt(), card_library.GoldenPelt()])
    
    def test_add(self) -> None :
        new_card = card_library.Adder()
        self.assertNotIn(new_card, self.deck)
        self.deck.add_card(new_card)
        self.assertIn(new_card, self.deck)

    def test_rem(self) -> None :
        idx = QoL.sort_deck(self.deck.cards).index(self.known_card)
        self.assertIn(self.known_card, self.deck)
        self.deck.remove_card(idx)
        self.assertNotIn(self.known_card, self.deck)

# Run the tests
if __name__ == '__main__':
    unittest.main()