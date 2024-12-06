from .board import MinesweepBoard

class MinesweepGame:
    def __init__(self):
        try:
            board_file = open('board', 'rb')
            first_bytes = int.from_bytes(board_file.read(2))
            board_dimension = first_bytes >> 2
            game_status = first_bytes & 3
            data = board_file.read()
            board_file.close()
            self.gameboard = MinesweepBoard(board_dimension, board_dimension)
            y = 0
            x = 0
            for i in range(len(data)):
                byte = data[i]
                
                first = byte >> 4
                second = byte & 15

                if x >= board_dimension:
                    y += 1
                    x = 0
                self.gameboard.set_value(y, x, first)
                x += 1

                if second == 15:
                    continue

                if x >= board_dimension:
                    y += 1
                    x = 0
                self.gameboard.set_value(y, x, second)
                x += 1

            if game_status == 1:
                self.game_running = False; self.victory = False
            elif game_status == 2:
                self.game_running = False; self.victory = True
            else:
                self.game_running = True; self.victory = False
            self.votes = {}

        except FileNotFoundError:
            self.reset_board(3,3 )

    def reset_board(self, y, x):
        self.gameboard = MinesweepBoard(y, x)
        self.gameboard.create_mines()
        self.game_running = True
        self.victory = False
        self.votes = {}
        self.save_board('board')
        self.save_online_board('current_board')

    def validate_vote(self, y, x):
        try:
            y = int(y)
            x = int(x)
        except ValueError:
            return False

        if self.gameboard.out_of_bounds(y, x):
            return False
            
        return True

    def vote(self, y, x, ip):
        if not self.game_running:
            return None
        if not self.gameboard.is_explored(y, x):
            self.votes[ip] = self.gameboard.yx_to_number(y, x)

    def play_turn(self):

        if not self.game_running:
            if not self.victory:
                self.reset_board(self.gameboard.y, self.gameboard.x)
            else:
                self.reset_board(self.gameboard.y+1, self.gameboard.x+1)
            return None

        votes_by_yx = {}
        for ip_address in self.votes:
            yx_number = self.votes[ip_address]
            votes_by_yx[yx_number] = votes_by_yx.get(yx_number, 0) + 1

        votes_sorted = dict(sorted(votes_by_yx.items(), key=lambda item: -item[1]))

        explore_amount = self.gameboard.x
        for yx_number in votes_sorted:
            if explore_amount > 0:
                yx = self.gameboard.number_to_yx(yx_number)
                y = yx[0]
                x = yx[1]
                self.gameboard.explore(y,x)
                explore_amount -= 1

        if self.gameboard.mine_hit():
            self.game_running = False
            self.victory = False

        self.save_board('board')
        self.save_online_board('current_board')

    # rightmost bits 0-1: game status:
    # 0 = game running
    # 1 = game stopped, loss
    # 2 = game stopped, victory
    # leftbits 3-15:
    # size of current board (number 3 representing 3x3 board, max 2^14
    # This is in total 2 bytes.
    #
    # Board tiles:
    # 0-8 = explored, not mine
    # 9 = not explored
    # 10 = mine, not explored
    # 11 = mine, explored
    # 15 skip
    # This is: half byte - add 2 tiles together for a byte

    def save_board(self, filename):
        board_file = open(filename, 'wb')
        first_bytes = 0
        game_status = 0
        if self.game_running == False:
            if self.victory == False:
                game_status = 1
            else: game_status = 2
        first_bytes = self.gameboard.x
        first_bytes = first_bytes << 2
        first_bytes = first_bytes + game_status
        
        board_file.write(first_bytes.to_bytes(2))

        byte_half = 0
        for y in range(self.gameboard.y):
            for x in range(self.gameboard.x):
                if byte_half != 0:
                    byte_half = byte_half << 4
                    byte = byte_half + self.gameboard.board[y][x]
                    byte_half = 0
                    board_file.write(byte.to_bytes(1))

                else:
                    byte_half = self.gameboard.board[y][x]
                    if (y == self.gameboard.y-1 and x == self.gameboard.x-1):
                        byte = byte_half << 4
                        byte = byte + 15
                        board_file.write(byte.to_bytes(1))

        board_file.close()


    def save_online_board(self, filename):
        board_file = open(filename, 'wb')
        first_bytes = 0
        game_status = 0
        if self.game_running == False:
            if self.victory == False:
                game_status = 1
            else: game_status = 2
        first_bytes = self.gameboard.x
        first_bytes = first_bytes << 2
        first_bytes = first_bytes + game_status
        
        board_file.write(first_bytes.to_bytes(2))

        byte_half = 0
        for y in range(self.gameboard.y):
            for x in range(self.gameboard.x):
                tile = self.gameboard.board[y][x]
                if self.game_running == True:
                    if tile == 10: tile = 9

                if byte_half == 0:
                    byte_half = tile
                    if (y == self.gameboard.y-1 and x == self.gameboard.x-1):
                        byte = byte_half << 4
                        byte = byte + 15
                        board_file.write(byte.to_bytes(1))
                else:
                    byte_half = byte_half << 4
                    byte = byte_half + tile
                    byte_half = 0
                    board_file.write(byte.to_bytes(1))

        board_file.close()

