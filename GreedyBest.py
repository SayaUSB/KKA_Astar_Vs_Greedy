import os
import time
import pygame
import psutil
import numpy as np
from queue import PriorityQueue

class GreedyBest:
    def __init__(self, benchmark=False):

        # Pygame Initialization
        pygame.init()
        pygame.font.init()

        # For benchmark purpose
        self.benchmark = benchmark
        
        # Visualization configuration
        self.width = 600
        self.height = 600
        self.gridsize = 3
        self.tilesize = self.width // self.gridsize

        # Colour
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        
        # Starting state
        self.start = ((7, 2, 4), 
                      (5, 0, 6), 
                      (8, 3, 1))

        # Goal state
        self.goal = ((0, 1, 2), 
                     (3, 4, 5), 
                     (6, 7, 8))

    def manhattan_distance(self, state):
        """Heuristik Manhattan Distance"""
        distance = 0
        for i in range(3):
            for j in range(3):
                val = state[i][j]
                if val != 0:
                    target = np.where(np.array(self.goal) == val)
                    distance += abs(i - target[0][0]) + abs(j - target[1][0])
        return distance

    def solve_puzzle_greedy(self):
        """Solve the puzzle using Greedy Best-First Search algorithm"""
        open_list = PriorityQueue()
        open_list.put((self.manhattan_distance(self.start), self.start, []))
        closed_list = set()

        while not open_list.empty():
            h, current, path = open_list.get()
            
            if current == self.goal:
                return path + [current]

            if current in closed_list:
                continue
            closed_list.add(current)

            # Empty box contain number zero
            zero_pos = next((i, j) for i, row in enumerate(current) for j, val in enumerate(row) if val == 0)

            # Generate child states
            moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for dx, dy in moves:
                new_row = zero_pos[0] + dx
                new_col = zero_pos[1] + dy

                if 0 <= new_row < 3 and 0 <= new_col < 3:
                    new_state = list(map(list, current))
                    new_state[zero_pos[0]][zero_pos[1]] = new_state[new_row][new_col]
                    new_state[new_row][new_col] = 0
                    new_state_tuple = tuple(map(tuple, new_state))

                    if new_state_tuple not in closed_list:
                        h_child = self.manhattan_distance(new_state_tuple)
                        open_list.put((h_child, new_state_tuple, path + [current]))

        return None

    def draw_grid(self, screen, state):
        """Rendering the grid"""
        screen.fill(self.white)
        for i in range(self.gridsize):
            for j in range(self.gridsize):
                val = state[i][j]
                rect = pygame.Rect(j*self.tilesize, i*self.tilesize, self.tilesize, self.tilesize)
                
                if val == 0:
                    pygame.draw.rect(screen, self.red, rect)  
                    pygame.draw.rect(screen, self.red, rect, 3)  
                else:
                    pygame.draw.rect(screen, self.red, rect, 3)
                    font = pygame.font.SysFont(None, 74)
                    text = font.render(str(val), True, self.black)
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)

    def main(self):
        """Main program"""
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("8-Puzzle using Greedy Best-First Search")
        
        solution_path = self.solve_puzzle_greedy()
        
        if not solution_path:
            print("Tidak ada solusi!")
            return

        current_step = 0
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if current_step < len(solution_path):
                self.draw_grid(screen, solution_path[current_step])
                pygame.display.flip()
                pygame.time.wait(1000) if not self.benchmark else pygame.time.wait(0)
                current_step += 1
            else:
                pygame.time.wait(3000) if not self.benchmark else pygame.time.wait(0)
                running = False
        self.current_step = current_step
        pygame.quit()

if __name__ == "__main__":
    process = psutil.Process(os.getpid())
    start = time.perf_counter()
    greedy = GreedyBest(1)
    greedy.main()
    memory_usage = process.memory_info().rss / 1024 ** 2
    print(f"Steps: {greedy.current_step}")
    print(f"Finish in {(time.perf_counter()-start)*1000:.2f} ms")
    print(f"Memory usage: {memory_usage:.2f} MB")