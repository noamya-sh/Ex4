import math

import numpy as np
from pygame import gfxdraw, display, RESIZABLE, Color
import pygame as pg
from Controller import Controller
import time
import networkx as nx

WIDTH, HEIGHT = 1080, 720
radius = 15


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


class gui:
    def __init__(self):
        control = Controller()
        graph = control.get_graph()
        pg.init()
        self.screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
        clock = pg.time.Clock()
        pg.font.init()
        FONT = pg.font.SysFont('Arial', 20, bold=True)
        self.min_x = min(list(graph.nodes(data=True)), key=lambda n: n[1]['pos'][0])[1]['pos'][0]
        self.min_y = min(list(graph.nodes(data=True)), key=lambda n: n[1]['pos'][1])[1]['pos'][1]
        self.max_x = max(list(graph.nodes(data=True)), key=lambda n: n[1]['pos'][0])[1]['pos'][0]
        self.max_y = max(list(graph.nodes(data=True)), key=lambda n: n[1]['pos'][1])[1]['pos'][1]
        pokball = pg.image.load("pik.png")
        pik = pg.image.load("Poke_Ball.png")
        pokball2 = pg.image.load('im.png')
        picture = pg.image.load('forest.jpg')
        control.client.start()
        t = time.time()
        while control.client.is_running() == 'true':
            agents = control.get_agents()
            pokemons = control.get_pokemons()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit(0)

            picture = pg.transform.scale(picture, self.screen.get_size())
            rect = picture.get_rect()
            self.screen.blit(picture, rect)
            # self.screen.fill(Color(0, 0, 0))

            for e in graph.edges(data=True):
                # find the edge nodes
                src = next(n for n in graph.nodes(data=True) if n[0] == e[0])
                dest = next(n for n in graph.nodes(data=True) if n[0] == e[1])

                # scaled positions
                src_x = self.my_scale(src[1]['pos'][0], x=True)
                src_y = self.my_scale(src[1]['pos'][1], y=True)
                dest_x = self.my_scale(dest[1]['pos'][0], x=True)
                dest_y = self.my_scale(dest[1]['pos'][1], y=True)

                # draw the line
                p = np.subtract((dest_x, dest_y), segment((src_x, src_y), (dest_x, dest_y)))
                line(self.screen, Color(61, 72, 126), (src_x, src_y), p)
            for e in graph.edges(data=True):
                # find the edge nodes
                src = next(n for n in graph.nodes(data=True) if n[0] == e[0])
                dest = next(n for n in graph.nodes(data=True) if n[0] == e[1])

                # scaled positions
                src_x = self.my_scale(src[1]['pos'][0], x=True)
                src_y = self.my_scale(src[1]['pos'][1], y=True)
                dest_x = self.my_scale(dest[1]['pos'][0], x=True)
                dest_y = self.my_scale(dest[1]['pos'][1], y=True)

                # draw the line
                p = np.subtract((dest_x, dest_y), segment((src_x, src_y), (dest_x, dest_y)))
                arrow(self.screen, Color(0, 0, 0), (src_x, src_y), p, 10)
            for n in graph.nodes(data=True):
                x = self.my_scale(n[1]['pos'][0], x=True)
                y = self.my_scale(n[1]['pos'][1], y=True)
                gfxdraw.filled_circle(self.screen, int(x), int(y),
                                      radius, Color(64, 80, 174))
                gfxdraw.aacircle(self.screen, int(x), int(y),
                                 radius, Color(255, 255, 255))

                # draw the node id
                id_srf = FONT.render(str(n[0]), True, Color(255, 255, 255))
                rect = id_srf.get_rect(center=(x, y))
                self.screen.blit(id_srf, rect)
            for p in pokemons:
                if p.get_type() == 1:
                    pokball.convert()
                    pokball = pg.transform.scale(pokball, (50, 50))
                    r = pokball.get_rect()
                    r.center = (int(self.my_scale(p._pos[0], x=True)), int(self.my_scale(p._pos[1], y=True)))
                    self.screen.blit(pokball, r)
                else:
                    pokball2.convert()
                    pokball2 = pg.transform.scale(pokball2, (50, 50))
                    r = pokball2.get_rect()
                    r.center = (int(self.my_scale(p._pos[0], x=True)), int(self.my_scale(p._pos[1], y=True)))
                    self.screen.blit(pokball2, r)
            for agent in agents:
                pik.convert()
                pik = pg.transform.scale(pik, (40, 40))
                r = pik.get_rect()
                r.center = (int(self.my_scale(agent._pos[0], x=True)), int(self.my_scale(agent._pos[1], y=True)))
                self.screen.blit(pik, r)

            # for agent in agents:
            #     if agent.dest == -1:
            #         next_node = (agent.src + 1) % graph.number_of_nodes()
            #         control.client.choose_next_edge(
            #             '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
            #         ttl = control.client.time_to_end()
            #         print(ttl, control.client.get_info())

            # control.client.move()
            # control.attach()

            f = FONT.render("Score: " + str(control.get_score()), True, Color(0, 0, 0))
            self.screen.blit(f, (self.screen.get_width() - 100, self.screen.get_height() - 100))
            display.update()

            # refresh rate
            clock.tick(600)
            control.attach()
            now = time.time()
            control.moving(now - t)

    # decorate scale with the correct values

    def my_scale(self, data, x=False, y=False):
        if x:
            return scale(data, 50, self.screen.get_width() - 50, self.min_x, self.max_x)
        if y:
            return scale(data, 50, self.screen.get_height() - 50, self.min_y, self.max_y)


def normalize(v: tuple) -> tuple:
    """v/||v||"""
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def segment(start: tuple, end: tuple) -> tuple:
    """calculate segment line , use normalization"""
    v = np.subtract(end, start)
    b = tuple(normalize(v) * 20)
    return b


def line(screen, color, start, end, thickness=4) -> None:
    """
    to draw line (in accordance with the arrow triangle)
    """
    pg.draw.line(screen, color, start, np.subtract(end, tuple(normalize(np.subtract(end, start)) * 5)), thickness)


def arrow(screen, color, start, end, trirad) -> None:
    """
    :param screen: surface that draw about it
    :param color: color of triangle
    :param start: src vertical of line
    :param end: dest vertical of line
    :param trirad: size of triangle
    """
    rad = math.pi / 180
    rotation = (math.atan2(start[1] - end[1], end[0] - start[0])) + math.pi / 2
    pg.draw.polygon(screen, color, ((end[0] + trirad * math.sin(rotation),
                                     end[1] + trirad * math.cos(rotation)),
                                    (end[0] + trirad * math.sin(rotation - 120 * rad),
                                     end[1] + trirad * math.cos(rotation - 120 * rad)),
                                    (end[0] + trirad * math.sin(rotation + 120 * rad),
                                     end[1] + trirad * math.cos(rotation + 120 * rad))))


if __name__ == '__main__':
    gui()
