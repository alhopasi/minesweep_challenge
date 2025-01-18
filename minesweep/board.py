import random

class Tile:
    NOT_EXPLORED = 9
    MINE = 10
    MINE_EXPLORED = 11
    SKIP = 15

class MinesweepBoard:
    def __init__(self, dimension):
        self.dimension = dimension
        self.board = [ [Tile.NOT_EXPLORED] * self.dimension for _ in range(self.dimension) ]

    def create_mines(self):
        mines = round(self.dimension * self.dimension * random.uniform(0.16, 0.22))
        if mines == 0: mines = 1

        for _ in range(mines):
            while True:
                mine_y = random.randint(0, self.dimension-1)
                mine_x = random.randint(0, self.dimension-1)
                if self.board[mine_y][mine_x] != Tile.MINE:
                    self.board[mine_y][mine_x] = Tile.MINE
                    break
    
    def reset_board(self, dimension):
        self.dimension = dimension
        self.board = [ [Tile.NOT_EXPLORED] * self.dimension for _ in range(self.dimension) ]

    def set_tile_value(self, y, x, value):
        self.board[y][x] = value

    def is_explored(self, y, x):
        return self.board[y][x] not in [Tile.NOT_EXPLORED, Tile.MINE]
    
    def explore(self, y, x):
        if self.is_explored(y, x):
            return None
        
        explored_tile = self.board[y][x]

        if explored_tile == Tile.MINE:
            self.board[y][x] = Tile.MINE_EXPLORED
            return None
        
        mines = self.count_mines_close(y, x)

        self.board[y][x] = mines

        if mines == 0:
            for y_ in range(-1,2):
                for x_ in range(-1,2):
                    if self.in_bounds(y + y_, x + x_):
                        self.explore(y + y_, x + x_)

    def in_bounds(self, y, x):
        return 0 <= y < self.dimension and 0 <= x < self.dimension
    
    def is_mine(self, y, x):
        return self.board[y][x] == Tile.MINE or self.board[y][x] == Tile.MINE_EXPLORED

    def count_mines_close(self, y, x):
        mines = 0
        for y_ in range(-1,2):
            for x_ in range(-1,2):
                check_y, check_x = y + y_, x + x_
                if self.in_bounds(check_y, check_x) and self.is_mine(check_y, check_x):
                    mines += 1
        return mines
    
    def check_mine_hit(self):
        for row in self.board:
            if Tile.MINE_EXPLORED in row:
                return True
        return False
    
    def check_victory(self):
        for y in range(self.dimension):
            for x in range(self.dimension):
                if self.board[y][x] == Tile.NOT_EXPLORED:
                    return False
        return True

    def coords_to_index(self, y, x):
        return y * self.dimension + x
    
    def index_to_coords(self, index):
        y = index // self.dimension
        x = index % self.dimension
        return [y, x]
        
