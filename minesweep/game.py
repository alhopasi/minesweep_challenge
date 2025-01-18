from .board import MinesweepBoard
import math
import random

class GameStatus:
    RUNNING = 0
    LOSS = 1
    VICTORY = 2

class MinesweepGame:
    def __init__(self):
        try:
            with open('board', 'rb') as board_file:
                first_bytes = int.from_bytes(board_file.read(2), 'big')
                board_dimension = first_bytes >> 2
                game_status = first_bytes & 3
                data = board_file.read()

            self.gameboard = MinesweepBoard(board_dimension)
            self.set_board_data(data, board_dimension)
            self.game_running, self.victory = self.get_game_status(game_status)
            self.votes = {}

        except FileNotFoundError:
            self.gameboard = None
            self.reset_game(3)
        
        self.send_data = False

    def set_board_data(self, data, board_dimension):
        y, x = 0, 0
        for byte in data:
            first_half = byte >> 4
            second_half = byte & 15

            self.gameboard.set_tile_value(y, x, first_half)
            x = (x + 1) % board_dimension
            if x == 0:
                y += 1

            if second_half != 15:
                self.gameboard.set_tile_value(y, x, second_half)
                x = (x + 1) % board_dimension
                if x == 0:
                    y += 1

    def get_game_status(self, status_code):
        if status_code == GameStatus.RUNNING:
            return True, False
        elif status_code == GameStatus.LOSS:
            return False, False
        elif status_code == GameStatus.VICTORY:
            return False, True

    def reset_game(self, board_dimension):
        if self.gameboard is None:
            self.gameboard = MinesweepBoard(3)
        else:
            self.gameboard.reset_board(board_dimension)
        self.gameboard.create_mines()
        self.game_running, self.victory = True, False
        self.votes = {}

    def validate_vote(self, y, x):
        try:
            y, x = int(y), int(x)
        except ValueError:
            return False

        if self.gameboard.in_bounds(y, x) and not self.gameboard.is_explored(y, x):
            return True

        return False

    def vote(self, y, x, ip):
        if not self.game_running:
            return None
        if not self.gameboard.is_explored(y, x):
            self.votes[ip] = self.gameboard.coords_to_index(y, x)

    def sort_by_votes(self, votes_by_index):
        votes_initial_sort = sorted(votes_by_index.items(), key=lambda item: -item[1])

        final_votes_sorted = []

        indexes_with_same_vote_amount = []
        previous_vote_amount = None

        for index, vote_amount in votes_initial_sort:
            if vote_amount != previous_vote_amount:
                random.shuffle(indexes_with_same_vote_amount)
                final_votes_sorted.extend(indexes_with_same_vote_amount)
                indexes_with_same_vote_amount = []
                previous_vote_amount = vote_amount
            else:
                indexes_with_same_vote_amount.append(index)

        random.shuffle(indexes_with_same_vote_amount)
        final_votes_sorted.extend(indexes_with_same_vote_amount)

        return dict(final_votes_sorted)

    def play_turn(self):
        if not self.game_running:
            self.reset_game(self.gameboard.dimension + 1) if self.victory else self.reset_game(self.gameboard.dimension)
            self.send_data = True
            return None

        if not self.votes:
            return None
        
        votes_by_index = self.count_votes()
        votes_sorted = self.sort_by_votes(votes_by_index)
        self.votes = {}

        self.explore_votes(votes_sorted)

        if self.gameboard.check_mine_hit():
            self.game_running, self.victory = False, False
        
        if self.gameboard.check_victory():
            self.game_running, self.victory = False, True
        
        self.send_data = True

    def count_votes(self):
        votes_by_index = {}
        for ip_address in self.votes:
            index = self.votes[ip_address]
            votes_by_index[index] = votes_by_index.get(index, 0) + 1
        return votes_by_index

    def explore_votes(self, votes):
        explore_amount = self.gameboard.dimension
        for yx_number in votes:
            if explore_amount > 0:
                y, x = self.gameboard.index_to_coords(yx_number)
                self.gameboard.explore(y,x)
                explore_amount -= 1
    
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
    # This is: half byte (4 bits) - add 2 tiles together for a byte

    def online_data(self):
        return self.create_board_bytes(save_online=True)

    def save_board(self, filename):
        bytes_to_save = self.create_board_bytes()
        with open(filename, 'wb') as board_file:
            board_file.write(bytes_to_save)

    def save_online_board(self, filename):
        bytes_to_save = self.create_board_bytes(save_online=True)
        with open(filename, 'wb') as board_file:
            board_file.write(bytes_to_save)

    def create_board_bytes(self, save_online=False):
        first_bytes = (self.gameboard.dimension << 2) + (GameStatus.RUNNING if self.game_running else GameStatus.VICTORY if self.victory else GameStatus.LOSS)
        byte_1 = first_bytes >> 8
        byte_2 = first_bytes & 255

        bytes_to_save = bytearray(2 + math.ceil(self.gameboard.dimension * self.gameboard.dimension / 2))
        bytes_to_save[0] = byte_1
        bytes_to_save[1] = byte_2

        i, first_byte, byte_half = 2, True, 0
        for y in range(self.gameboard.dimension):
            for x in range(self.gameboard.dimension):
                tile = self.gameboard.board[y][x]
                if self.game_running and save_online and tile == 10:
                    tile = 9

                if first_byte:
                    byte_half = tile << 4
                    first_byte = False
                    if (y == self.gameboard.dimension-1 and x == self.gameboard.dimension-1):
                        byte = byte_half + 15
                        bytes_to_save[i] = byte
                else:
                    byte = byte_half + tile
                    bytes_to_save[i] = byte
                    i += 1
                    first_byte = True
        return bytes_to_save