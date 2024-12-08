from typing import Tuple
import pygame
from ACO.parking import Parking

class Car:
    def __init__(
            self,
            pos: Tuple[int, int] = (0,0),
            angle: int = 0
            ) -> None:
        
        self.pos = pos
        self.width = 106
        self.height = 56
        self.speed = 10
        self.angle = angle
        self.corners = [[self.pos[0]+self.width//2*i, self.pos[1]+self.height//2*j] for i in [-1, 1] for j in [-1, 1]]

        self.image = pygame.image.load("ACO/images/car_parking.png")
        self.rect = self.image.get_rect(center=self.pos)
        self.rotated_image = self.image
        self.rotated_rect = self.rotated_image.get_rect(center=self.pos)

        self.update((self.pos[0], self.pos[1], self.angle))


    def draw(
            self,
            screen: pygame.Surface
            ) -> None:
        
        screen.blit(self.rotated_image, self.rotated_rect)

    def brake(self) -> None:
        self.speed = max(self.speed-0.5, 0)

    def update(
            self,
            pos: Tuple[int, int]
            ) -> None:
        
        self.pos = pos[0], pos[1]
        self.angle = pos[2]

        self.rotated_image = pygame.transform.rotate(self.image, self.angle)
        self.rotated_rect = self.rotated_image.get_rect(center = self.pos)

    def park(
            self,
            parking: Parking
            ) -> None:
        
        if parking.check_park(self.rotated_rect):
            self.brake()
        else:
            self.pos = [self.pos[0], self.pos[1] - self.speed]
        self.update((self.pos[0], self.pos[1], self.angle))