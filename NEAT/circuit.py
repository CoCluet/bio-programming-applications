from typing import Tuple, List
import pygame

class Circuit:
    ROAD_COLORS = [(140, 158, 158), (255, 255, 255), (65, 65, 65)]

    def __init__(
            self,
            screen: pygame.Surface
            ) -> None:
        
        self.screen = screen

        self.img = pygame.image.load('NEAT/images/circuit.png')
        self.img_info = pygame.image.load('NEAT/images/circuit_info.png')
        
        self.screen.blit(self.img_info, (0, 0))
        self.screen.blit(self.img, (0, 0))

    def check_coord(
            self,
            coord: Tuple[int, int]
            ) -> bool:
        
        if self.img.get_at((int(coord[0]), int(coord[1]))) not in Circuit.ROAD_COLORS:
            return False
        return True
    
    def check_list_coord(
            self,
            coords: List[Tuple[int, int]]
            ) -> None:
        
        for coord in coords:
            if not self.check_coord(coord):
                return False
        return True
    
    def get_dist_color(
            self,
            coord: Tuple[int, int]
            ) -> Tuple[int, int, int]:
        return self.img_info.get_at((int(coord[0]), int(coord[1])))
    
    def draw(self) -> None:
        self.screen.blit(self.img_info, (0, 0))
        self.screen.blit(self.img, (0, 0))