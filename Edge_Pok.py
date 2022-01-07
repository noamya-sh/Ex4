class Edge_Pok:
    def __init__(self, edge: tuple, pos: str = None):
        self._edge = edge
        self._is_attached = False
        self._pokemons = []
        self._value = 0
        if pos:
            self._pokemons.append(pos)

    def get_is_attached(self):
        return self._is_attached

    def get_pokemons(self):
        return self._pokemons

    def get_edge(self):
        return self._edge

    def get_value(self):
        return self._value

    def add_value(self, v):
        self._value += v

    def set_is_attached(self, b: bool):
        self._is_attached = b

    def __lt__(self, other):
        return self._value < other._value