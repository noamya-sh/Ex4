from pygame import Rect, Surface, Color, font
import pygame as pg

font.init()
arial_font = font.SysFont('Century', 24, bold=False)


class Button:
    """
    simple button, base for everything
    """

    def __init__(self, title: str, size: tuple[int, int], color) -> None:
        self.title = title
        self.size = size
        self.color = color
        self.rect = Rect((0, 0), size)
        self.on_click = []
        self.show = True
        self.disabled = False

    def add_click_listener(self, func) -> None:
        self.on_click.append(func)

    def render(self, surface: Surface, pos) -> None:
        if not self.show:
            return
        self.rect.topleft = pos

        title_srf = arial_font.render(self.title, True, Color(255, 255, 255))
        title_rect = title_srf.get_rect(center=self.rect.center)
        pg.draw.rect(surface, self.color, self.rect)
        pg.draw.rect(surface, Color(255, 255, 255), self.rect, width=1)
        surface.blit(title_srf, title_rect)

    def check(self) -> None:
        if self.on_click != [] and not self.disabled:
            mouse_pos = pg.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                clicked, _, _ = pg.mouse.get_pressed()
                if clicked:
                    for func in self.on_click:
                        func()
