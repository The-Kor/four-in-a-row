from copy import deepcopy
import random


class AI:
    """
    This class is responsible of calculating the best possible move for a player in a certain game situation.
    """
    def __init__(self, game, player):
        """
        This class gets game Game instance and a player (1 or 2).
        :param game: Game instance
        :param player: 1 / 2
        """
        self.__player = player
        self.__players = [1, 2]
        self.__game = game
        self.__learning_depth = 2
        self.__BOARD_WIDTH = 7
        self.__BOARD_HEIGHT = 6
        self.__current_moves_score = [0]*self.__BOARD_WIDTH
        self.__current_best_move = random.randint(0,6)

    def __is_board_full(self, game):
        """
        This function checks if the board in the given game instance is full.
        The function relies that the get_player_at function will return None for empty cell in the board.
        :param game: Game instance
        :return: True if full, False if not
        """
        board_data = []
        for c in range(self.__BOARD_WIDTH):
            for r in range(self.__BOARD_HEIGHT):
                board_data.append(game.get_player_at(r, c))
        if all(b not in self.__players for b in board_data):
            return True
        return False

    def __calculate_moves_score(self, game=None, current_player=None, depth=None):
        """
        This function is calculating a score for every possible move in the game using recursion.
        Ths function will simulate every possible moves of the current player and every possible move of the
        second player and will check the what did the move cause ( win to the desired player or loss).
        The moves are being simulated by creating a game instance copy which does not affect the given game instance.
        The recursion has a base case = depth value- which is the number of moves ahead that the function will
        calculate.
        The function will add 1 to the score if the user won in this move, and will decrease the score by 1
        if the user lost in this move.
        The function updates a list of the current moves scores in the instance and the current best move
        (the move with the best score).

        :param game: Game instance
        :param current_player: 1 or 2
        :param depth: int (How many moves ahead the function will calculate)
        :return: The moves scores
        """
        if not game:
            game = self.__game
        if not current_player:
            current_player = self.__player
        moves_score = [0] * self.__BOARD_WIDTH
        if depth is None:
            depth = self.__learning_depth
        if depth == 0 or self.__is_board_full(game):
            return moves_score
        enemy_player = [p for p in self.__players if p != current_player][0]
        for m in range(self.__BOARD_WIDTH):
            game_copy = deepcopy(game)
            try:
                game_copy.make_move(m)
                move_result = game_copy.get_winner()
                if move_result == current_player:
                    moves_score[m] += 1
                    break
                else:
                    if move_result == 0:
                        moves_score[m] = 0
                    else:
                        for enemy_m in range(self.__BOARD_WIDTH):
                            game_copy_2 = deepcopy(game_copy)
                            try:
                                game_copy_2.make_move(enemy_m)
                                enemy_move_result = game_copy_2.get_winner()
                                if enemy_move_result == enemy_player:
                                    moves_score[m] -= 1
                                    break
                                else:
                                    score_result = self.__calculate_moves_score(game=game_copy_2,
                                                                                current_player=current_player,
                                                                                depth=depth-1)
                                    # Adding the average score that this move got in the next game loop ( average of all
                                    # the move's score's that were applied after that combination of moves were applied.

                                    moves_score[m] += (sum(score_result) / self.__BOARD_WIDTH) / self.__BOARD_WIDTH
                                    self.__current_moves_score = moves_score
                                    self.__current_best_move = self.__current_moves_score.index(
                                        max(self.__current_moves_score))
                            except BaseException:
                                continue
            except BaseException:
                continue
        return moves_score

    def find_legal_move(self):
        """
        This function calls calculate_moves_score to update the current_moves_score list in the instance.
        The function will loop over the scores that were updated and will try to return the legal move with the
        best score.
        If the no legal moves has the best score the function will return a random legal move.
        :return: The best possible move for the player that is given to the instance.
        """
        if self.__game.get_current_player() != self.__player:
            raise BaseException("Wrong Player")
        self.__calculate_moves_score()
        best_moves = []
        legal_moves = {}
        # Finding the legal moves
        for i, m in enumerate(self.__current_moves_score):
            if self.is_move_valid(i):
                legal_moves[i] = m
        best_move_score = max(legal_moves.values())
        # Finding the best legal moves
        for m in legal_moves.keys():
            if legal_moves[m] == best_move_score:
                best_moves.append(m)
        if best_moves:
            return random.choice(best_moves)
        else:
            raise BaseException("No possible AI moves")

    def is_move_valid(self, col):
        """
        This function gets a move (col index) and checks if the move is legal by checking that the first row
        in the column is empty (index - (0, col)).
        :param col: column index
        :return: True if the move is legal, False if not
        """
        try:
            # Checking the first row of the column
            value = self.__game.get_player_at(0, col)
            if value is None:
                return True
            return False
        # If the col that is given is not in the board
        except IndexError:
            return False

    def get_last_found_move(self):
        """
        :return:This function returns the best current move that is save in the instance arguments
        """
        return self.__current_best_move
