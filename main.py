import pygame
from queue import Queue

# 1. Configuration and Constants
WIDTH = 600
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Pathfinding Visualizer (BFS)")

# Color Definitions (RGB)
WHITE = (255, 255, 255)    # Unvisited Node
BLACK = (0, 0, 0)          # Wall / Obstacle
GRAY = (200, 200, 200)      # Grid Line
ORANGE = (255, 165, 0)      # Start Node
TURQUOISE = (64, 224, 208)  # End Node
RED = (255, 0, 0)          # Visited / Searched Node
GREEN = (0, 255, 0)        # Node currently in the queue
YELLOW = (255, 255, 0)     # Final Shortest Path

# 2. Node Class representing each square on the grid
class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_wall(self):
        return self.color == BLACK

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_wall(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_visited(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_path(self):
        self.color = YELLOW

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        # Check Down
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall():
            self.neighbors.append(grid[self.row + 1][self.col])
        # Check Up
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():
            self.neighbors.append(grid[self.row - 1][self.col])
        # Check Right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall():
            self.neighbors.append(grid[self.row][self.col + 1])
        # Check Left
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():
            self.neighbors.append(grid[self.row][self.col - 1])

# 3. Grid Helper Functions
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GRAY, (0, i * gap), (width, i * gap))
        pygame.draw.line(win, GRAY, (i * gap, 0), (i * gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

# 4. Path Reconstruction Function
def reconstruct_path(came_from, current, draw_func):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw_func()

# 5. Core BFS Algorithm Integration
def bfs_algorithm(draw_func, grid, start, end):
    queue = Queue()
    queue.put(start)
    came_from = {}
    visited = {start}

    while not queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current = queue.get()

        if current == end:
            reconstruct_path(came_from, end, draw_func)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                came_from[neighbor] = current
                visited.add(neighbor)
                queue.put(neighbor)
                neighbor.make_open()

        draw_func()

        if current != start:
            current.make_visited()

    return False

# 6. Main Executable Loop
def main(win, width):
    ROWS = 30
    grid = make_grid(ROWS, width)

    start = None
    end = None
    run = True

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Left Click Actions
            if pygame.mouse.get_pressed()[0]: 
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != end and node != start:
                    node.make_wall()

            # Right Click Action (Clear Node)
            elif pygame.mouse.get_pressed()[2]: 
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            # Keyboard Actions
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    bfs_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

if __name__ == "__main__":
    main(WIN, WIDTH)
