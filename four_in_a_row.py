import tkinter as tk
from game import Game
from ai import AI
from time import sleep
from os import path


class GUI:
    """
        This class is responsible of the graphic representation of the game
        to the user.
        """

    def __init__(self, parent):
        """
                   This class gets a parent - TK instance that will contain
                   all the graphic components of the game.
                   :param parent: parent
                   """
        self.__parent = parent
        self.game = Game()
        self.__COL_SIZE = 7
        self.__ROW_SIZE = 6
        self.board = {}
        self.__game_over = False

        # Initializing Images
        self.__data_folder = 'images'
        self.__draw_img = tk.PhotoImage(file=path.join(self.__data_folder, "draw.gif"))
        self.__play_again_img = tk.PhotoImage(file=path.join(self.__data_folder, "play_again.gif"))
        self.__exit_img = tk.PhotoImage(file=path.join(self.__data_folder, "exit.gif"))
        self.__play_img = tk.PhotoImage(file=path.join(self.__data_folder, "play.gif"))
        self.__empty_disk_img = tk.PhotoImage(file=path.join(self.__data_folder, "colorwhite1.gif"))
        self.__player_one_img = tk.PhotoImage(file=path.join(self.__data_folder, "player1.gif"))
        self.__player_two_img = tk.PhotoImage(file=path.join(self.__data_folder, "player2.gif"))
        self.__arrow = tk.PhotoImage(file=path.join(self.__data_folder, "arrow3.gif"))
        self.__winner = tk.PhotoImage(file=path.join(self.__data_folder, "winner.gif"))

        self.__players = {1: None, 2: None}

        # Initializing window settings
        self.__disk_dict = {0: self.__empty_disk_img, 1: self.__player_one_img, 2: self.__player_two_img}
        self.__screen_width = self.__parent.winfo_screenwidth()
        self.__screen_height = self.__parent.winfo_screenheight()
        self.__top_menu_width = 650
        self.__top_menu_height = 120
        self.__win_window = None
        self.__win_window_width = 300
        self.__win_window_height = 300
        self.__top_menu = None
        self.__top_menu_labels = {1: None, 2: None}
        self.__board_menu_width = 650
        self.__board_menu_height = 650
        self.__game_is_running = False
        self.__parent.geometry('{}x{}+{}+{}'.format(self.__board_menu_width, self.__board_menu_height,
                                                    int(self.__screen_width / 2 - self.__board_menu_width / 2),
                                                    int(self.__screen_height / 2 - self.__board_menu_height / 2)))
        self.__current_player_msg = tk.Label(self.__parent)
        self.__buttons_frame = tk.Frame(self.__parent, height=200, width=100)
        self.__board_frame = tk.Frame(self.__parent, height=850, width=650, bg="white")
        self.__info_frame = tk.Frame(self.__parent, height=100, width=650)
        self.choose_players()
        self.__info_frame.pack()
        self.__parent.after(100, self.game_handler)
        self.__parent.mainloop()

    def create_board_gui(self):
        """
        This function creates the initialized board's graphics.
        """
        self.__buttons_frame.pack()
        self.__board_frame.pack()
        self.create_buttons()
        self.initialize_board()

    def update_info(self, player):
        """
                This function updates the information on the board on every turn
                presenting which player is currently playing.
                :param player: representing the current player 1 or 2

                """
        for w in self.__info_frame.winfo_children():
            w.destroy()
        tk.Label(self.__info_frame, text='Current Player is'.format(player)).pack()
        tk.Label(self.__info_frame, image=self.__disk_dict[player]).pack()

    def create_buttons(self):
        """
                This function creates the buttons that are used for picking
                the column in which the players wants to locate their disk.
                """
        for c in range(7):
            tk.Button(self.__buttons_frame, image=self.__arrow,
                      command=lambda x=c: self.button_command(x)).grid(row=1, column=c, padx=17)

    def button_command(self, col):
        """
                This function gets a move (col index). it checks if the player
                is human and if so, locates the player's disk in the correct
                location by calling the "make_move" function from class Game.
                :param col: column index
                :return: True if the player is human and the move was made,
                None if not
                """
        current_player = self.game.get_current_player()
        if self.__players[current_player] is False and self.__game_is_running:
            return self.__make_move(col)
        else:
            return None

    def initialize_board(self):
        """
        This function creates the initialized board's graphics.
        it locates empty disks according to the board's measurements:
        6x7. it also inserts the board dictionary every coordinate on
        the board as a key and an empty disk and None as every coordinate's
        values.
        """
        for r in range(6):
            for c in range(7):
                label_disk = tk.Label(self.__board_frame, image=self.__disk_dict[0])
                label_disk.grid(row=r, column=c)
                self.board[(r, c)] = (label_disk, None)

    def __make_move(self, col):
        """
        This function gets a move (col index). it tries to make a move by
        calling the function "make move" from the class Game.
        if it succeeds, the function locates the disk of the current player
        in the right coordinate in chosen column and updates the board
        dictionary with the correct disk and player matching the coordinate.
        :param col: column index
        """
        try:
            self.game.make_move(col)
        except Exception:
            return
        for r in range(6):
            new_value = self.game.get_player_at(r, col)
            if new_value != self.board[(r, col)][1]:
                label_disk = tk.Label(self.__board_frame, image=self.__disk_dict[new_value])
                self.board[(r, col)] = (label_disk, new_value)
                self.board[(r, col)][0].grid(row=r, column=col)

    def set_players(self, player, ai):
        """
       This function is responsible for setting the players of the game
       according to the user's choice of player's type : ai or human.
       it presents the number of the player and the player's type that was
       chosen by the user.
       :param player: 1 or 2
       :param ai: True if the user chose ai or False if the user chose human

       """
        self.__players[player] = ai
        if player == 1:
            if self.__top_menu_labels[1]:
                self.__top_menu_labels[1].destroy()
            if ai:
                self.__top_menu_labels[1] = tk.Label(self.__info_frame, text='Player 1 is AI')
            else:
                self.__top_menu_labels[1] = tk.Label(self.__info_frame, text='Player 1 is Human')
            self.__top_menu_labels[1].place(x=100, y=75)
            return

        else:
            if self.__top_menu_labels[2]:
                self.__top_menu_labels[2].destroy()
            if ai:
                self.__top_menu_labels[2] = tk.Label(self.__info_frame, text='Player 2 is AI')
            else:
                self.__top_menu_labels[2] = tk.Label(self.__info_frame, text='Player 2 is Human')
            self.__top_menu_labels[2].place(x=450, y=75)
            return

    def call_play(self):
        """
       This function is responsible for starting a new game.
       after the user chooses the player's types, the function creates a Game
       instance and creates a gui for the board. if the user didn't choose a
       type, the function asks him to do so.
       """
        if None in self.__players.values():
            request_player_input = tk.Label(self.__info_frame, text='Please select players!')
            request_player_input.place(x=260, y=70)
            return
        self.__game_is_running = True
        if self.game.get_winner() is not None:
            self.game = Game()
        self.create_board_gui()
        return

    def choose_players(self):
        """
         This function creates the graphic interface in which the user
         chooses the type of player: ai or human. in order to set the
         players of the game the user needs to press the button
         representing the desired type. when pressing the button, the
         function calls the "set players" function and sets the players
         of the game with the types that were chosen by the user.
         """
        for w in self.__info_frame.winfo_children():
            w.destroy()
        tk.Label(self.__info_frame, image=self.__player_one_img).place(x=0, y=0)
        tk.Label(self.__info_frame, image=self.__player_two_img).place(x=575, y=0)
        tk.Button(self.__info_frame, text='Human', command=lambda p=1, ai=False:
        self.set_players(p, ai)).place(x=100, y=0)
        tk.Button(self.__info_frame, text='AI', command=lambda p=1, ai=True: self.set_players(p, ai)).place(x=110, y=40)
        tk.Button(self.__info_frame, text='Human', command=lambda p=2, ai=False: self.set_players(p, ai)).place(x=500,
                                                                                                                y=0)
        tk.Button(self.__info_frame, text='AI', command=lambda p=2, ai=True: self.set_players(p, ai)).place(x=510, y=40)
        tk.Button(self.__info_frame, image=self.__play_img, command=self.call_play,
                  highlightthickness=0, bd=0).place(x=285, y=0)
        # Setting players information if players were selected before.
        if all(v is not None for v in self.__players.values()):
            for p in self.__players:
                self.set_players(p, self.__players[p])

    def win_state(self, winner):
        """
         This function creates the graphic interface for a winning state.
         it presents the winning player, a winning massage and asks the user
         if they want to play again.
         by pressing the "exit" button it closes the window, by pressing play
         again it calls the function "choose players" to initialize a new game.
         :param winner: the winning player, 1 or 2
         """
        for w in self.__info_frame.winfo_children():
            w.destroy()
        self.__info_frame = tk.Frame(self.__info_frame, height=100, width=650)
        self.__info_frame.pack()
        if winner == 0:
            tk.Label(self.__info_frame, text='DRAW!').place(x=245, y=0)
            tk.Label(self.__info_frame, image=self.__draw_img).place(x=285, y=0)
            tk.Label(self.__info_frame, text='DRAW!').place(x=375, y=0)
            tk.Label(self.__info_frame, image=self.__disk_dict[1]).place(x=150, y=0)
            tk.Label(self.__info_frame, image=self.__disk_dict[2]).place(x=425, y=0)
        else:
            tk.Label(self.__info_frame, text='WINNER!').place(x=250, y=0)
            tk.Label(self.__info_frame, image=self.__winner).place(x=300, y=0)
            tk.Label(self.__info_frame, text='WINNER!').place(x=350, y=0)
            tk.Label(self.__info_frame, image=self.__disk_dict[winner]).place(x=150, y=0)
            tk.Label(self.__info_frame, image=self.__disk_dict[winner]).place(x=425, y=0)
        tk.Button(self.__info_frame, image=self.__play_again_img, command=self.choose_players,
                  highlightthickness=0, bd=0).place(x=20, y=0)
        tk.Button(self.__info_frame, image=self.__exit_img, command=self.__parent.destroy,
                  highlightthickness=0, bd=0).place(x=550, y=0)

    def game_handler(self):
        """
       This function controls the game. if the game is running and there is
       no winner yet, checks if the player is ai or human. if the player is ai
       it preforms the ai move by calling the functions "find legal move" from
       the AI class and the "make move" function from the Game class.
       if there is a winner' the function presents the winner by calling the
       "win state" function.
       """
        if self.__game_is_running:
            state = self.game.get_winner()
            current_player = self.game.get_current_player()
            self.update_info(current_player)
            if state is not None:
                self.__game_is_running = False
                self.win_state(state)
            else:
                tk.Label(self.__info_frame, text='Player {} turn!'.format(current_player)).place(x=350, y=0)
                if self.__players[current_player]:
                    comp = AI(self.game, current_player)
                    try:
                        chosen_move = comp.find_legal_move()
                        # Sleeping for 0.5 second before making the computer move
                        sleep(0.5)
                        self.__make_move(chosen_move)
                    # If exception is returned - The game is finished, using pass for moving to move forward
                    # (The finished game situation will be managed by the next call of game_handler)
                    except Exception:
                        pass
        self.__parent.after(100, self.game_handler)


def main():
    root = tk.Tk()
    GUI(root)


if __name__ == '__main__':
    main()
