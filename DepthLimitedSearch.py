import os
import time
import pygame
import psutil
import numpy as np

class DepthLimitedSearch:
    """Depth-Limited Search for solving the 8-puzzle"""
    def __init__(self, depth_limit=50, benchmark=False):
        # Pygame initialization
        pygame.init()
        pygame.font.init()

        # For benchmark purpose
        self.benchmark = benchmark
        self.depth_limit = depth_limit

        # Visualization configuration
        self.width = 600
        self.height = 600
        self.gridsize = 3
        self.tilesize = self.width // self.gridsize
        self.current_step = 0

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

    def depth_limited_search(self, state, depth, path, visited):
        """Recursive Depth-Limited Search"""
        if state == self.goal:
            return path + [state]

        if depth == 0:
            return None

        visited.add(state)
        zero_pos = next((i, j) for i, row in enumerate(state) for j, val in enumerate(row) if val == 0)
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dx, dy in moves:
            new_row = zero_pos[0] + dx
            new_col = zero_pos[1] + dy

            if 0 <= new_row < 3 and 0 <= new_col < 3:
                # Swap positions
                new_state = list(map(list, state))
                new_state[zero_pos[0]][zero_pos[1]] = new_state[new_row][new_col]
                new_state[new_row][new_col] = 0
                new_state_tuple = tuple(map(tuple, new_state))

                if new_state_tuple not in visited:
                    result = self.depth_limited_search(new_state_tuple, depth - 1, path + [state], visited)
                    if result:
                        return result

        return None

    def solve_puzzle(self):
        """Solve the 8-puzzle using Depth-Limited Search"""
        visited = set()
        return self.depth_limited_search(self.start, self.depth_limit, [], visited)

    def draw_grid(self, screen, state):
        """Rendering the grid"""
        screen.fill(self.white)
        for i in range(self.gridsize):
            for j in range(self.gridsize):
                val = state[i][j]
                rect = pygame.Rect(j * self.tilesize, i * self.tilesize, self.tilesize, self.tilesize)

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
        pygame.display.set_caption("8-Puzzle Solver using Depth-Limited Search")
        clock = pygame.time.Clock()

        solution_path = self.solve_puzzle()
        if not solution_path:
            print("No solution exists within the depth limit!")
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
    dls = DepthLimitedSearch(depth_limit=100, benchmark=True)
    dls.main()
    memory_usage = process.memory_info().rss / 1024 ** 2
    print(f"Steps: {dls.current_step}")
    print(f"Finish in {(time.perf_counter() - start) * 1000:.2f} ms")
    print(f"Memory usage: {memory_usage:.2f} MB")
    print(f"Depth-Limited Search with depth limit {dls.depth_limit}")