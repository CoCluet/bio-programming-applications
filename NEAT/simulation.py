import sys
import time
import pygame
import neat
from NEAT.car import Car
from NEAT.circuit import Circuit

class Simulation:
    current_generation = 0

    @staticmethod
    def eval_genomes(genomes, config):
        Simulation.current_generation += 1

        pygame.init()
        screen = pygame.display.set_mode((1080, 720))
        circuit = Circuit(screen)

        nets = []
        cars = []

        for i, g in genomes:
            net = neat.nn.FeedForwardNetwork.create(g, config)
            nets.append(net)
            g.fitness = 0
            cars.append(Car(circuit))

        clock = pygame.time.Clock()
        timer = time.time()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

            for i, car in enumerate(cars):
                if car.init_time == 0 :
                    car.start_timer()
                output = nets[i].activate(car.get_inputs())
                choice = output.index(max(output))
                car.execute_action(choice)
            
            still_alive = 0
            for i, car in enumerate(cars):
                if car.alive:
                    still_alive += 1
                    car.update(circuit)
                    car.update_sensors(circuit)
                    genomes[i][1].fitness = car.get_score()

            best_fitness = round(max(genome[1].fitness for genome in genomes),2)
            best_distance = max(car.distance for car in cars)
 

            if still_alive == 0:
                break

            # Draw circuit and cars
            circuit.draw()
            for car in cars:
                if car.alive:
                    car.draw(screen)
            
            # Display Info
            infos = [["Generation", Simulation.current_generation],
                      ["Cars Alive", still_alive],
                      ["Best fitness", best_fitness],
                      ["Best distance", best_distance],
                      ["Time", int(time.time()-timer)]]

            font = pygame.font.SysFont("Arial", 14)
            for i,info in enumerate(infos):
                text = font.render(f"{info[0]} : {info[1]}",True, (0,0,0))
                text_rect = text.get_rect()
                text_rect.midleft = (10, 15 + i*20)
                screen.blit(text, text_rect)

            pygame.display.flip()
            clock = pygame.time.Clock()
            clock.tick(15) 
