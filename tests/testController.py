
from unittest import TestCase

from Controller import Controller



class TestController(TestCase):

    def test_is_run(self):
        """
        !! run the server befor run this function !!
        :return:
        """
        c = Controller()
        c.client.start()
        self.assertEqual(c.is_run(), True)

    def test_init_graph(self):
        """
        !! run the server befor run this function with case 8 !!
        :return:
        """
        c = Controller()
        c.set_start()
        self.assertEqual(c.get_graph().number_of_nodes(), 31)
        c.client.stop_connection()

    def test_get_grade(self):
        """
        !! run the server befor run this function!!
        """
        c = Controller()
        c.set_start()
        self.assertEqual(c.get_grade(), 0)
        c.client.stop_connection()
