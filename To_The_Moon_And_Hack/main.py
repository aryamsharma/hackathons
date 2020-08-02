import pygame
from time import sleep
import random
import pygame.freetype

class Board:
    def __init__(self, x=1280, y=720):
        self.x = x
        self.y = y
        pygame.display.set_caption("Space Screen")
        self.screen = pygame.display.set_mode((x, y))
        self.screen.fill(DBlue)
        self.font = pygame.freetype.Font("Merriweather_light.ttf", 24)
        self.events = []
        self.levels = [100, 100, 37]

    def fps_to_sec(fps):
        return (1000 / fps) / 1000
    
    def update(self):
        oxy = self.levels[0]
        batt = self.levels[1]
        temp = self.levels[2]

        if oxy <= 0 or temp <= 20:
            self.death()

        if batt > 0:
            self.levels[1] -= 1 if random.randint(-5, 1) > 0 else 0 # Battery -5
        
        else:
            self.levels[2] -= random.choice([1.5, 1, 0.5, 0.2, 0])
            self.levels[2] = int(self.levels[2])
        
        self.levels[0] -= 1 if random.randint(-10, 1) > 0 else 0 # Oxygen -10

        self.screen.fill(self.color())
        self.render()

    def death(self):
        self.screen.fill((0, 0, 0))
        self.font.render_to(
            self.screen, (self.x / 2 - 100, self.y / 2 - 100),
            "DEAD", Red, size=50)
        pygame.display.flip()
        sleep(2)
        exit()
        

    def render(self):
        pygame.draw.rect(self.screen, LBlue, (10, 10, self.x - 20, self.y - 20))
        pygame.draw.rect(self.screen, White, (0, 0, 400, 35))
        self.font.render_to(
            self.screen, (5, 5),
            "Press r for a random event", Black, size=30)

        x, y = 25, 60

        for part in zip(self.levels, ["Oxygen", "Battery"]):
            self.font.render_to(
                self.screen, (x, y),
                part[1], Black, size=30)
            
            pygame.draw.rect(self.screen, DBlue, (15, y + 40, 310, 50))
            pygame.draw.rect(self.screen, White, (20, y + 45, part[0] * 3, 40))
            
            self.font.render_to(
                self.screen, (330, y + 50),
                str(part[0]) + "%", Black, size=30)
            
            y *= 3
        
        temp = self.levels[2]
        self.font.render_to(
            self.screen, (25, 300),
            "Temp", Black, size=30)
        
        pygame.draw.rect(self.screen, DBlue, (15, 340, 310, 50))
        pygame.draw.rect(self.screen, White, (20, 345, temp * 4, 40))
        
        self.font.render_to(
            self.screen, (330, 350),
            str(temp) + "ºC", Black, size=30)

    def color(self):
        level1 = self.levels[0]
        level2 = self.levels[1]
        lowest = level1 if level1 < level2 else level2

        if lowest >= 75:
            return DBlue
        
        elif lowest >= 51:
            return (0, 255, 0)
        
        elif lowest >= 26:
            return (255, 255, 0)
        
        elif lowest >= 0:
            return (255, 0, 0)


    def random_event():
        possible_events = ["atmosphere pressure drop", "comms down"]
        return random.choice(possible_events)


if __name__ == "__main__":
    Black = (0, 0, 0)
    White = (255, 255, 255)
    Red = (255, 0, 0)
    Yellow = (0, 255, 255)
    Green = (0, 255, 0)
    LBlue = (44, 176, 235)
    DBlue = (0, 92, 141)

    pygame.init()
    screen = Board(755, 490)
    
    time_to_sleep = Board.fps_to_sec(24)

    while True:
        screen.update()
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