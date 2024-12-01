from .board import MinesweepBoard

class MinesweepGame:
    def __init__(self):
        try:
            board_file = open('board', 'rb')
            first_bytes = int.from_bytes(board_file.read(2))
            game_status = int(format(first_bytes, 'b')[-2:],2)
            board_dimension = first_bytes >> 2
            data = board_file.read()
            board_file.close()
            self.gameboard = MinesweepBoard(board_dimension, board_dimension)
            y = 0
            x = 0
            for i in range(len(data)):
                byte = data[i]
                if byte > 15:
                    first = byte >> 4
                    second = byte - 15
                    if x >= board_dimension:
                        y += 1
                        x = 0
                    if first != 15:
                        self.gameboard.set_value(y, x, first)
                        x += 1
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

        except FileNotFoundError:
            self.gameboard = MinesweepBoard(3,3)
            self.gameboard.create_mines()
            self.game_running = True
            self.victory = False
            self.save_board('board')
            self.save_online_board('current_board')


    def play_turn(self):
        # see saved list of votes - explore votes - see game end - save board
        # explore tiles -> see if game end
        self.save_board('board')
        self.save_online_board('current_board')

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
        byte = 0
        for y in range(self.gameboard.y):
            for x in range(self.gameboard.x):
                if byte == 0:
                    if (y == self.gameboard.y-1 and x == self.gameboard.x-1):
                        byte = 15
                        byte = byte << 4
                        byte = byte + self.gameboard.board[y][x]
                        board_file.write(byte.to_bytes(1))
                    else:    
                        byte = self.gameboard.board[y][x]
                else:
                    byte = byte << 4
                    byte = byte + self.gameboard.board[y][x]
                    board_file.write(byte.to_bytes(1))
                    byte = 0
        board_file.close()

    # bits 0-1: game status:
    # 0 = game running
    # 1 = game stopped, loss
    # 2 = game stopped, victory
    # bits 3-15:
    # size of current board (number 3 representing 3x3 board, max 2^14
    # This is 2 bytes.
    #
    # Board tiles:
    # 0-8 = explored, not mine
    # 9 = not explored
    # 10 = mine, not explored
    # 11 = mine, explored
    # 15 skip
    # This is: 1 byte (16 bits)
    # Min to write to file = 1 byte. Each byte represents a tile.


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
        for y in range(self.gameboard.y):
            for x in range(self.gameboard.x):
                tile = self.gameboard.board[y][x]
                if self.game_running == True:
                    if (tile == 10): tile == 9
                board_file.write(self.gameboard.board[y][x].to_bytes(1))
        board_file.close()

