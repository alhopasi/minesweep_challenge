import random

class MinesweepBoard:
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.board = [ [9]*x for i in range(y) ]

    def create_mines(self):
        self.mines = round(self.y * self.x * random.uniform(0.15, 0.21))

        for i in range(self.mines):
            while True:
                mine_y = random.randint(0,self.y-1)
                mine_x = random.randint(0,self.x-1)
                if self.board[mine_y][mine_x] != 10:
                    self.board[mine_y][mine_x] = 10
                break

    def set_value(self, y, x, value):
        self.board[y][x] = value

    def is_explored(self, y, x):
        return not (self.board[y][x] == 9 or self.board[y][x] == 10)
    
    def explore(self, y, x):
        if self.is_explored(y, x):
            return None
        
        explored_tile = self.board[y][x]

        if explored_tile == 10:
            self.board[y][x] = 11
            return None
        
        mines = self.mines_close(y, x)

        self.board[y][x] = mines

        if mines == 0:
            for y_ in range(-1,2):
                for x_ in range(-1,2):
                    if self.out_of_bounds(y + y_, x + x_):
                        continue
                    self.explore(y + y_, x + x_)
    
    def out_of_bounds(self, y, x):
        return (y < 0 or y >= self.y or x < 0 or x >= self.x)

    def mines_close(self, y, x):
        mines = 0
        for y_ in range(-1,2):
            for x_ in range(-1,2):
                check_y = y + y_
                check_x = x + x_
                if self.out_of_bounds(check_y, check_x):
                    continue
                if (self.board[check_y][check_x] == 10 or self.board[check_y][check_x] == 11):
                    mines += 1
        return mines
    
    def check_mine_hit(self):
        for y in range(self.y):
            for x in range(self.x):
                if self.board[y][x] == 11: return True
        return False

    def yx_to_number(self, y, x):
        return y * self.y + x
    
    def number_to_yx(self, number):
        y = int(number / self.y)
        x = number - (y * self.y)
        return [y, x]
        
