import random
from graphics import Point, Window
import time


class Maze:
    def __init__(
        self,
        x1,
        y1,
        win: Window = None,
    ) -> None:
        self._x1 = x1
        self._y1 = y1
        self._win = win
        self._baloons = []
        self._arrows = []
