class Edge_Pok:
    def __init__(self, edge: tuple, pos: str = None):
        self._edge = edge
        self._toAgent = False
        self._pokemons = []
        self._value = 0
        if pos:
            self._pokemons.append(pos)

    def get_toAgent(self):
        return self._toAgent

    def get_pokemons(self):
        return self._pokemons

    def get_edge(self):
        return self._edge

    def get_value(self):
        return self._value

    def add_value(self, v):
        self._value += v

    def set_toAgent(self, b: bool):
        self._toAgent = b
