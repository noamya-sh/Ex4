import json
from unittest import TestCase

from Pokemon import Pokemon



class TestPokemon(TestCase):
    def test_get_pos(self):
        p: Pokemon=Pokemon(5,-1,"32.0,35.0,")
        self.assertEqual(p.get_pos(),(32.0, 35.0, 0.0))
        p: Pokemon = Pokemon(5, -1, "43.0,32.0,")
        self.assertEqual(p.get_pos(), (43.0, 32.0, 0.0))
        p: Pokemon = Pokemon(5, -1, "12.0,25.0,")
        self.assertEqual(p.get_pos(), (12.0, 25.0, 0.0))

    def test_get_type(self):
        p: Pokemon = Pokemon(5, -1, "32.0,35.0,")
        self.assertEqual(p.get_type(), -1)
        p: Pokemon = Pokemon(5, 1, "34.0,45.0,")
        self.assertEqual(p.get_type(), 1)
        p: Pokemon = Pokemon(5, 1, "12.0,32.0,")
        self.assertEqual(p.get_type(), 1)

    def test_get_value(self):
        p: Pokemon = Pokemon(7, -1, "32.0,35.0,")
        self.assertEqual(p.get_value(), 7)
        p: Pokemon = Pokemon(5, 1, "34.0,45.0,")
        self.assertEqual(p.get_value(), 5)
        p: Pokemon = Pokemon(12, 1, "12.0,32.0,")
        self.assertEqual(p.get_value(), 12)
