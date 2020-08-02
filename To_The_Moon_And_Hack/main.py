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
        self.font = pygame.freetype.Font("Merriweather_light.ttf", 24)
        self.values = [100, 100, 37]
        self.events = []

    def fps_to_sec(fps):
        return (1000 / fps) / 1000

    def update(self):
        self.update_vals()
        self.screen.fill(LBlue)
        pygame.draw.rect(
            self.screen, self.what_color(), (0, 0, self.x, self.y), 15)
        self.render()

    def update_vals(self, val=None, amt=1):
        self.is_dead()
        if val is None:
            self.values[0] -= amt if random.randint(0, 10) > 9 else 0
            if self.values[1] > 0:
                self.values[1] -= amt if random.randint(0, 10) > 8 else 0
            else:
                self.values[2] -= 0.5
        else:
            if val == "O":
                self.values[0] -= amt if random.randint(0, 10) > 9 else 0
            elif val == "B":
                if self.values[1] >= 2:
                    self.values[1] -= amt if random.randint(0, 10) > 8 else 0
            elif val == "T":
                self.values[2] -= amt

    def is_dead(self):
        oxy = self.values[0]
        temp = self.values[2]

        if oxy <= 0:
            self.death("Suffocation")
        elif temp <= 0 or temp >= 50:
            self.death("Temperature")

    def death(self, cause):
        self.screen.fill((0, 0, 0))
        self.font.render_to(
            self.screen, (50, self.y / 2),
            f"Death by {cause}", Red, size=50)

        pygame.display.flip()
        sleep(2)
        exit()

    def what_color(self, val=None):
        if val is None:
            value1 = self.values[0]
            value2 = self.values[1]
            val = value1 if value1 < value2 else value2

        if val >= 75:
            return DBlue
        elif val >= 51:
            return Green
        elif val >= 26:
            return Yellow
        else:
            return Red

    def render(self):
        pygame.draw.rect(self.screen, White, (0, 0, 405, 80))
        self.font.render_to(
            self.screen, (5, 5), "Press r for a random event!", Black, size=30)
        self.font.render_to(
            self.screen, (5, 45), "Press d to delete it!", Black, size=30)

        x, y = 40, 120

        for part in zip(self.values, ["Oxygen", "Battery", "Temperature"]):
            val, stat = int(part[0]), part[1]
            txt = f"{str(val)}%"
            txt = txt[:-1] + "ºC" if stat.startswith("T") else txt
            # Text
            self.font.render_to(
                self.screen, (x, y), stat, Black, size=30)
            self.font.render_to(
                self.screen, (x + 310, y + 45), txt, Black, size=30)
            # Squares
            pygame.draw.rect(
                self.screen, White, (x - 10, y + 35, 310, 50))
            pygame.draw.rect(
                self.screen, self.what_color(val), (x - 5, y + 40, val * 3, 40))
            pygame.draw.rect(
                self.screen, self.what_color(val), (x - 25, y - 15, 410, 115), 8)

            y += 140

        y = 60
        for problem in self.events:
            for part in problem:
                self.font.render_to(
                    self.screen, (x + 450, y), part, Red, size=30)
                y += 40
            y += 10

            if problem[0].find("Oxygen") != -1:
                self.update_vals("O", 2)
            elif problem[0].find("Battery") != -1:
                self.update_vals("B", 2)
            elif problem[0].find("Temperature") != -1:
                self.update_vals("T", 0.5)

    def random_event(self):
        possible_events = [
            ["\n Oxygen", "tank failure"], ["\n Comms", "down"],
            ["\n Microphone", "not working"],
            ["\n Temperature", "systems failing"], ["\n Battery", "failure"]]

        if len(self.events) == len(possible_events):
            return None

        while True:
            event = random.choice(possible_events)

            if self.events.count(event) >= 1:
                continue
            else:
                self.events.append(event)
                break

    def del_random_event(self):
        self.events.pop()


if __name__ == "__main__":
    Black, White = (0, 0, 0), (255, 255, 255)
    Red, Green, Yellow, = (255, 0, 0), (0, 255, 0), (255, 94, 1)
    LBlue, DBlue = (44, 176, 235), (0, 92, 141)

    pygame.init()
    screen = Board(770, 525)
    time_to_sleep = Board.fps_to_sec(24)

    while True:
        screen.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    print("letter R pressed")
                    screen.random_event()
                elif event.key == pygame.K_d:
                    print("Letter D pressed")
                    screen.del_random_event()
                elif event.key == pygame.K_q:
                    print("Letter Q pressed")
                    exit()
            elif event.type == pygame.QUIT:
                print("Exit window")
                exit()

        pygame.display.flip()
        sleep(time_to_sleep)
