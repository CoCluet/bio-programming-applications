import math
import time
from typing import List, Union
import pygame
from NEAT.circuit import Circuit

class Car:
    def __init__(
            self,
            circuit: Circuit
            ) -> None:
        
        self.pos = [570, 548]
        self.width = 40
        self.height = 20

        self.speed = 0
        self.velocity = 0

        self.angle = 0
        self.wheel_angle = 0

        self.corners = [[self.pos[0]+self.width//2*i,self.pos[1]+self.height//2*j] for i in [-1,1] for j in [-1,1]]
        self.sensors = []
        self.update_sensors(circuit)

        self.image = pygame.image.load("NEAT/images/car_circuit.png")
        self.rect = self.image.get_rect(center=self.pos)
        self.rotated_image = self.image
        self.rotated_rect = self.rotated_image.get_rect(center=self.pos)

        self.current_dist_color = (0, 0, 0)
        self.distance = 0
        self.lap = -1

        self.time = 0
        self.init_time = 0
        self.alive = True

    ## DISPLAY ##

    def draw(
            self,
            screen: pygame.Surface
            ) -> None:
        
        screen.blit(self.rotated_image, self.rotated_rect)
        self.draw_corners(screen)
        self.draw_sensors(screen)

    def draw_corners(
            self,
            screen: pygame.Surface
            ) -> None:
        
        for coord in self.corners:
            pygame.draw.circle(screen, pygame.Color('red'), coord, 2)
        pygame.draw.circle(screen, pygame.Color('red'), self.pos, 2)

    def draw_sensors(
            self,
            screen: pygame.Surface
            ) -> None:
        
        for sensor in self.sensors:
            pygame.draw.circle(screen, pygame.Color('red'), sensor[0], 2)
            pygame.draw.line(screen, pygame.Color('red'), self.pos, sensor[0], 1)

    ## ACTIONS ##
    def turn(self, angle: int) -> None:
        if self.speed > 1:
            if angle>0:
                self.wheel_angle = min(50,self.wheel_angle+angle)
            else:
                self.wheel_angle = max(-50,self.wheel_angle+angle)
        else:
            self.alive = False

    def move(self, direction: int) -> None:
        if self.velocity == direction == -1:
            self.speed = max(self.speed+1,5)
        elif self.velocity == direction == 1:
            self.speed = max(self.speed+1,5)
        elif self.velocity == -1 and direction == 1:
            self.speed = max(0,self.speed-1.5)
            if self.speed == 0 : self.velocity = 1
        else:
            self.speed = max(0,self.speed-1.5)
            if self.speed == 0 : self.velocity = -1

    def brake(self) -> None:
        self.speed = max(self.speed-1,0)
        if self.speed < 2: 
            self.alive = False

    def decrease_rotation(self) -> None:
        if self.wheel_angle>0:
            self.wheel_angle = max(0,self.wheel_angle-5)
        else:
            self.wheel_angle = min(0,self.wheel_angle+5)

    def decrease_speed(self) -> None:
        self.speed = max(0,max(self.speed-0.4,self.speed*0.95))
        if self.speed < 0.2 : self.speed = 0

    ## UPDATES ##

    def update_sensors(self, circuit: Circuit) -> None:
        self.sensors = []
        for ang in [-90,-45,0,35,90]:
            length = 0
            x,y = int(self.pos[0]),int(self.pos[1])
            while length < 350 and circuit.check_coord((x,y)):
                length += 1
                x = int(self.pos[0] + math.cos(math.radians(self.angle + ang)) * length)
                y = int(self.pos[1] - math.sin(math.radians(self.angle + ang)) * length)
            d = math.sqrt((x - self.pos[0])**2 + (y - self.pos[1])**2)
            self.sensors.append([(x, y), d])

    def update(self, circuit: Circuit) -> None:
        # update of the total angle of the car
        self.angle += self.wheel_angle * self.velocity * 0.05 * math.log(2*self.speed+1)
        # update of the future position of the car according to the angle and the speed
        self.pos[0] += math.cos(math.radians(self.angle)) * self.speed * self.velocity * 0.5
        self.pos[1] -= math.sin(math.radians(self.angle)) * self.speed * self.velocity * 0.5
        # rotation of the image and the rect
        self.rotated_image = pygame.transform.rotate(self.image, self.angle)
        self.rotated_rect = self.rotated_image.get_rect(center = self.pos)
        # update of each corner coordinates
        self.corners = []
        d = math.sqrt(self.width**2+self.height**2)/2 # distance between the center of the car and each corner
        for i in [[-1,-1],[-1,1],[1,-1],[1,1]]:
            new_angle = math.atan2(self.height,self.width) - i[0]*i[1] * math.radians(self.angle)
            self.corners.append([self.pos[0]+i[0]*d*math.cos(new_angle),self.pos[1]+i[1]*d*math.sin(new_angle)])


        if not circuit.check_list_coord(self.corners):
            self.alive = False

        new_color = circuit.get_dist_color(self.pos)
        if new_color != self.current_dist_color:
            self.current_dist_color = new_color
            self.distance += 1
            if new_color == (255,0,0):
                self.lap += 1

        # stopping conditions
        if self.lap == 3 or self.get_time() > 120:
            self.alive = False

        self.check_speed()

    def start_timer(self) -> None:
        self.init_time = time.time()

    def get_time(self) -> float:
        end_time = time.time()
        return end_time - self.init_time

    def check_speed(self) -> None:
        if self.get_time() > 3 and self.speed < 3 :
            self.alive = False

    def get_inputs(self) -> List[Union[int, float]]:
        inputs = []
        for sensor in self.sensors:
            inputs.append(int(sensor[1]))
        inputs.append(self.speed)
        inputs.append(self.wheel_angle)
        return inputs
    
    def get_score(self) -> float:
        return self.distance + self.distance/max(1, self.get_time())
    
    def execute_action(self, choice: int) -> None:
        if choice == 0:
            self.turn(10)
        elif choice == 1:
            self.turn(-10)
        else:
            self.decrease_rotation()

        if choice == 2:
            self.move(1)
        elif choice == 3:
            self.brake()
        else:
            self.decrease_speed()