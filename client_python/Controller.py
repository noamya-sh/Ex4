from Agent import *


class Controller:
    def __init__(self, graph):
        self._graph = graph
        self.dict_path = {}

    def init_agents(self, agents: list[Agent]) -> None:
        for a in agents:
            self.dict_path[a.id] = []

    def get_next(self, id: int) -> int:
        if not self.dict_path[id]:
            return None
        return self.dict_path[id][0]

    # def find_edge(self,pos):


