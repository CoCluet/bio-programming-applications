
import math
from typing import Tuple, List
import numpy as np
import matplotlib.pyplot as plt
from ACO.parking import Parking

class TrajectoryAntColonyOptimization:
    def __init__(
            self,
            parking: Parking
            ) -> None:
        
        self.parking = parking
        self.start = (parking.start_pos[0], 720-parking.start_pos[1], parking.start_pos[2])
        self.end = (parking.end_pos[0], 720-parking.end_pos[1], parking.end_pos[2])

    def init_parameters(
            self,
            num_ants: int = 50,
            num_elite_ants: int = 10,
            num_iterations: int = 20,
            alpha: float = 1.0,
            beta: float = 2.0,
            evaporation_rate: float = 0.1,
            **kwargs
            ) -> None:
        
        self.num_ants = num_ants
        self.num_elite_ants = num_elite_ants
        self.num_iterations = num_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate

    def possibilities(
            self,
            node: Tuple[int, int, int],
            angle: int, length: int
            ) -> List[Tuple[int, int, int]]:
        
        childrens = []
        for ang in (-angle,0,angle):
            x = int(node[0] + math.cos(math.radians(node[2] + ang)) * length)
            y = int(node[1] - math.sin(math.radians(node[2] + ang)) * length)
            if self.parking.check_pos((x, 720-y), -(node[2]+ang)):
                childrens.append((x, y, node[2]+ang))
        return childrens

    def node_distance(
            self,
            node1: Tuple[int, int, int],
            node2: Tuple[int, int, int]
            ) -> float:
        
        return ((node1[0]-node2[0])**2+(node1[1]-node2[1])**2)**0.5

    def fitness(
            self,
            path: List[Tuple[int, int, int]],
            end_point: Tuple[int, int, int]
            ) -> float:
        
        d = 0
        for i in range(len(path)-1):
            d += self.node_distance(path[i], path[i+1])
        return d + 30*self.node_distance(path[-1], end_point) + 20*(path[-1][2]-end_point[2])**2
    
    def get_optimal_path(
            self,
            length_segments: int,
            angle: int,
            num_max_segments: int,
            **kwargs
            ) -> List[Tuple[int, int, int]]:
        
        print("--- calculation in progress --- ")
        main_path = self.ACO(self.start, self.end, length_segments, angle, num_max_segments, False)
        print("--- path find ! ---")
        return main_path
    
    def ACO(
            self,
            start: Tuple[int, int, int],
            end: Tuple[int, int, int],
            length_segments: int,
            angle: int,
            num_max_segments: int,
            display: bool = True
            ) -> List[Tuple[int, int, int]]:
        
        pheromone = {start : 1} #contains the pheromones associated with each node
        best_path = []
        best_fitness = 1000000
        means = []
        bests = []

        for iteration in range(self.num_iterations):
            if display : print("Iteration : ", iteration+1, "...")

            ant_paths = []

            for ant in range(self.num_ants):
                current_node = start
                path = [start]

                for _ in range(num_max_segments):
                    next_nodes = self.possibilities(current_node, angle, length_segments)

                    if len(next_nodes) == 0:
                        break
                    elif len(next_nodes) == 1:
                        next_node = next_nodes[0]
                        if next_node not in pheromone:
                                pheromone[next_node] = 1
                    else:
                        probabilities = np.array([0.]*len(next_nodes))
                        sum_total = 0
                        for i,next_node in enumerate(next_nodes):
                            if next_node not in pheromone:
                                pheromone[next_node] = 1
                            pheromone_amount = pheromone[next_node]

                            distance = self.node_distance(next_node,end)
                            if distance == 0 : probabilities[i] = 100
                            else: probabilities[i] = pheromone_amount ** self.alpha * (1.0 / distance) ** self.beta
                        sum_total = np.sum(probabilities)
                        if sum_total == 0:
                            break
                        probabilities = probabilities/sum_total

                        next_node = next_nodes[np.random.choice(len(next_nodes), p=probabilities)]

                    path.append(next_node)

                    if self.node_distance(next_node,end) < length_segments/2:
                        break

                    current_node = next_node

                ant_paths.append(path)

            # pheromones update
            for node, pheromone_amount in pheromone.items():
                pheromone[node] = pheromone_amount * (1.0 - self.evaporation_rate)
            for path in ant_paths:
                for node in path:
                    if self.fitness(path,end)!=0:
                        pheromone[node] += 100 / self.fitness(path,end)
            # best path update
            best_local_path = min(ant_paths, key=lambda x : self.fitness(x,end))
            if self.fitness(best_local_path,end) < best_fitness:
                best_path = best_local_path
                best_fitness = self.fitness(best_local_path,end)

            # elitist ants retrace the best path to increase pheromone
            for i in range(self.num_elite_ants):
                for node in best_path:
                    pheromone[node] += 100/best_fitness

            if display: 
                print("Actual best path : ",best_path)
                print("Actual best fitness : ",best_fitness)
                print("")

            fitnesses = np.array(list(map(lambda x:self.fitness(x, end), ant_paths)))
            bests.append(np.min(fitnesses))
            means.append(np.mean(fitnesses))

        if self.node_distance(best_path[-1], end) > 2* length_segments:
            print("Optimization failed, retry in progress...")
            print("Distance from end : ",self.node_distance(best_path[-1], end))
            return self.ACO(start, end, length_segments, angle, num_max_segments, display)
        
        x = [i for i in range(self.num_iterations)]

        fig, ax = plt.subplots()
        ax.plot(x, means, '--b', label='average fitness')
        ax.plot(x, bests, '-r', label='best fitness')
        ax.set_xlabel('Iterations')
        ax.set_ylabel('Fitness')
        ax.legend()
        plt.show()

        fig, ax = plt.subplots()
        ax.plot(x, bests, '-r', label='best fitness')
        ax.set_xlabel('Iterations')
        ax.set_ylabel('Fitness')
        ax.legend()
        plt.show()
        
        return best_path