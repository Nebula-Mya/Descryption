import unittest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import card_library
import QoL

class TestOuroborosLevelUp(unittest.TestCase):

    def setUp(self):
        self.prev_level = QoL.read_data([['progress markers', 'ouro level']])[0]
        QoL.write_data([(['progress markers', 'ouro level'], 1)])

    def tearDown(self):
        QoL.write_data([(['progress markers', 'ouro level'], self.prev_level)])

    def test_ouroboros_level_up(self):
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

# Run the test
if __name__ == '__main__':
    unittest.main()