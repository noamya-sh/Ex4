import json
import math
import random
from typing import List
from Edge_Pok import Edge_Pok
from Agent import Agent
from Pokemon import Pokemon
from client_python.client import Client
import networkx as nx
import numpy as np

PORT = 6666
HOST = '127.0.0.1'


def dist(p1: tuple, p2: tuple):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def init_graph(json_str) -> nx.DiGraph:
    dg = nx.DiGraph()
    d = json.loads(json_str)
    for node in d['Nodes']:
        x, y, _ = node['pos'].split(",")
        pos = (float(x), float(y), 0.0)
        dg.add_node(node['id'], pos=pos)
    for edge in d['Edges']:
        dg.add_edge(edge['src'], edge['dest'], weight=edge['w'])
    return dg


class Controller:
    def __init__(self):
        self.client = Client()
        self.client.start_connection(HOST, PORT)
        self.client.log_in("316503986")
        self._graph = init_graph(self.client.get_graph())

        self.pokemons = {}
        d = json.loads(self.client.get_pokemons())
        tmp = [Pokemon(**p['Pokemon']) for p in d['Pokemons']]

        for p in tmp:
            edge = self._find_edge(p)
            self.pokemons[edge] = Edge_Pok(p.get_pos())  # p.value
            # else:
            #     self.pokemons[edge] += p.value

        self.dict_path = {}
        d = json.loads(self.client.get_info())
        k = d['GameServer']['agents']
        self.pokemons = dict(sorted(self.pokemons.items(), key=lambda t: t[1]))
        # to check
        cmp = []
        i = 0
        it = iter(self.pokemons.keys())
        while i < k and i < len(self.pokemons):
            ed = next(it)
            cmp.append(ed[0])
            self.client.add_agent("{\"id\":" + str(ed[0]) + "}")
            i += 1
        while i < k:
            x = random.randint(0, self._graph.number_of_nodes() - 1)
            if x not in cmp:
                self.client.add_agent("{\"id\":" + str(x) + "}")
                cmp.append(x)
                i += 1

        d = json.loads(self.client.get_agents())
        self.agents = {a['Agent']['id']: Agent(**a['Agent']) for a in d['Agents']}
        for k, v in self.agents.items():
            self.dict_path[k] = [v.get_src()]

    def get_graph(self):
        return self._graph

    def _get_next(self, ag: Agent) -> int:
        if not self.dict_path[ag.get_id()]:
            return None
        if ag.get_src() == self.dict_path[ag.get_id()][0] and len(self.dict_path[ag.get_id()]) > 1:
            self.dict_path[ag.get_id()].pop(0)
        return self.dict_path[ag.get_id()][0]

    def _on_edge(self, p: Pokemon, edge) -> bool:
        node_1 = self._graph.nodes[edge[0]]
        node_2 = self._graph.nodes[edge[1]]
        edge_type = 1 if edge[0] < edge[1] else -1
        if p.get_type() != edge_type:
            return False
        p1 = node_1['pos']
        p2 = node_2['pos']
        p3 = p.get_pos()
        p1 = np.array([p1[0], p1[1]])
        p2 = np.array([p2[0], p2[1]])
        p3 = np.array([p3[0], p3[1]])
        d = np.linalg.norm(np.cross(p2 - p1, p1 - p3)) / np.linalg.norm(p2 - p1)
        return math.isclose(0, d, abs_tol=1e-09)

    def _find_edge(self, p: Pokemon) -> tuple:
        for e in self._graph.edges.data():
            if self._on_edge(p, e):
                return e[0], e[1]
        return None

    def attach(self):
        if self.client.is_running() != 'true':
            return
        d = json.loads(self.client.get_pokemons())
        tmp = [Pokemon(**p['Pokemon']) for p in d['Pokemons']]
        check = []
        self.pokemons = {}

        sor = sorted(self.get_agents(), key=lambda a: a.get_speed())

        ind_ag = [i.get_id() for i in sor]
        for ag in ind_ag:
            min_dis = math.inf
            min_path = []
            key = None
            for p in sorted(tmp, key=lambda p: p.get_value(), reverse=True):
                edge = self._find_edge(p)
                check.append(edge)
                if edge not in self.pokemons.keys():
                    self.pokemons[edge] = Edge_Pok(edge)
                if p.get_pos() not in self.pokemons[edge].get_pokemons():
                    self.pokemons[edge].get_pokemons().append(p.get_pos())
                    self.pokemons[edge].add_value(p.get_value())
                if not self.pokemons[edge].get_toAgent():
                    x = self.dict_path[ag][0]
                    dis = nx.shortest_path_length(self._graph, x,
                                                  edge[0], weight='weight')
                    pa = nx.shortest_path(self._graph, x,
                                          edge[0], weight='weight')
                    pa.append(edge[1])
                    dis += self._graph.edges[edge[0], edge[1]]['weight']
                    sp = (dis * sor[ag].get_speed()) / self.pokemons[edge].get_value()
                    # if set(pa[-2:-1]).issubset(self.dict_path[ag]):
                    #     continue

                    if sp < min_dis:
                        min_dis = sp
                        min_path = pa
                        key = edge
            if min_dis != math.inf:
                self.dict_path[ag] = min_path
                self.pokemons[key].set_toAgent(True)

    def get_pokemons(self):
        if self.client.is_running() != 'true':
            return
        d = json.loads(self.client.get_pokemons())
        return [Pokemon(**p['Pokemon']) for p in d['Pokemons']]

    def get_agents(self) -> List[Agent]:
        if self.client.is_running() != 'true':
            return
        d = json.loads(self.client.get_agents())
        return [Agent(**a['Agent']) for a in d['Agents']]

    def moving(self, t):
        if self.client.is_running() != 'true':
            return
        agents = self.get_agents()
        poks = []
        for p in self.pokemons.values():
            if len(p.get_pokemons()) > 0:
                poks += p.get_pokemons()
        flag = False
        flag2 = False
        for a in agents:
            for pos in poks:
                if dist(a.get_pos(), pos) < 1e-09:
                    flag2 = True
            if a.get_dest() == -1:
                next_node = self._get_next(a)
                self.client.choose_next_edge(
                    '{"agent_id":' + str(a.get_id()) + ', "next_node_id":' + str(next_node) + '}')
                flag = True
        d = json.loads(self.client.get_info())
        k = d['GameServer']['moves']
        if k < t * 10 and (not flag or flag2):
            k += 1
            self.client.move()
        return k

    def get_score(self):
        d = json.loads(self.client.get_info())
        return d['GameServer']['grade']

    def get_moves(self):
        d = json.loads(self.client.get_info())
        return d['GameServer']['moves']

    def get_time_to_end(self):
        x = round(int(self.client.time_to_end()) / 1000, ndigits=2)
        return str(x)

    def stop_game(self):
        self.client.stop()
        exit(0)

    def set_start(self) -> None:
        self.client.start()

    def is_run(self) -> bool:
        return self.client.is_running() == 'true'
