import pygame
from time import sleep
import random

class Board:
    def __init__(self, x=1280, y=720):
        pygame.display.set_caption("PLACEHOLDER")
        self.screen = pygame.display.set_mode((x, y))
        self.screen.fill(Blue)
        self.font = pygame.freetype.Font("Merriweather.ttf", 24)
        self.events = []
        self.levels = [100, 100, 37]

    def fps_to_sec(fps):
        return (1000 / fps) / 1000
    
    def update(self, levels):
        levels[0] -= random.randint(1, 3) # Oxygen
        levels[1] -= random.randint(1, 2) # battery
        Board.render(levels)
    

    def render(levels):
        pygame.


    def random_event():
        possible_events = ["atmosphere pressure drop", "comms down"]
        return random.choice(possible_events)


if __name__ == "__main__":
    Black = (0, 0, 0)
    White = (255, 255, 255)
    Red = (255, 0, 0)
    Yellow = (0, 255, 255)
    Green = (0, 255, 0)
    Blue = (0, 0, 255)

    pygame.init()
    screen = Board()
    
    time_to_sleep = Board.fps_to_sec(24)

    while True:
        Board.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    print("r")
                    screen.events.append(Board.random_event())

                elif event.key == pygame.K_q:
                    print("q_exit")
                    exit()

            if event.type == pygame.QUIT:
                    print("x_exit")
                    exit()

        pygame.display.flip()
        sleep(time_to_sleep)