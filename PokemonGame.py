import math
import numpy as np
from pygame import gfxdraw, display, RESIZABLE, Color, MOUSEBUTTONDOWN
import pygame as pg
from Controller import Controller
from Button import Button
import time

WIDTH, HEIGHT = 1080, 720
radius = 15


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


class PokemonGame:
    """
    This class is GUI implemention for Pokemon game using the pygame and Numpy library.
    The class get information from Controller and draw on the screen.
    """
    def __init__(self):
        control = Controller()
        graph = control.get_graph()
        pg.init()
        self.screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
        clock = pg.time.Clock()
        pg.font.init()
        FONT = pg.font.SysFont('Century', 20, bold=False)
        FONT2 = pg.font.SysFont('Bahnschrift SemiBold', 26, bold=True)
        self.min_x = min(list(graph.nodes(data=True)), key=lambda n: n[1]['pos'][0])[1]['pos'][0]
        self.min_y = min(list(graph.nodes(data=True)), key=lambda n: n[1]['pos'][1])[1]['pos'][1]
        self.max_x = max(list(graph.nodes(data=True)), key=lambda n: n[1]['pos'][0])[1]['pos'][0]
        self.max_y = max(list(graph.nodes(data=True)), key=lambda n: n[1]['pos'][1])[1]['pos'][1]
        but = Button("Stop", (80, 80), Color(14, 112, 112))
        but.add_click_listener(control.stop_game)
        pok1 = pg.image.load(".\\img\\pik.png")
        pok1.convert()
        pok1 = pg.transform.scale(pok1, (50, 50))
        pokball = pg.image.load(".\\img\\Poke_Ball.png")
        pokball.convert()
        pokball = pg.transform.scale(pokball, (40, 40))
        pok2 = pg.image.load('.\\img\\im.png')
        pok2.convert()
        pok2 = pg.transform.scale(pok2, (50, 50))
        bg = pg.image.load('.\\img\\forest.jpg')
        control.set_start()
        start = time.time()
        # draw as long as there is a connection to the server
        while control.is_run():
            agents = control.get_agents()
            pokemons = control.get_pokemons()

            # check event
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit(0)
                elif event.type == MOUSEBUTTONDOWN:
                    but.check()
            # draw background
            bg = pg.transform.scale(bg, self.screen.get_size())
            rect = bg.get_rect()
            self.screen.blit(bg, rect)

            for e in graph.edges(data=True):
                # find the edge nodes
                src = next(n for n in graph.nodes(data=True) if n[0] == e[0])
                dest = next(n for n in graph.nodes(data=True) if n[0] == e[1])

                # scaled positions
                src_x, src_y, dest_x, dest_y = self._get_x_y(src, dest)
                # draw the line
                p = np.subtract((dest_x, dest_y), segment((src_x, src_y), (dest_x, dest_y)))
                line(self.screen, Color(201, 156, 8), (src_x, src_y), p)
            for e in graph.edges(data=True):
                # find the edge nodes
                src = next(n for n in graph.nodes(data=True) if n[0] == e[0])
                dest = next(n for n in graph.nodes(data=True) if n[0] == e[1])

                # scaled positions
                src_x, src_y, dest_x, dest_y = self._get_x_y(src, dest)
                # draw the arrow
                p = np.subtract((dest_x, dest_y), segment((src_x, src_y), (dest_x, dest_y)))
                arrow(self.screen, Color(70, 31, 5), (src_x, src_y), p, 10)

            for n in graph.nodes(data=True):
                x = self._my_scale(n[1]['pos'][0], x=True)
                y = self._my_scale(n[1]['pos'][1], y=True)
                gfxdraw.filled_circle(self.screen, int(x), int(y),
                                      radius, Color(2, 158, 106))
                gfxdraw.aacircle(self.screen, int(x), int(y),
                                 radius, Color(255, 255, 255))

                # draw the node id
                id_srf = FONT2.render(str(n[0]), True, Color(0, 0, 0))
                rect = id_srf.get_rect(center=(x, y))
                self.screen.blit(id_srf, rect)

            # draw pokemons by their type
            for p in pokemons:
                if p.get_type() == -1:
                    r = pok1.get_rect()
                    r.center = (int(self._my_scale(p.get_pos()[0], x=True)), int(
                        self._my_scale(p.get_pos()[1], y=True)))
                    self.screen.blit(pok1, r)
                else:
                    r = pok2.get_rect()
                    r.center = (int(self._my_scale(p.get_pos()[0], x=True)), int(
                        self._my_scale(p.get_pos()[1], y=True)))
                    self.screen.blit(pok2, r)
            # draw agents
            for agent in agents:
                r = pokball.get_rect()
                r.center = (int(self._my_scale(agent.get_pos()[0], x=True)), int(
                    self._my_scale(agent.get_pos()[1], y=True)))
                self.screen.blit(pokball, r)

            h = self.screen.get_height()
            w = self.screen.get_width()

            # draw details of moves, time and grade
            pg.draw.rect(self.screen, Color(200, 192, 7), pg.Rect(w - 280, h - 80, 200, 80))
            pg.draw.rect(self.screen, Color(255, 255, 255), pg.Rect(w - 280, h - 80, 200, 80), width=1)
            f = FONT.render("Grade: " + str(control.get_grade()), True, Color(0, 0, 0))
            self.screen.blit(f, (w - 265, h - 80))
            f = FONT.render("Moves: " + str(control.get_moves()), True, Color(0, 0, 0))
            self.screen.blit(f, (w - 265, h - 40))
            f = FONT.render("Time to end: " + control.get_time_to_end(), True, Color(0, 0, 0))
            self.screen.blit(f, (w - 265, h - 60))
            but.render(self.screen, (w - 80, h - 80))
            display.update()

            # refresh rate
            clock.tick(600)
            # update data of agents and pokemons.
            control.attach()
            now = time.time()
            control.moving(now - start)

    # decorate scale with the correct values
    def _my_scale(self, data, x=False, y=False):
        if x:
            return scale(data, 50, self.screen.get_width() - 50, self.min_x, self.max_x)
        if y:
            return scale(data, 50, self.screen.get_height() - 50, self.min_y, self.max_y)

    def _get_x_y(self, src: tuple, dest: tuple) -> tuple:
        """
        :param src: src point
        :param dest: dest point
        :return: x,y for each point
        """
        src_x = self._my_scale(src[1]['pos'][0], x=True)
        src_y = self._my_scale(src[1]['pos'][1], y=True)
        dest_x = self._my_scale(dest[1]['pos'][0], x=True)
        dest_y = self._my_scale(dest[1]['pos'][1], y=True)
        return src_x, src_y, dest_x, dest_y


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
    PokemonGame()