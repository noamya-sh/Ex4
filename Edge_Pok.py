class Edge_Pok:
    """
    Represent an edge in a graph that has Pokemon (one or more) on it.
    """
    def __init__(self, edge: tuple, pos: str = None):
        self._edge = edge
        self._is_attached = False
        self._pokemons = []
        self._value = 0
        if pos:
            self._pokemons.append(pos)

    def get_is_attached(self)->bool:
        """
        :return: If there's an agent going to this edge.
        """
        return self._is_attached

    def get_pokemons(self)->list:
        """
        :return: list of all pos of Pokemons in this edge
        """
        return self._pokemons

    def get_edge(self)->tuple:
        return self._edge

    def get_value(self)->float:
        """
        :return: sum of pokemons values on this edge.
        """
        return self._value

    def add_value(self, v):
        self._value += v

    def set_is_attached(self, b: bool):
        self._is_attached = b

    def __lt__(self, other):
        return self._value < other._value
