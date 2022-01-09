from unittest import TestCase

from Agent import Agent


class TestAgent(TestCase):
    def test_get_pos(self):
        a: Agent=Agent(1,30,3,7,5.0,"32.0, 35.0, 0.0")
        self.assertEqual(a.get_pos(),(32.0,35.0,0.0))
        b: Agent = Agent(1, 30, 3, 7, 5.0, "12.0, 45.0, 0.0")
        self.assertEqual(b.get_pos(), (12.0, 45.0, 0.0))
