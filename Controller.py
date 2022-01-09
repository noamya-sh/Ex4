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

# for connection to server
PORT = 6666
HOST = '127.0.0.1'


def dist(p1: tuple, p2: tuple):
    """
    :param p1: point 1
    :param p2: point 2
    :return: distance betweent point1 to point2
    """
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def init_graph(json_str) -> nx.DiGraph:
    """
    :param json_str: string in the form of json.
    :return: Digraph (directed weighted graph of networkx)
    """
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
    """
    The controller receives and sends information to the server according to the game data.
    """
    def __init__(self) -> None:
        self.client = Client()
        self.client.start_connection(HOST, PORT)
        self._graph = init_graph(self.client.get_graph())
        self.pokemons = {}
        d = json.loads(self.client.get_pokemons())
        tmp = [Pokemon(**p['Pokemon']) for p in d['Pokemons']]
        # insert each pokemons to his edge
        for p in tmp:
            edge = self._find_edge(p)
            if edge not in self.pokemons.keys():
                self.pokemons[edge] = Edge_Pok(edge)
            if p.get_pos() not in self.pokemons[edge].get_pokemons():
                self.pokemons[edge].get_pokemons().append(p.get_pos())
                self.pokemons[edge].add_value(p.get_value())

        self.dict_path = {}
        d = json.loads(self.client.get_info())
        k = d['GameServer']['agents']
        self.pokemons = dict(sorted(self.pokemons.items(), key=lambda t: t[1].get_value()))
        tmp = []
        i = 0
        it = iter(self.pokemons.keys())
        while i < k and i < len(self.pokemons):
            ed = next(it)
            tmp.append(ed[0])
            self.client.add_agent("{\"id\":" + str(ed[0]) + "}")
            i += 1
        while i < k:
            x = random.randint(0, self._graph.number_of_nodes() - 1)
            if x not in tmp:
                self.client.add_agent("{\"id\":" + str(x) + "}")
                tmp.append(x)
                i += 1

        d = json.loads(self.client.get_agents())
        self.agents = {a['Agent']['id']: Agent(**a['Agent']) for a in d['Agents']}
        for k, v in self.agents.items():
            self.dict_path[k] = [v.get_src()]

    def get_graph(self) -> nx.DiGraph:
        return self._graph

    def _get_next(self, ag: Agent) -> int:
        """
        :param ag: agent for get him path
        :return: next node to go
        """
        if not self.dict_path[ag.get_id()]:
            return None
        if ag.get_src() == self.dict_path[ag.get_id()][0] and len(self.dict_path[ag.get_id()]) > 1:
            self.dict_path[ag.get_id()].pop(0)
        return self.dict_path[ag.get_id()][0]

    def _on_edge(self, p: Pokemon, edge) -> bool:
        """
        :param p: Pokemon to check
        :param edge: edge from this graph
        :return: true if the pokemon on this edge
        """
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

    def attach(self) -> None:
        """
        The function is assigned to each Pokemon path agent.
        Pokemon selection is made based on proximity to the agent,
        the Pokemon value and whether it has already been assigned to another agent.
        The function selects a new path for each agent in order to
        take advantage of the changes made during the game.
        """
        try:
            d = json.loads(self.client.get_pokemons())
            tmp = [Pokemon(**p['Pokemon']) for p in d['Pokemons']]
            check = []
            self.pokemons = {}
            # sort the agents by their speed
            agents = sorted(self.get_agents(), key=lambda a: a.get_speed())
            ind_ag = [a.get_id() for a in agents]
            for ag in ind_ag:
                min_dis = math.inf
                min_path = []
                edge_selected = None
                # first get the greather pokemons
                for p in sorted(tmp, key=lambda p: p.get_value(), reverse=True):
                    edge = self._find_edge(p)
                    check.append(edge)
                    if edge not in self.pokemons.keys():
                        self.pokemons[edge] = Edge_Pok(edge)
                    if p.get_pos() not in self.pokemons[edge].get_pokemons():
                        self.pokemons[edge].get_pokemons().append(p.get_pos())
                        self.pokemons[edge].add_value(p.get_value())
                    if not self.pokemons[edge].get_is_attached():  # if the edge of pokemon not attach to agent
                        x = self.dict_path[ag][0]
                        # calculate shortest path to reach this edge
                        dis = nx.shortest_path_length(self._graph, x,
                                                      edge[0], weight='weight')
                        pa = nx.shortest_path(self._graph, x,
                                              edge[0], weight='weight')
                        pa.append(edge[1])
                        dis += self._graph.edges[edge[0], edge[1]]['weight']

                        sp = (dis / agents[ag].get_speed()) / self.pokemons[edge].get_value()

                        if sp < min_dis:
                            min_dis = sp
                            min_path = pa
                            edge_selected = edge
                if min_dis != math.inf:
                    self.dict_path[ag] = min_path
                    self.pokemons[edge_selected].set_is_attached(True)
        except:  # if the server colse
            exit(0)

    def get_pokemons(self) -> List[Pokemon]:
        """
        :return: list with pokemons details from server.
        """
        try:
            d = json.loads(self.client.get_pokemons())
            return [Pokemon(**p['Pokemon']) for p in d['Pokemons']]
        except:  # if the server colse
            exit(0)

    def get_agents(self) -> List[Agent]:
        """
        :return: list with agents details from server.
        """
        try:
            d = json.loads(self.client.get_agents())
            return [Agent(**a['Agent']) for a in d['Agents']]
        except:  # if the server colse
            exit(0)

    def moving(self, t) -> None:
        """
        :param t: Time elapsed since the start of the game.
        The function commands the agents to move to the next node in their path,
        and performs a move when the agent is close to Pokemon,
         provided no more than 10 moves are made per second.
        """
        try:
            agents = self.get_agents()
            poks = []
            for p in self.pokemons.values():
                if len(p.get_pokemons()) > 0:
                    poks += p.get_pokemons()
            next_node = False
            close_to_pok = False
            for a in agents:
                for pos in poks:
                    if dist(a.get_pos(), pos) < 0.001:
                        close_to_pok = True
                if a.get_dest() == -1:
                    next_node = self._get_next(a)
                    self.client.choose_next_edge(
                        '{"agent_id":' + str(a.get_id()) + ', "next_node_id":' + str(next_node) + '}')
                    next_node = True

            moves = self.get_moves()
            if moves < t * 10 and (not next_node or close_to_pok):
                self.client.move()
        except:  # if the server colse
            exit(0)

    def get_grade(self) -> int:
        """
        :return: sum grade up to now (all value of pokemons collected).
        """
        try:
            d = json.loads(self.client.get_info())
            return d['GameServer']['grade']
        except:  # if the server colse
            exit(0)

    def get_moves(self) -> int:
        """
        :return: sum 'move' calls up to now.
        """
        try:
            d = json.loads(self.client.get_info())
            return d['GameServer']['moves']
        except:  # if the server colse
            exit(0)

    def get_time_to_end(self) -> str:
        """
        :return: sum time left to end game.
        """
        try:
            x = round(int(self.client.time_to_end()) / 1000, ndigits=2)
            return str(x)
        except:  # if the server colse
            exit(0)

    def stop_game(self):
        """
        stop game command.
        """
        self.client.stop()
        self.client.stop_connection()
        exit(0)

    def set_start(self) -> None:
        """
        strat game command.
        """
        self.client.start()

    def is_run(self) -> bool:
        """
        :return: True if the server run
        """
        return self.client.is_running() == 'true'
