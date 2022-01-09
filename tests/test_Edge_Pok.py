from unittest import TestCase

from Edge_Pok import Edge_Pok


class TestEdge_Pok(TestCase):

    def test_get_pokemons(self):
        ep:Edge_Pok= Edge_Pok((3,6),"32.0,35.0,0.0")
        self.assertEqual(ep.get_pokemons(),["32.0,35.0,0.0"])
        ep: Edge_Pok = Edge_Pok((3, 6), "12.0,45.0,0.0")
        self.assertEqual(ep.get_pokemons(), ["12.0,45.0,0.0"])

    def test_get_edge(self):
        ep:Edge_Pok= Edge_Pok((3,6))
        self.assertEqual(ep.get_edge(),(3,6))
        ep: Edge_Pok = Edge_Pok((0,11))
        self.assertEqual(ep.get_edge(), (0,11))

    def test_get_value(self):
        ep:Edge_Pok= Edge_Pok((3,6))
        self.assertEqual(ep.get_value(),0)

    def test_add_value(self):
        ep: Edge_Pok = Edge_Pok((3, 6))
        self.assertEqual(ep.get_value(), 0)
        ep.add_value(8)
        self.assertEqual(ep.get_value(), 8)
        ep.add_value(4)
        self.assertEqual(ep.get_value(), 12)

    def test_set_is_attached(self):
        ep:Edge_Pok= Edge_Pok((3,6))
        ep.set_is_attached(True)
        self.assertEqual(ep.get_is_attached(),True)
        ep.set_is_attached(False)
        self.assertEqual(ep.get_is_attached(), False)