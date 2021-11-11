import math
import random
from time import sleep
import pygame
import pygame.freetype


class Map:
    def __init__(self):
        pygame.display.set_caption("Drone simulator")
        self.screen = pygame.display.set_mode((1280, 720))
        self.screen.fill(Ocean_Blue)
        self.all_drones = []
        self.all_buoys = []
        self.font = pygame.freetype.Font("JetBrains.ttf", 24)
    
    def what_quad(self, loc):
        x, y = loc[0], loc[1]
        if (x > 0 and y > 0): 
            return [-1, -1]
    
        elif (x < 0 and y > 0): 
            return [1, -1]
            
        elif (x < 0 and y < 0): 
            return [1, 1]
        
        elif (x > 0 and y < 0): 
            return [-1, 1]
            
        elif (x == 0 and y > 0): 
            return [0, -1]
        
        elif (x == 0 and y < 0): 
            return [0, 1]
        
        elif (y == 0 and x < 0): 
            return [1, 0]
        
        elif (y == 0 and x > 0): 
            return [-1, 0]
        
        else:
            return True
  
    def draw_drone(self, drone_cfg):
        battery_text = f"Battery level {drone_cfg[0]}%"
        name = "Drone"
        loc = drone_cfg[-1]
        pygame.draw.circle(self.screen, Black, loc, 5, 0)
        pygame.draw.circle(self.screen, Red, loc, drone_cfg[-2], 1)
        pygame.draw.rect(self.screen, White, (loc[0], loc[1], 250, 50))
        self.font.render_to(
            self.screen,(loc[0] + 1, loc[1] + 5), battery_text, Black)

        self.font.render_to(
            self.screen, (loc[0] + 1, loc[1] + 30), name, Black)

    def draw_buoy(self, buoy_cfg):
        recharge_rate = buoy_cfg[0]
        recharge_rate_text = f"Recharge {recharge_rate}u/s"
        name = "buoy"
        loc = buoy_cfg[-1]
        pygame.draw.circle(self.screen, Green, loc, 25, 0)
        
        pygame.draw.rect(
            self.screen, White, (loc[0] - 110, loc[1] - 75, 220, 50))

        self.font.render_to(
            self.screen, (loc[0] - 108, loc[1] - 73), recharge_rate_text, Black)

        self.font.render_to(
            self.screen, (loc[0] - 108, loc[1] - 48), name, Black)

    def update(self):
        pygame.draw.rect(self.screen, White, (0, 0, 750, 100))
        off_y = -25
        for text in help_text:
            off_y += 30
            self.font.render_to(self.screen,(5, off_y), text, Black)

        to_delete = []
        for buoy_cfg in self.all_buoys:
            b_x = buoy_cfg[-1][0]
            b_y = buoy_cfg[-1][1]

            if b_x < 0 or b_y < 0:
                to_delete.append(buoy_cfg)
                continue            
            
            elif b_x > 1280 or b_y > 720:
                to_delete.append(buoy_cfg)
                continue
            
            self.draw_buoy(buoy_cfg)

        for drone_cfg in self.all_drones:
            charge = drone_cfg[0]
            d_x = drone_cfg[-1][0]
            d_y = drone_cfg[-1][1]
            m_x = drone_cfg[-3][0]
            m_y = drone_cfg[-3][1]
            
            # Checking if current x or y is out of bounds
            if d_x < 0 or d_y < 0:
                to_delete.append(drone_cfg)
                continue            
            
            elif d_x > 1280 or d_y > 720:
                to_delete.append(drone_cfg)
                continue
            
            # Checking if battery level is 55 or below
            if charge <= 55:
                if charge <= 0:
                    to_delete.append(drone_cfg)    
                    continue
                if len(self.all_buoys) > 0:
                    b_x = self.all_buoys[0][-1][0]
                    b_y = self.all_buoys[0][-1][1]
                    closest = math.sqrt(
                        (b_x - d_x) ** 2 + (b_y - d_y) ** 2)
                    
                    for buoy_cfg in self.all_buoys:
                        b_x = buoy_cfg[-1][0]
                        b_y = buoy_cfg[-1][1]
                        distance = math.sqrt(
                            (b_x - d_x) ** 2 + (b_y - d_y) ** 2)
                        
                        rel_pos = d_x - b_x, d_y - b_y
                        
                        if distance <= closest:
                            closest = distance
                            current = buoy_cfg
                            rel_pos = d_x - b_x, d_y - b_y
                        
                        print(f"b {b_x} {b_y}")
                        print(f"d {d_x} {d_y}")
                        print(rel_pos)

                        ret = self.what_quad(rel_pos)
                        print(ret)
                        # ret[0], ret[1] = ret[1], ret[0]
                        
                        if ret == True:
                            drone_cfg[0] += buoy_cfg[0]
                        else:
                            m_x = ret[0]
                            m_y = ret[1]

            # Random movement
            drone_cfg[-1][0] += m_x
            drone_cfg[-1][1] += m_y
            drone_cfg[0] -= 1 if random.randint(0, 2) == 1 else 0 
            self.draw_drone(drone_cfg)
        
        for drone_cfg in to_delete:
            Drone.delete_drone(self, drone_cfg)

class Drone:
    def create_drone(Map_object, battery=100 , module="b", loc=[0, 0]):
        """module options are currently (b)ase, (c)amera, (s)onar, (cu)stom"""
        if module == "b":
            search_area = 0
        elif module == "c":
            search_area = 50
        elif module == "s":
            search_area = 10
        else:
            search_area = 500

        direction = random.choice([(-1, 0), (0, 1), (1, 0), (0, -1)])
        Map_object.all_drones.append(
            [battery, module, direction, search_area, loc])
    
    def delete_latest_drone(Map_object):
        all_drones = Map_object.all_drones
        if len(all_drones) >= 1:
            Map_object.all_drones.pop()
        else:
            print("Nothing to delete")
    
    def delete_drone(Map_object, drone_cfg):
        Map_object.all_drones.remove(drone_cfg)


class Buoy:
    def create_buoy(Map_object, recharging_speed=1, loc=[0, 0]):
        Map_object.all_buoys.append(
        [recharging_speed, loc])
    
    def delete_latest_buoy(Map_object):
        all_buoys = Map_object.all_buoys
        if len(all_buoys) >= 1:
            Map_object.all_buoys.pop()
        else:
            print("Nothing to delete")
    
    


if __name__ == "__main__":
    Black = (0, 0, 0)
    White = (255, 255, 255)
    Red = (255, 0, 0)
    Green = (0, 255, 0)
    Ocean_Blue = (0, 105, 148)
    Purple = (255, 0, 255)
    Yellow = (0, 255, 255)

    pygame.init()
    board = Map()
    help_text = [
        "A to spawn drones, D to delete the most recent drone!",
        "Z to spawn a buoy, C to delete the most recent buoy!",
        "Q to quit or press the x on the top left!"]

    while True:
        board.screen.fill(Ocean_Blue)
        board.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    print("Add drone")
                    loc = [random.randint(0, 1280), random.randint(0, 720)]
                    module = random.choice(["b", "c", "s"])
                    Drone.create_drone(board, module=module, loc=loc)

                elif event.key == pygame.K_d:
                    print("Delete drone")
                    Drone.delete_latest_drone(board)

                elif event.key == pygame.K_z:
                    print("Add buoy")
                    loc = [random.randint(200, 1080), random.randint(100, 620)]
                    watt_out = random.randint(1, 5)
                    Buoy.create_buoy(board, recharging_speed=watt_out, loc=loc)

                elif event.key == pygame.K_c:
                    print("Delete buoy")
                    Buoy.delete_latest_buoy(board)

                elif event.key == pygame.K_q:
                    print("q_exit")
                    exit()

            if event.type == pygame.QUIT:
                    print("x_exit")
                    exit()

        pygame.display.flip()
        sleep(0.04166) # 1000 / fps = duration during each frame (in milliseconds)
