class Game:
    """
    This class defines a classic four in a row game with 2 players (1 and 2).
    The class has methods that are used to control the state of the game and the operations that
    a player can perform in a game.
    """
    def __init__(self):
        self.__players = [1, 2]
        self.__current_player = 1
        self.__BOARD_WIDTH = 7
        self.__BOARD_HEIGHT = 6
        self.__EMPTY_CELL = 0
        self.__winning_sequence_length = 4
        self.__current_board = self.__create_board()
        self.__win_sequences = self.__get_winner_sequences()
        self.__winner = None

    def __create_board(self):
        """
        This function creates list of lists with the empty cell value in every cell in the size of the
        board.
        :return: list of lists (The game board)
        """
        board = []
        for r in range(self.__BOARD_HEIGHT):
            board.append([self.__EMPTY_CELL]*self.__BOARD_WIDTH)
        return board

    def __get_move_coordinate(self, column):
        """
        This function gets a column and returns a tuple as follows :
        The latest row that is empty, the given column.
        If not empty row was find in that column, False will be returned
        :return: Tuple or False
        """
        if column in range(self.__BOARD_WIDTH):
            row_coordinates = [row for row in range(self.__BOARD_HEIGHT) if
                               self.__current_board[row][column] == self.__EMPTY_CELL]
            if row_coordinates:
                return max(row_coordinates), column
        return False

    def make_move(self, column):
        """
        This function gets a column index and insert to the cell that is found by get_move_coordinates
        the value of the current player, if the move was successfully made, the current player will be changes to the
        second player.
        :return: True upon successful move, Exception otherwise.
        """
        coordinate = self.__get_move_coordinate(column)
        if coordinate:
            if self.__current_board[coordinate[0]][coordinate[1]] == self.__EMPTY_CELL:
                self.__current_board[coordinate[0]][coordinate[1]] = self.__current_player
                # Changing the current player after the move was done
                self.__current_player = [player for player in self.__players if player !=
                                         self.__current_player][0]
                return True
        else:
            raise BaseException('Illegal move')

    def __get_winner_sequences(self):
        """
        This function returns a list of all possible winning sequences.
        :return: list of winning sequences
        """
        sequences = []
        for p in self.__players:
            sequences.append([p]*self.__winning_sequence_length)
        return sequences

    def __check_sequences(self, values_lists):
        """
        This function gets a list of values list and creates a sequences (in length of the winning sequences)
        list that are later checked if matched to the winning sequences.
        If a winning sequence was found, the first value of the sequence(which is the player that won) will be returned
        , else False will be returned.
        :return: Winner value if there is a winning sequence in the given values,
        False if no winning sequence was found
        """
        sequences = []
        for l in values_lists:
            for i, v in enumerate(l):
                if i <= (len(l) - self.__winning_sequence_length):
                    seq = [l[i+j] for j in range(self.__winning_sequence_length)]
                    sequences.append(seq)
        for w in self.__win_sequences:
            if w in sequences:
                return w[0]
        return False

    def __check_row_winner(self):
        """
        This function calls check_sequences with the board rows
        """
        return self.__check_sequences(self.__current_board)

    def __check_col_winner(self):
        """
        This function gets all of the columns data and calls check_sequences with the columns values.
        """
        col_values_lists = []
        for col in range(self.__BOARD_WIDTH):
            col_data = []
            for row in range(self.__BOARD_HEIGHT):
                col_data.append(self.__current_board[row][col])
            col_values_lists.append(col_data)
        return self.__check_sequences(col_values_lists)

    def __check_diagonal_winner(self):
        """
        This function finds all of the diagonal values in the board and calls check_sequences with the
        diagonal's data.
        """
        diagonals_values_lists = []
        diagonal_factor = 3
        # Finding both right diagonals and left diagonals.
        for c in range(self.__BOARD_WIDTH - diagonal_factor):
            for r in range(diagonal_factor, self.__BOARD_HEIGHT):
                diagonals_values_lists.append([self.__current_board[r][c], self.__current_board[r-1][c+1],
                                               self.__current_board[r-2][c+2], self.__current_board[r-3][c+3]])
        for c in range(self.__BOARD_WIDTH - diagonal_factor):
            for r in range(self.__BOARD_HEIGHT - diagonal_factor):
                diagonals_values_lists.append([self.__current_board[r][c], self.__current_board[r + 1][c + 1],
                                               self.__current_board[r + 2][c + 2],
                                               self.__current_board[r + 3][c + 3]])
        return self.__check_sequences(diagonals_values_lists)

    def get_winner(self):
        """
        This function checks for every possible winning situation and returns
        the value of the winner if the is one.
        0 will be returned if no winner was found and the board is full.
        None will be returned if no winner was found and the board is not full.
        """
        winner_checkers = [self.__check_row_winner(), self.__check_col_winner(),
                           self.__check_diagonal_winner()]
        if any(winner_checkers):
            self.__winner = [p for p in winner_checkers if p][0]
            return self.__winner
        if all(self.__EMPTY_CELL != v for row in self.__current_board for v in row):
            return 0
        return None

    def get_player_at(self, row, col):
        """
        This function gets row and column index;s and tries to return the value of the player that is in the
        given coordinates. (None for empty cell).
        """
        try:
            value = self.__current_board[row][col]
            if value == self.__EMPTY_CELL:
                return None
            return value
        except Exception:
            raise Exception("Illegal location")

    def get_current_player(self):
        """
        This function returns the current player to play.
        """
        return self.__current_player
