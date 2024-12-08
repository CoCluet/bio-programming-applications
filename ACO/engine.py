
import json
import pygame
from ACO.car import Car
from ACO.parking import Parking
from ACO.optimization import TrajectoryAntColonyOptimization

class Engine:
    def __init__(
            self,
            screen: pygame.Surface
            ) -> None:
        
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()

        ### we can choose different problems
        ## PROBLEM 1
        self.parking = Parking(screen, Parking.MODELE_1)
        with open("ACO/config1.json", 'r') as f:
            config = json.load(f)

        ## PROBLEM 2
        '''
        self.parking = Parking(screen, Parking.MODELE_2)
        with open("ACO/config2.json", 'r') as f:
            config = json.load(f)
        '''

        self.car = Car([self.parking.start_pos[0], self.parking.start_pos[1]], self.parking.start_pos[2])

        self.parking.draw()
        self.car.draw(self.screen)
        pygame.display.flip()

        ACO = TrajectoryAntColonyOptimization(self.parking)
        ACO.init_parameters(**config)
        self.path = ACO.get_optimal_path(**config)



    def handling_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.running = False
            
    def display(self) -> None:
        self.parking.draw()
        self.car.draw(self.screen)
        for node1,node2 in zip(self.path[:-1], self.path[1:]):
            pygame.draw.line(self.screen, pygame.Color('blue'), (node1[0],720-node1[1]), (node2[0],720-node2[1]), 2)

    def run(self) -> None:
        i = 0
        while self.running:
            self.handling_events()
            if i < len(self.path):
                self.car.update((self.path[i][0], 720-self.path[i][1], -self.path[i][2]))
                i += 1
            else:
                self.car.park(self.parking)
            self.display()
            self.clock.tick(10)
            pygame.display.flip()