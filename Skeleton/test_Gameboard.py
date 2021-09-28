import unittest
from Gameboard import Gameboard


class Test_TestGameboard(unittest.TestCase):
    def setUp(self):
        self.board = Gameboard()

    def tearDown(self):
        self.board = Gameboard()

    def test_set_player1_color(self):
        # checks the function that sets player 1's chosen color is working properly.
        self.board.set_player_1("red")
        self.assertEqual(self.board.player1, "red", "set_player_1 failed!")
        self.board.set_player_1("yellow")
        self.assertEqual(self.board.player1, "yellow", "set_player_1 failed!")

    def test_set_player2_color(self):
        # checks the function that sets player 2's chosen color is working properly.
        self.board.set_player_2("red")
        self.assertEqual(self.board.player2, "red", "set_player_2 failed!")
        self.board.set_player_2("yellow")
        self.assertEqual(self.board.player2, "yellow", "set_player_2 failed!")

    def test_change_turn(self):
        # checks change_turn() function is working properly, changing game's current turn.
        self.board.change_turn()
        self.assertEqual(self.board.current_turn, 'p2', "change_turn failed!")
        self.board.change_turn()
        self.assertEqual(self.board.current_turn, 'p1', "change_turn failed!")

    def test_set_game_result(self):
        # checks set_game_result() function is working properly, setting the game result as desired.
        self.board.set_game_result("p1")
        self.assertEqual(self.board.game_result, "p1", "set_game_result failed!")
        self.board.set_game_result("p2")
        self.assertEqual(self.board.game_result, "p2", "set_game_result failed!")

    def test_decrease_remaining_moves(self):
        # checks decrease_remaining_moves() function is working properly, decreasing the remaining moves by 1 and does nothing when the remaining is 0
        self.board.decrease_remaining_moves()
        self.assertEqual(self.board.remaining_moves, 41, "decrease_remaining_moves failed!")

        for times in range(1, 10):
            self.board.decrease_remaining_moves()
            self.assertEqual(self.board.remaining_moves, 41 - times, "decrease_remaining_moves failed!")
        self.board.remaining_moves = 0
        self.board.decrease_remaining_moves()
        self.assertEqual(self.board.remaining_moves, 0, "decrease_remaining_moves failed!")

    def test_making_valid_move(self):
        # checks if the gammboard could make a move when given position is valid.
        self.board.set_player_1("red")
        self.board.set_player_2("yellow")

        # before actual moving, first test the move validation function
        move_validation_result = self.board.verify_game_status_and_move(1, 'p1')
        self.assertEqual(move_validation_result, "VALID", "verify_game_status_and_move failed!")
        # actual making that move, check the gameboard result and determine_winner function
        self.board.move(1, self.board.player1)
        self.board.determine_winner()
        self.assertEqual(self.board.board[5][0], "red", "game board did not update after moving!")
        self.assertEqual(self.board.game_result, "", "determine_winner failed!")

        # do the same test with player2
        self.board.change_turn()
        self.assertEqual(self.board.current_turn, 'p2', "change_turn failed!")

        move_validation_result = self.board.verify_game_status_and_move(1, 'p2')
        self.assertEqual(move_validation_result, "VALID", "verify_game_status_and_move failed!")

        self.board.move(1, self.board.player2)
        self.board.determine_winner()
        self.assertEqual(self.board.board[4][0], "yellow", "game board did not update after moving!")
        self.assertEqual(self.board.game_result, "", "determine_winner failed!")

    def test_invalid_move_not_current_turn(self):
        # checks a move to be invalid when the player tries to make a move on the other's turn.
        self.board.set_player_1("red")
        self.board.set_player_2("yellow")

        move_validation_result = self.board.verify_game_status_and_move(1, 'p2')
        self.assertEqual(move_validation_result, "NOT_YOUR_TURN_p2", "verify_game_status_and_move failed when determining invalid move: not your trun!")
        self.assertEqual(self.board.board[5][0], 0, "make the move when that move is determined invalid")

        move_validation_result = self.board.verify_game_status_and_move(1, 'p1')
        self.assertEqual(move_validation_result, "VALID", "verify_game_status_and_move failed when determining invalid move: not your trun!")
        self.board.move(1, self.board.player1)
        self.assertEqual(self.board.board[5][0], "red", " not make the move when that move is determined valid")

        self.board.change_turn()
        move_validation_result = self.board.verify_game_status_and_move(1, 'p1')
        self.assertEqual(move_validation_result, "NOT_YOUR_TURN_p1", "verify_game_status_and_move failed when determining invalid move: not your trun!")
        self.assertEqual(self.board.board[4][0], 0, "make the move when that move is determined invalid")

    def test_invalid_move_has_winner(self):
        # checks a move to be invalid when there is a game result
        self.board.set_player_1("red")
        self.board.set_player_2("yellow")

        # crearting player 1 winning condition
        self.board.move(1, self.board.player1)
        self.board.move(2, self.board.player1)
        self.board.move(3, self.board.player1)
        self.board.move(4, self.board.player1)

        self.board.determine_winner()
        self.assertEqual(self.board.game_result, "p1", "determine_winner failed!")
        move_validation_result = self.board.verify_game_status_and_move(1, 'p2')
        self.assertEqual(move_validation_result, "WINNER_P1", "fail to varify the game winner!")

        # creating player 2 winning condition
        self.board.board = [[0 for x in range(7)] for y in range(6)]
        self.board.move(1, self.board.player2)
        self.board.move(1, self.board.player2)
        self.board.move(1, self.board.player2)
        self.board.move(1, self.board.player2)

        self.board.determine_winner()
        self.assertEqual(self.board.game_result, "p2", "determine_winner failed!")
        move_validation_result = self.board.verify_game_status_and_move(1, 'p1')
        self.assertEqual(move_validation_result, "WINNER_P2", "fail to varify the game winner!")

    def test_invalid_move_column_filled(self):
        # checks a move to be invalid when that column is full
        self.board.set_player_1("red")
        self.board.set_player_2("yellow")

        # creating situation where column #2 is full
        self.board.move(2, self.board.player1)
        self.board.move(2, self.board.player2)
        self.board.move(2, self.board.player1)
        self.board.move(2, self.board.player2)
        self.board.move(2, self.board.player1)
        self.board.move(2, self.board.player2)

        # varification result will be "INVALID" if that column has been filled
        move_validation_result = self.board.verify_game_status_and_move(2, 'p1')
        self.assertEqual(move_validation_result, "INVALID", "fail to recogize a column is full!")

        move_validation_result = self.board.verify_game_status_and_move(1, 'p1')
        self.assertEqual(move_validation_result, "VALID", "fail to recogize a valid move!")

    def test_invalid_move_draw(self):
        # checks a move to be invalid when the game is draw
        self.board.set_player_1("red")
        self.board.set_player_2("yellow")
        self.board.remaining_moves = 0
        # create a draw board
        self.board.board = [["yellow", "yellow", "yellow", "red", "yellow", "yellow", "yellow"],
                            ["red", "red", "red", "yellow", "red", "red", "red"],
                            ["yellow", "yellow", "red", "red", "red", "yellow", "red"],
                            ["red", "red", "yellow", "yellow", "red", "red", "yellow"],
                            ["yellow", "yellow", "red", "red", "yellow", "yellow", "red"],
                            ["yellow", "yellow", "red", "red", "yellow", "red", "yellow"]]

        move_validation_result = self.board.verify_game_status_and_move(5, 'p1')
        self.assertEqual(move_validation_result, "DRAW", "fail to recogize a move is invalid when a draw happens!")
        self.board.change_turn()
        move_validation_result = self.board.verify_game_status_and_move(4, 'p2')
        self.assertEqual(move_validation_result, "DRAW", "fail to recogize a move is invalid when a draw happens!")

    def test_winning_move_horizontal(self):
        # checks a move to be valid and winning move in horizontal direction
        self.board.set_player_1("red")
        self.board.set_player_2("yellow")

        # create a board for player 1 to win from the right
        self.board.move(2, self.board.player1)
        self.board.move(3, self.board.player1)
        self.board.move(4, self.board.player1)

        move_validation_result = self.board.verify_game_status_and_move(5, 'p1')
        self.assertEqual(move_validation_result, "VALID", "fail to recogize a move is valid!")
        self.board.move(5, self.board.player1)
        self.board.determine_winner()
        self.assertEqual(self.board.game_result, "p1", "fail to determine winning move from the right!")

        self.board.board = [[0 for x in range(7)] for y in range(6)]
        self.board.game_result = ""  # reset game result
        self.board.set_player_1("yellow")
        self.board.set_player_2("red")

        # create a board for player 1 to win from the right
        self.board.move(2, self.board.player1)
        self.board.move(3, self.board.player1)
        self.board.move(4, self.board.player1)

        move_validation_result = self.board.verify_game_status_and_move(5, 'p1')
        self.assertEqual(move_validation_result, "VALID", "fail to recogize a move is valid!")
        self.board.move(5, self.board.player1)
        self.board.determine_winner()
        self.assertEqual(self.board.game_result, "p1", "fail to determine winning move from the right!")

        self.board.board = [[0 for x in range(7)] for y in range(6)]
        self.board.game_result = ""  # reset game result
        self.board.set_player_1("red")
        self.board.set_player_2("yellow")
        self.board.current_turn = 'p2'
        # create a board for player 1 to win from the right
        self.board.move(2, self.board.player2)
        self.board.move(3, self.board.player2)
        self.board.move(4, self.board.player2)

        move_validation_result = self.board.verify_game_status_and_move(5, 'p2')
        self.assertEqual(move_validation_result, "VALID", "fail to recogize a move is valid!")
        self.board.move(5, self.board.player2)
        self.board.determine_winner()
        self.assertEqual(self.board.game_result, "p2", "fail to determine winning move from the right!")

        self.board.board = [[0 for x in range(7)] for y in range(6)]
        self.board.game_result = ""  # reset game result
        self.board.set_player_1("yellow")
        self.board.set_player_2("red")
        self.board.current_turn = 'p2'

        # create a board for player 1 to win from the right
        self.board.move(2, self.board.player2)
        self.board.move(3, self.board.player2)
        self.board.move(4, self.board.player2)

        move_validation_result = self.board.verify_game_status_and_move(5, 'p2')
        self.assertEqual(move_validation_result, "VALID", "fail to recogize a move is valid!")
        self.board.move(5, self.board.player2)
        self.board.determine_winner()
        self.assertEqual(self.board.game_result, "p2", "fail to determine winning move from the right!")
        # create a board for player 2 to win from the left
        self.board.board = [[0 for x in range(7)] for y in range(6)]
        self.board.current_turn = 'p1'
        self.board.set_player_1("yellow")
        self.board.set_player_2("red")
        self.board.game_result = ""  # reset game result
        self.board.move(2, self.board.player1)
        self.board.move(3, self.board.player1)
        self.board.move(4, self.board.player1)

        move_validation_result = self.board.verify_game_status_and_move(1, 'p1')
        self.assertEqual(move_validation_result, "VALID", "fail to recogize a move is valid!")
        self.board.move(1, self.board.player1)
        self.board.determine_winner()
        self.assertEqual(self.board.game_result, "p1", "fail to determine winning move from the left!")

        self.board.board = [[0 for x in range(7)] for y in range(6)]
        self.board.current_turn = 'p1'
        self.board.set_player_1("red")
        self.board.set_player_2("yellow")
        self.board.game_result = ""  # reset game result
        self.board.move(2, self.board.player1)
        self.board.move(3, self.board.player1)
        self.board.move(4, self.board.player1)

        move_validation_result = self.board.verify_game_status_and_move(1, 'p1')
        self.assertEqual(move_validation_result, "VALID", "fail to recogize a move is valid!")
        self.board.move(1, self.board.player1)
        self.board.determine_winner()
        self.assertEqual(self.board.game_result, "p1", "fail to determine winning move from the left!")

        self.board.board = [[0 for x in range(7)] for y in range(6)]
        self.board.current_turn = 'p2'
        self.board.set_player_1("red")
        self.board.set_player_2("yellow")
        self.board.game_result = ""  # reset game result
        self.board.move(2, self.board.player2)
        self.board.move(3, self.board.player2)
        self.board.move(4, self.board.player2)

        move_validation_result = self.board.verify_game_status_and_move(1, 'p2')
        self.assertEqual(move_validation_result, "VALID", "fail to recogize a move is valid!")
        self.board.move(1, self.board.player2)
        self.board.determine_winner()
        self.assertEqual(self.board.game_result, "p2", "fail to determine winning move from the left!")

        self.board.board = [[0 for x in range(7)] for y in range(6)]
        self.board.current_turn = 'p2'
        self.board.set_player_1("yellow")
        self.board.set_player_2("red")
        self.board.game_result = ""  # reset game result
        self.board.move(2, self.board.player2)
        self.board.move(3, self.board.player2)
        self.board.move(4, self.board.player2)

        move_validation_result = self.board.verify_game_status_and_move(1, 'p2')
        self.assertEqual(move_validation_result, "VALID", "fail to recogize a move is valid!")
        self.board.move(1, self.board.player2)
        self.board.determine_winner()
        self.assertEqual(self.board.game_result, "p2", "fail to determine winning move from the left!")

    def test_winning_move_vertical(self):
        # checks a move to be valid and winning move in vertical direction
        self.board.set_player_1("red")
        self.board.set_player_2("yellow")

        # create a board for player 1 to win from the right
        self.board.move(3, self.board.player1)
        self.board.move(3, self.board.player1)
        self.board.move(3, self.board.player1)

        move_validation_result = self.board.verify_game_status_and_move(3, 'p1')
        self.assertEqual(move_validation_result, "VALID", "fail to recogize a move is valid!")
        self.board.move(3, self.board.player1)
        self.board.determine_winner()
        self.assertEqual(self.board.game_result, "p1", "fail to determine winning move from the top!")

        self.board.board = [[0 for x in range(7)] for y in range(6)]
        self.board.game_result = ""
        self.board.set_player_1("yellow")
        self.board.set_player_2("red")

        # create a board for player 1 to win from the right
        self.board.move(3, self.board.player1)
        self.board.move(3, self.board.player1)
        self.board.move(3, self.board.player1)

        move_validation_result = self.board.verify_game_status_and_move(3, 'p1')
        self.assertEqual(move_validation_result, "VALID", "fail to recogize a move is valid!")
        self.board.move(3, self.board.player1)
        self.board.determine_winner()
        self.assertEqual(self.board.game_result, "p1", "fail to determine winning move from the top!")

        self.board.board = [[0 for x in range(7)] for y in range(6)]
        self.board.game_result = ""
        self.board.current_turn = 'p2'
        self.board.set_player_1("red")
        self.board.set_player_2("yellow")

        # create a board for player 1 to win from the right
        self.board.move(3, self.board.player2)
        self.board.move(3, self.board.player2)
        self.board.move(3, self.board.player2)

        move_validation_result = self.board.verify_game_status_and_move(3, 'p2')
        self.assertEqual(move_validation_result, "VALID", "fail to recogize a move is valid!")
        self.board.move(3, self.board.player2)
        self.board.determine_winner()
        self.assertEqual(self.board.game_result, "p2", "fail to determine winning move from the top!")

        self.board.board = [[0 for x in range(7)] for y in range(6)]
        self.board.game_result = ""
        self.board.current_turn = 'p2'
        self.board.set_player_1("yellow")
        self.board.set_player_2("red")

        # create a board for player 1 to win from the right
        self.board.move(3, self.board.player2)
        self.board.move(3, self.board.player2)
        self.board.move(3, self.board.player2)

        move_validation_result = self.board.verify_game_status_and_move(3, 'p2')
        self.assertEqual(move_validation_result, "VALID", "fail to recogize a move is valid!")
        self.board.move(3, self.board.player2)
        self.board.determine_winner()
        self.assertEqual(self.board.game_result, "p2", "fail to determine winning move from the top!")

    def test_winning_move_positive_slope(self):
        # checks a move to be valid and winning move in positive slope direction
        self.board.set_player_1("red")
        self.board.set_player_2("yellow")

        # create a board for player 1 to win from the top right
        self.board.move(7, self.board.player2)
        self.board.move(7, self.board.player2)
        self.board.move(7, self.board.player2)
        self.board.move(6, self.board.player2)
        self.board.move(6, self.board.player2)
        self.board.move(6, self.board.player1)
        self.board.move(5, self.board.player2)
        self.board.move(5, self.board.player1)
        self.board.move(4, self.board.player1)

        move_validation_result = self.board.verify_game_status_and_move(7, 'p1')
        self.assertEqual(move_validation_result, "VALID", "fail to recogize a move is valid!")
        self.board.move(7, self.board.player1)
        self.board.determine_winner()

        self.assertEqual(self.board.game_result, "p1", "fail to determine winning move from the top right!")

        self.board.board = [[0 for x in range(7)] for y in range(6)]
        self.board.game_result = ""
        self.board.set_player_1("yellow")
        self.board.set_player_2("red")

        # create a board for player 1 to win from the top right
        self.board.move(7, self.board.player2)
        self.board.move(7, self.board.player2)
        self.board.move(7, self.board.player2)
        self.board.move(6, self.board.player2)
        self.board.move(6, self.board.player2)
        self.board.move(6, self.board.player1)
        self.board.move(5, self.board.player2)
        self.board.move(5, self.board.player1)
        self.board.move(4, self.board.player1)

        move_validation_result = self.board.verify_game_status_and_move(7, 'p1')
        self.assertEqual(move_validation_result, "VALID", "fail to recogize a move is valid!")
        self.board.move(7, self.board.player1)
        self.board.determine_winner()

        self.assertEqual(self.board.game_result, "p1", "fail to determine winning move from the top right!")

        self.board.board = [[0 for x in range(7)] for y in range(6)]
        self.board.game_result = ""
        self.board.current_turn = 'p2'
        self.board.set_player_1("red")
        self.board.set_player_2("yellow")

        # create a board for player 1 to win from the top right
        self.board.move(7, self.board.player1)
        self.board.move(7, self.board.player1)
        self.board.move(7, self.board.player1)
        self.board.move(6, self.board.player1)
        self.board.move(6, self.board.player1)
        self.board.move(6, self.board.player2)
        self.board.move(5, self.board.player1)
        self.board.move(5, self.board.player2)
        self.board.move(4, self.board.player2)

        move_validation_result = self.board.verify_game_status_and_move(7, 'p2')
        self.assertEqual(move_validation_result, "VALID", "fail to recogize a move is valid!")
        self.board.move(7, self.board.player2)
        self.board.determine_winner()

        self.assertEqual(self.board.game_result, "p2", "fail to determine winning move from the top right!")

        self.board.board = [[0 for x in range(7)] for y in range(6)]
        self.board.game_result = ""
        self.board.current_turn = 'p2'
        self.board.set_player_1("yellow")
        self.board.set_player_2("red")

        # create a board for player 1 to win from the top right
        self.board.move(7, self.board.player1)
        self.board.move(7, self.board.player1)
        self.board.move(7, self.board.player1)
        self.board.move(6, self.board.player1)
        self.board.move(6, self.board.player1)
        self.board.move(6, self.board.player2)
        self.board.move(5, self.board.player1)
        self.board.move(5, self.board.player2)
        self.board.move(4, self.board.player2)

        move_validation_result = self.board.verify_game_status_and_move(7, 'p2')
        self.assertEqual(move_validation_result, "VALID", "fail to recogize a move is valid!")
        self.board.move(7, self.board.player2)
        self.board.determine_winner()

        self.assertEqual(self.board.game_result, "p2", "fail to determine winning move from the top right!")

    def test_winning_move_negative_slope(self):
        # checks a move to be valid and winning move in negative slope direction
        self.board.set_player_1("red")
        self.board.set_player_2("yellow")
        self.board.change_turn()

        # create a board for player 2 to win from the top right
        self.board.move(1, self.board.player1)
        self.board.move(1, self.board.player1)
        self.board.move(1, self.board.player1)
        self.board.move(2, self.board.player1)
        self.board.move(2, self.board.player1)
        self.board.move(2, self.board.player2)
        self.board.move(3, self.board.player1)
        self.board.move(3, self.board.player2)
        self.board.move(4, self.board.player2)

        move_validation_result = self.board.verify_game_status_and_move(1, 'p2')
        self.assertEqual(move_validation_result, "VALID", "fail to recogize a move is valid!")
        self.board.move(1, self.board.player2)
        self.board.determine_winner()

        self.assertEqual(self.board.game_result, "p2", "fail to determine winning move from the top right!")

        self.board.board = [[0 for x in range(7)] for y in range(6)]
        self.board.game_result = ""
        self.board.set_player_1("yellow")
        self.board.set_player_2("red")

        # create a board for player 2 to win from the top right
        self.board.move(1, self.board.player1)
        self.board.move(1, self.board.player1)
        self.board.move(1, self.board.player1)
        self.board.move(2, self.board.player1)
        self.board.move(2, self.board.player1)
        self.board.move(2, self.board.player2)
        self.board.move(3, self.board.player1)
        self.board.move(3, self.board.player2)
        self.board.move(4, self.board.player2)

        move_validation_result = self.board.verify_game_status_and_move(1, 'p2')
        self.assertEqual(move_validation_result, "VALID", "fail to recogize a move is valid!")
        self.board.move(1, self.board.player2)
        self.board.determine_winner()

        self.assertEqual(self.board.game_result, "p2", "fail to determine winning move from the top right!")

        self.board.board = [[0 for x in range(7)] for y in range(6)]
        self.board.game_result = ""
        self.board.current_turn = 'p1'
        self.board.set_player_1("red")
        self.board.set_player_2("yellow")

        # create a board for player 2 to win from the top right
        self.board.move(1, self.board.player2)
        self.board.move(1, self.board.player2)
        self.board.move(1, self.board.player2)
        self.board.move(2, self.board.player2)
        self.board.move(2, self.board.player2)
        self.board.move(2, self.board.player1)
        self.board.move(3, self.board.player2)
        self.board.move(3, self.board.player1)
        self.board.move(4, self.board.player1)

        move_validation_result = self.board.verify_game_status_and_move(1, 'p1')
        self.assertEqual(move_validation_result, "VALID", "fail to recogize a move is valid!")
        self.board.move(1, self.board.player1)
        self.board.determine_winner()

        self.assertEqual(self.board.game_result, "p1", "fail to determine winning move from the top right!")

        self.board.board = [[0 for x in range(7)] for y in range(6)]
        self.board.game_result = ""
        self.board.current_turn = 'p1'
        self.board.set_player_1("yellow")
        self.board.set_player_2("red")

        # create a board for player 2 to win from the top right
        self.board.move(1, self.board.player2)
        self.board.move(1, self.board.player2)
        self.board.move(1, self.board.player2)
        self.board.move(2, self.board.player2)
        self.board.move(2, self.board.player2)
        self.board.move(2, self.board.player1)
        self.board.move(3, self.board.player2)
        self.board.move(3, self.board.player1)
        self.board.move(4, self.board.player1)

        move_validation_result = self.board.verify_game_status_and_move(1, 'p1')
        self.assertEqual(move_validation_result, "VALID", "fail to recogize a move is valid!")
        self.board.move(1, self.board.player1)
        self.board.determine_winner()

        self.assertEqual(self.board.game_result, "p1", "fail to determine winning move from the top right!")
