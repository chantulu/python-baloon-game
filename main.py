from graphics import Window, Line, Point
from maze import Maze


def main():
    margin = 20
    screen_x = 800
    screen_y = 600
    win = Window(screen_x, screen_y)

    maze = Maze(margin, margin, win)

    win.wait_for_close()


main()
