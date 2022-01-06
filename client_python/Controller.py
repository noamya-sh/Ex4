import json
import math
import random
from typing import List
from Edge_Pok import *
from Agent import *
from Pokemon import *
from client import *
import networkx as nx
import numpy as np

PORT = 6666
HOST = '127.0.0.1'


class Controller:
    def __init__(self):
        self.client = Client()
        self.client.start_connection(HOST, PORT)
        self._graph = self.init_graph(self.client.get_graph())
        d = json.loads(self.client.get_pokemons())
        self.pokemons = {}
        tmp = [Pokemon(**p['Pokemon']) for p in d['Pokemons']]
        for p in tmp:
            edge = self.find_edge(p)
            self.pokemons[edge] = Edge_Pok(p.get_pos())  # p.value
            # else:
            #     self.pokemons[edge] += p.value

        self.dict_path = {}
        d = json.loads(self.client.get_info())
        k = d['GameServer']['agents']

        # to check
        cmp = []
        i = 0
        it = iter(self.pokemons.keys())
        while i < k and i < len(self.pokemons):
            ed = next(it)
            cmp.append(ed[0])
            self.client.add_agent("{\"id\":" + str(ed[0]) + "}")
            # self.dict_path[src] = [src]
            i += 1
        while i < k:
            x = random.randint(0, self._graph.number_of_nodes() - 1)
            if x not in cmp:
                self.client.add_agent("{\"id\":" + str(x) + "}")
                # self.dict_path[x] = [x]
                cmp.append(x)
                i += 1

        d = json.loads(self.client.get_agents())
        self.agents = {a['Agent']['id']: Agent(**a['Agent']) for a in d['Agents']}
        for k, v in self.agents.items():
            self.dict_path[k] = [v.src]

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

    def get_graph(self):
        return self._graph

    def get_next(self, ag: Agent) -> int:
        if not self.dict_path[ag.id]:
            return None
        if ag.src == self.dict_path[ag.id][0] and len(self.dict_path[ag.id]) > 1:
            self.dict_path[ag.id].pop(0)
        return self.dict_path[ag.id][0]

    def _on_edge(self, p: Pokemon, edge) -> bool:
        node_1 = self._graph.nodes[edge[0]]
        node_2 = self._graph.nodes[edge[1]]
        edge_type = 1 if edge[0] < edge[1] else -1
        if p.get_type() != edge_type:
            return False
        pos_1 = node_1['pos']
        pos_2 = node_2['pos']
        pos3 = p.get_pos()
        p1 = np.array([pos_1[0], pos_1[1]])
        p2 = np.array([pos_2[0], pos_2[1]])
        p3 = np.array([pos3[0], pos3[1]])
        d = np.linalg.norm(np.cross(p2 - p1, p1 - p3)) / np.linalg.norm(p2 - p1)
        return math.isclose(0, d, abs_tol=1e-09)

    def find_edge(self, p: Pokemon) -> tuple:
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

        sor = sorted(self.get_agents(), key=lambda a: a._value, reverse=True)
        kk = [i.id for i in sor]
        for ag in kk:
            min_dis = math.inf
            min_path = []
            key = None
            for p in sorted(tmp, key=lambda p: p.get_value(), reverse=True):
                edge = self.find_edge(p)
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
                    sp = (dis * sor[ag].speed) / self.pokemons[edge].get_value()
                    # if set(pa[-2:-1]).issubset(self.dict_path[ag]):
                    #     continue

                    if sp < min_dis:
                        min_dis = sp
                        min_path = pa
                        key = edge
            if min_dis != math.inf:
                self.dict_path[ag] = min_path
                self.pokemons[key].set_toAgent(True)
        list = [k for k in self.pokemons.keys()]
        for k in list:
            if k not in check:
                del self.pokemons[k]

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
        flag = False
        for a in agents:
            # print(a.id, self.dict_path[a.id])
            if a.dest == -1:
                next_node = self.get_next(a)
                self.client.choose_next_edge(
                    '{"agent_id":' + str(a.id) + ', "next_node_id":' + str(next_node) + '}')
                flag = True
        d = json.loads(self.client.get_info())
        k = d['GameServer']['moves']
        if k < t * 100 and not flag:
            # print(k)
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
        x = int(self.client.time_to_end())
        return str(x/1000)


if __name__ == '__main__':
    # PORT = 6666
    # # server host (default localhost 127.0.0.1)
    # HOST = '127.0.0.1'
    # client = Client()
    # client.start_connection(HOST, PORT)
    # graph_json = client.get_graph()
    d = Controller()
    graph = d.get_graph()
    min_x = min(list(graph.nodes(data=True)), key=lambda n: n[1]['pos'][0])[1]['pos'][0]
    min_y = min(list(graph.nodes(data=True)), key=lambda n: n[1]['pos'][1])[1]['pos'][1]
    max_x = max(list(graph.nodes(data=True)), key=lambda n: n[1]['pos'][0])[1]['pos'][0]
    max_y = max(list(graph.nodes(data=True)), key=lambda n: n[1]['pos'][1])[1]['pos'][1]
    print(min_y)
    # data = json.loads(client.get_pokemons())
    # print(data)
    # pokemons = [Pokemon(**p['Pokemon']) for p in data['Pokemons']]
    # for p in pokemons:
    #     print(d.find_edge(p))
