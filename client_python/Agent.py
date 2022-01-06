from Pokemon import *


# k = 0


class Agent:


    def __init__(self, id: int, value: float, src: int, dest: int, speed: float, pos: str) -> None:
        self.id = id
        self._value = value
        self.src = src
        self.dest = dest
        self.speed = speed
        x, y, _ = pos.split(",")
        self._pos = (float(x), float(y), 0.0)
        self.dict_pok = {}
        self.old_pok = 0


    def add_pok(self, p: Pokemon, edge) -> None:
        self.dict_pok[p] = edge

    def remove_pok(self, p: Pokemon):
        del self.dict_pok[p]
        self.old_pok += 1

    def update(self, value, src, dest, speed, pos):
        self._value = value
        self.src = src
        self.dest = dest
        self.speed = speed
        x, y, _ = pos.split(",")
        self._pos = (float(x), float(y), 0.0)

    def timeSpeed(self):
        return