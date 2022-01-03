import json
import math
from typing import List

from Agent import *
from Pokemon import *
from client import *
import networkx as nx
import numpy as np

PORT = 6666
HOST = '127.0.0.1'


class Controller:
    def __init__(self):
        client = Client()
        client.start_connection(HOST, PORT)
        self._graph = self.init_graph(client.get_graph())
        self.dict_path = {}
        d = json.loads(client.get_pokemons())
        self.pokemons = [Pokemon(**p['Pokemon']) for p in d['Pokemons']]

    def init_graph(self, json_str) -> nx.DiGraph:
        dg = nx.DiGraph()
        d = json.loads(json_str)
        for node in d['Nodes']:
            x, y, _ = node['pos'].split(",")
            pos = (float(x), float(y), 0.0)
            dg.add_node(node['id'], pos=pos)
        for edge in d['Edges']:
            dg.add_edge(edge['src'], edge['dest'], weight=edge['w'])
        return dg

    def init_agents(self, agents: list[Agent]) -> None:
        for a in agents:
            self.dict_path[a.id] = []

    def get_graph(self):
        return self._graph

    def get_next(self, id: int) -> int:
        if not self.dict_path[id]:
            return None
        return self.dict_path[id][0]

    def _on_edge(self, p: Pokemon, edge) -> bool:
        node_1 = self._graph.nodes[edge[0]]
        node_2 = self._graph.nodes[edge[1]]
        edge_type = 1 if edge[0] < edge[1] else -1
        if p.get_type() != edge_type:
            return False
        pos_1 = node_1['pos']
        pos_2 = node_2['pos']
        pos = p.get_pos()
        x1, x2, x3 = pos_1[0], pos_2[0], pos[0]
        y1, y2, y3 = pos_1[1], pos_2[1], pos[1]
        p1 = np.array([x1, y1])
        p2 = np.array([x2, y2])
        p3 = np.array([x3, y3])
        d = np.linalg.norm(np.cross(p2 - p1, p1 - p3)) / np.linalg.norm(p2 - p1)
        return math.isclose(0, d, abs_tol=1e-09)

    def find_edge(self, p: Pokemon) -> tuple:
        for e in self._graph.edges.data():
            if self._on_edge(p, e):
                return e
        return None

    def _get_new_pokemons(self, curr: List[Pokemon]) -> List[Pokemon]:
        return [p for p in curr if p not in self.pokemons]

    def _update_pokemons(self):
        d = json.loads(client.get_pokemons())
        curr = [Pokemon(**p['Pokemon']) for p in d['Pokemons']]
        new_p = self._get_new_pokemons(curr)
        for p in new_p:
            self.attach(p)

    def attach(self, p: Pokemon):
        pass


if __name__ == '__main__':
    PORT = 6666
    # server host (default localhost 127.0.0.1)
    HOST = '127.0.0.1'
    client = Client()
    client.start_connection(HOST, PORT)
    graph_json = client.get_graph()
    d = Controller(graph_json)
    print(d._graph.edges.data())
    data = json.loads(client.get_pokemons())
    print(data)
    pokemons = [Pokemon(**p['Pokemon']) for p in data['Pokemons']]
    for p in pokemons:
        print(d.find_edge(p))
