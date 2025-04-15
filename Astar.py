import os
import time
import pygame
import psutil
import numpy as np
from queue import PriorityQueue

class Astar:
    """A* for solving """
    def __init__(self, benchmark=False, heuristik="manhattan"):
        
        # Pygame initialization
        pygame.init()
        pygame.font.init()
        
        # For benchmark purpose
        self.benchmark = benchmark
        self.heuristik = heuristik
        # Visualization configuration
        self.width = 600
        self.height = 600
        self.gridsize = 3
        self.tilesize = self.width // self.gridsize

        # Starting state
        self.start = (
            (7, 2, 4),
            (5, 0, 6),
            (8, 3, 1)
        )

        # Goal state
        self.goal = (
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8)
        )
        
        # Colour
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)

    def euclidean_distance(self, state):
        """Heuristik Euclidean Distance"""
        distance = 0
        for i in range(3):
            for j in range(3):
                val = state[i][j]
                if val != 0:
                    target = np.where(np.array(self.goal) == val)
                    distance += ((i - target[0][0]) ** 2 + (j - target[1][0]) ** 2) ** 0.5
        return distance

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

    def solve_puzzle(self):
        """Solve the 8-puzzle"""
        open_list = PriorityQueue()
        if self.heuristik == "euclidean":
            open_list.put((self.euclidean_distance(self.start), 0, self.start, []))
        else:
            open_list.put((self.manhattan_distance(self.start), 0, self.start, []))
        closed_list = set()

        while not open_list.empty():
            f, g, current, path = open_list.get()
            
            if current == self.goal:
                return path + [current]

            if current in closed_list:
                continue
            closed_list.add(current)

            # Cari posisi kotak kosong (0)
            zero_pos = next((i, j) for i, row in enumerate(current) for j, val in enumerate(row) if val == 0)

            # Generate child states
            moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for dx, dy in moves:
                new_row = zero_pos[0] + dx
                new_col = zero_pos[1] + dy

                if 0 <= new_row < 3 and 0 <= new_col < 3:
                    # Swap posisi
                    new_state = list(map(list, current))
                    new_state[zero_pos[0]][zero_pos[1]] = new_state[new_row][new_col]
                    new_state[new_row][new_col] = 0
                    new_state_tuple = tuple(map(tuple, new_state))

                    if new_state_tuple not in closed_list:
                        h = self.manhattan_distance(new_state_tuple)
                        open_list.put((g + 1 + h, g + 1, new_state_tuple, path + [current]))

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
        pygame.display.set_caption("8-Puzzle Solver using A*")
        clock = pygame.time.Clock()

        solution_path = self.solve_puzzle()
        if not solution_path:
            print("No solution exists!")
            return

        current_step = 0
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update the visualization every 1 second
            if current_step < len(solution_path):
                self.draw_grid(screen, solution_path[current_step])
                pygame.display.flip()
                pygame.time.wait(1000) if not self.benchmark else pygame.time.wait(0)
                current_step += 1
            else:
                pygame.time.wait(3000) if not self.benchmark else pygame.time.wait(0)
                running = False

            clock.tick(30)
        self.current_step = current_step
        pygame.quit()

if __name__ == "__main__":
    process = psutil.Process(os.getpid())
    start = time.perf_counter()
    astar = Astar(1, "euclidean")
    # astar = Astar(1, "manhattan")
    astar.main()
    memory_usage = process.memory_info().rss / 1024 ** 2
    print(f"Steps: {astar.current_step}")
    print(f"Finish in {(time.perf_counter() - start)*1000:.2f} ms")
    print(f"Memory usage: {memory_usage:.2f} MB")
    print(f"A Star with {astar.heuristik} heuristik")