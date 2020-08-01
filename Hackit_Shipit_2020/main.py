import random
import pygame
from time import sleep
import pygame.freetype
import math

class Board:
    def __init__(self, bg_color, background_name="ocean1.jpg"):
        pygame.display.set_caption("lily")
        self.screen = pygame.display.set_mode((1280, 720))
        self.background_image = pygame.image.load(background_name)
        # self.screen.fill(Ocean_Blue)
        self.font = pygame.freetype.Font("JetBrains.ttf", 24)
        pygame.display.flip()
        self.all_lilys = []
        self.all_birds = []
        self.to_delete = []

    def _draw_text(self, help_text):
        pygame.draw.rect(self.screen, White, (0, 0, 1280, 100))
        off_y = -25
        for text in help_text:
            off_y += 30
            self.font.render_to(self.screen,(5, off_y), text, Black)
    
    def _is_dead(self, obj):
        x, y = obj[0]
        if x <= 0 or y <= 0 or x >= 1280 or y >= 720:
            return True

        pix_val = self.screen.get_at([x, y])

        if pix_val != (0, 170, 255, 255):
            return True

    def update(self, help_text):
        fps_time = Board._fps_to_sec(24)

        while True:
            self.screen.blit(self.background_image, [0, 0])

            for obj in self.all_lilys:
                Board._draw_lily(self.screen, obj)

            Board._draw_text(self, help_text)

            for obj in self.all_birds:
                ret = Board._is_dead(self, obj)
                
                if ret == True:
                    self.to_delete.append(obj)
                    continue

                Board._draw_bird(self, self.screen, obj)
            
            for event in pygame.event.get():
                screen.events(event)

            pygame.display.flip()
            sleep(fps_time) # 1000 / fps = time between each frame (millisec)
            Board.reset(self)

    def reset(self):
        for obj in self.to_delete:
            self.all_birds.remove(obj)
        
        del self.to_delete[:]

    def _create_lily(pos):
        noise_range = 50
        return pos, noise_range
    
    def _create_bird(self):
        while True:
            pos = [random.randint(50, 1230), random.randint(50, 670)]
            direction = random.choice([
                [-1, 0], [0, 1], [1, 0], [0, -1], 
                [1, 1], [-1, -1], [1, -1], [-1, 1]])
            
            ret = Board._is_dead(self, (pos, direction))
            if ret:
                continue
            break
        return pos, direction
    
    def _del_obj(head):
        if len(head) >= 1:
            head.pop()
        else:
            print("nothing to remove")
    
    def _fps_to_sec(fps):
        return (1000 / fps) / 1000
    
    def _draw_lily(screen, obj):
        loc = obj[0]
        noise_range = obj[1]
        pygame.draw.circle(screen, D_Green, loc, 10, 0)
        pygame.draw.circle(screen, Red, loc, noise_range, 2)
    
    def _draw_bird(self, screen, obj):
        x, y = obj[0]
        x_diff, y_diff = obj[1]

        if len(self.all_lilys) >= 1:
            for lily in self.all_lilys:
                x2, y2 = lily[0]
                distance = math.sqrt((x - x2) ** 2 + (y - y2) ** 2)
                if distance < 60:
                    x_diff, y_diff = -x_diff, -y_diff
                    obj[1][0] = x_diff
                    obj[1][1] = y_diff

        x, y = x + x_diff, y + y_diff
        
        pygame.draw.circle(screen, Gray, (x, y), 10, 0)
        obj[0][0] = x
        obj[0][1] = y


    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:
                print("l")
                Board._del_obj(self.all_lilys)

            elif event.key == pygame.K_b:
                print("b")
                self.all_birds.append(Board._create_bird(self))

            elif event.key == pygame.K_k:
                print("k")
                Board._del_obj(self.all_birds)

            elif event.key in [pygame.K_q, pygame.K_ESCAPE]:
                print("q or esc")
                exit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("mouse down")
            pos = pygame.mouse.get_pos()
            self.all_lilys.append(Board._create_lily(pos))
        
        elif event.type == pygame.QUIT:
            print("x")
            exit()

if __name__ == "__main__":
    Black = (0, 0, 0)
    Gray = (100, 100, 100)
    White = (255, 255, 255)
    Red = (255, 0, 0)
    Green = (0, 255, 0)
    D_Green = (0, 155, 0)
    Blue = (0, 0, 255)
    Ocean_Blue = (0, 105, 148)

    pygame.init()
    help_text = [
        "use your mouse left click to spawn B.P.M, l to delete the most recent B.P.M!",
        "b to spawn a bird, k to delete the most recent bird!",
        "Q to quit or press the x on the top left!"]

    screen = Board(Ocean_Blue, "ocean1.jpg")

    screen.update(help_text)