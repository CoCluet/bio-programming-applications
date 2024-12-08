import random
import argparse
import pygame
import neat
from ACO.engine import Engine
from NEAT.simulation import Simulation
import NEAT.visualize as visualize

def run_aco():
    pygame.init()
    screen = pygame.display.set_mode((1080, 720))
    engine = Engine(screen)
    engine.run()
    pygame.quit()

def run_neat():
    random.seed(123)

    config = neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,neat.DefaultStagnation,
                                "./NEAT/config.txt")

    population = neat.Population(config)
    stats = neat.StatisticsReporter()
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(stats)
    population.run(Simulation.eval_genomes, 200)

    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

    pygame.quit()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--method', choices=['ACO', 'NEAT'])
    args = parser.parse_args()

    if args.method == 'ACO':
        run_aco()
    elif args.method == 'NEAT':
        run_neat()
    else:
        print('-------------------------------------------------------------------')
        print('/!\\ Choose method to execute, with argument --method (ACO or NEAT).')
        print('-------------------------------------------------------------------')

if __name__ == '__main__':
    main()