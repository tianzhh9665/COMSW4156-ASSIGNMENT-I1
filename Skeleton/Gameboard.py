import db

class Gameboard():
    def __init__(self):
        self.player1 = ""
        self.player2 = ""
        self.board = [[0 for x in range(7)] for y in range(6)]
        self.game_result = ""
        self.current_turn = 'p1'
        self.remaining_moves = 42

    def set_player_1(self,color):
        self.player1 = color

    def set_player_2(self,color):
        self.player2 = color

    def change_turn(self):
        if self.current_turn == 'p1':
            self.current_turn = 'p2'
        else:
            self.current_turn = 'p1'

    def set_game_result(self,result):
        self.game_result = result

    def decrease_remaining_moves(self):
        if(self.remaining_moves == 0):
            return
        else:
            self.remaining_moves = self.remaining_moves - 1

    def move(self,columnNumber, playerColor):
        for row in range(5,-1,-1):
            if self.board[row][columnNumber-1] == 0:
                self.board[row][columnNumber-1] = playerColor
                break
        

    
    def verify_game_status_and_move(self,columnNumber,movingPlayer):
        if self.player1 == "":
            return "NO_COLOR_P1"
        if self.player2 == "":
            return "NO_COLOR_P2"
        if self.game_result == "p1":
            return "WINNER_P1"
        if self.game_result == "p2":
            return "WINNER_P2"
        if self.game_result == "" and self.remaining_moves == 0:
            return "DRAW"
        
        if(movingPlayer != self.current_turn):
            return "NOT_YOUR_TURN_" + movingPlayer
        
        valid_move = False
        for row in range(5,-1,-1):
            if self.board[row][columnNumber-1] == 0:
                valid_move = True
                break
        
        if(valid_move == False):
            return "INVALID"
        


        return "VALID"
    

    def determine_winner(self):
        if self._check_horizontal() != "":
            self.game_result = self._check_horizontal()
        elif self._check_vertical() != "":
            self.game_result = self._check_vertical()
        elif self._check_diagonal() != "":
            self.game_result = self._check_diagonal()
        
    

    def _check_horizontal(self):
        if self._check_left() != "":
            if self._check_left() == "RED":
                if self.player1 == "red":
                    return "p1"
                else:
                    return "p2"
            else:
                if self.player1 == "yellow":
                    return "p1"
                else:
                    return "p2"
        elif self._check_right() != "":
            if self._check_right() == "RED":
                if self.player1 == "red":
                    return "p1"
                else:
                    return "p2"
            else:
                if self.player1 == "yellow":
                    return "p1"
                else:
                    return "p2"
        else:
            return ""

    def _check_vertical(self):
        if self._check_up() != "":
            if self._check_up() == "RED":
                if self.player1 == "red":
                    return "p1"
                else:
                    return "p2"
            else:
                if self.player1 == "yellow":
                    return "p1"
                else:
                    return "p2"
        elif self._check_down() != "":
            if self._check_down() == "RED":
                if self.player1 == "red":
                    return "p1"
                else:
                    return "p2"
            else:
                if self.player1 == "yellow":
                    return "p1"
                else:
                    return "p2"
        else:
            return ""


    def _check_up(self):
        for row in range(5,-1,-1):
            for col in range(6,-1,-1):
                red_count = 0
                yellow_count = 0

                if self.board[row][col] == 0:
                    continue
                elif self.board[row][col] == "red":
                    red_count += 1
                    for r in range(row-1,-1,-1):
                        if red_count == 4:
                            return "RED"
                        if self.board[r][col] == 0 or self.board[r][col] == "yellow":
                            break
                        if self.board[r][col] == "red":
                            red_count += 1
                else:
                    yellow_count += 1
                    for r in range(row-1,-1,-1):
                        if yellow_count == 4:
                            return "YELLOW"
                        if self.board[r][col] == 0 or self.board[r][col] == "red":
                            break
                        if self.board[r][col] == "yellow":
                            yellow_count += 1
        
        return ""

    def _check_down(self):
        for row in range(5,-1,-1):
            for col in range(6,-1,-1):
                red_count = 0
                yellow_count = 0

                if self.board[row][col] == 0:
                    continue
                elif self.board[row][col] == "red":
                    red_count += 1
                    for r in range(row+1,6,1):
                        if red_count == 4:
                            return "RED"
                        if self.board[r][col] == 0 or self.board[r][col] == "yellow":
                            break
                        if self.board[r][col] == "red":
                            red_count += 1
                else:
                    yellow_count += 1
                    for r in range(row+1,6,1):
                        if yellow_count == 4:
                            return "YELLOW"
                        if self.board[r][col] == 0 or self.board[r][col] == "red":
                            break
                        if self.board[r][col] == "yellow":
                            yellow_count += 1
        
        return ""

    def _check_diagonal(self):
        if self._check_up_left() != "":
            if self._check_up_left() == "RED":
                if self.player1 == "red":
                    return "p1"
                else:
                    return "p2"
            else:
                if self.player1 == "yellow":
                    return "p1"
                else:
                    return "p2"
        elif self._check_up_right() != "":
            if self._check_up_right() == "RED":
                if self.player1 == "red":
                    return "p1"
                else:
                    return "p2"
            else:
                if self.player1 == "yellow":
                    return "p1"
                else:
                    return "p2"
        elif self._check_down_left() != "":
            if self._check_down_left() == "RED":
                if self.player1 == "red":
                    return "p1"
                else:
                    return "p2"
            else:
                if self.player1 == "yellow":
                    return "p1"
                else:
                    return "p2"
        elif self._check_down_right() != "":
            if self._check_down_right() == "RED":
                if self.player1 == "red":
                    return "p1"
                else:
                    return "p2"
            else:
                if self.player1 == "yellow":
                    return "p1"
                else:
                    return "p2"
        else:
            return ""


    def _check_up_left(self):
        for row in range(5,-1,-1):
            for col in range(6,-1,-1):
                red_count = 0
                yellow_count = 0

                if self.board[row][col] == 0:
                    continue
                elif self.board[row][col] == "red":
                    red_count += 1
                    c = col - 1
                    r = row - 1
                    while (c >= 0 and r >= 0):
                        if red_count == 4:
                            return "RED"
                        if self.board[r][c] == 0 or self.board[r][c] == "yellow":
                            break
                        if self.board[r][c] == "red":
                            red_count += 1
                        c -= 1
                        r -= 1
                else:
                    yellow_count += 1
                    c = col - 1
                    r = row - 1
                    while (c >= 0 and r >= 0):
                        if yellow_count == 4:
                            return "YELLOW"
                        if self.board[r][c] == 0 or self.board[r][c] == "red":
                            break
                        if self.board[r][c] == "yellow":
                            yellow_count += 1
                        c -= 1
                        r -= 1
        return ""
    def _check_up_right(self):
        for row in range(5,-1,-1):
            for col in range(6,-1,-1):
                red_count = 0
                yellow_count = 0

                if self.board[row][col] == 0:
                    continue
                elif self.board[row][col] == "red":
                    red_count += 1
                    c = col + 1
                    r = row - 1
                    while (c <= 6 and r >= 0):
                        if red_count == 4:
                            return "RED"
                        if self.board[r][c] == 0 or self.board[r][c] == "yellow":
                            break
                        if self.board[r][c] == "red":
                            red_count += 1
                        c += 1
                        r -= 1
                else:
                    yellow_count += 1
                    c = col + 1
                    r = row - 1
                    while (c <= 6 and r >= 0):
                        if yellow_count == 4:
                            return "YELLOW"
                        if self.board[r][c] == 0 or self.board[r][c] == "red":
                            break
                        if self.board[r][c] == "yellow":
                            yellow_count += 1
                        c += 1
                        r -= 1
        return ""
    def _check_down_left(self):
        for row in range(5,-1,-1):
            for col in range(6,-1,-1):
                red_count = 0
                yellow_count = 0

                if self.board[row][col] == 0:
                    continue
                elif self.board[row][col] == "red":
                    red_count += 1
                    c = col - 1
                    r = row + 1
                    while (c >= 0 and r <= 5):
                        if red_count == 4:
                            return "RED"
                        if self.board[r][c] == 0 or self.board[r][c] == "yellow":
                            break
                        if self.board[r][c] == "red":
                            red_count += 1
                        c -= 1
                        r += 1
                else:
                    yellow_count += 1
                    c = col - 1
                    r = row + 1
                    while (c >= 0 and r <= 5):
                        if yellow_count == 4:
                            return "YELLOW"
                        if self.board[r][c] == 0 or self.board[r][c] == "red":
                            break
                        if self.board[r][c] == "yellow":
                            yellow_count += 1
                        c -= 1
                        r += 1
        return ""
    def _check_down_right(self):
        for row in range(5,-1,-1):
            for col in range(6,-1,-1):
                red_count = 0
                yellow_count = 0

                if self.board[row][col] == 0:
                    continue
                elif self.board[row][col] == "red":
                    red_count += 1
                    c = col + 1
                    r = row + 1
                    while (c <= 6 and r <= 5):
                        if red_count == 4:
                            return "RED"
                        if self.board[r][c] == 0 or self.board[r][c] == "yellow":
                            break
                        if self.board[r][c] == "red":
                            red_count += 1
                        c += 1
                        r += 1
                else:
                    yellow_count += 1
                    c = col + 1
                    r = row + 1
                    while (c <= 6 and r <= 5):
                        if yellow_count == 4:
                            return "YELLOW"
                        if self.board[r][c] == 0 or self.board[r][c] == "red":
                            break
                        if self.board[r][c] == "yellow":
                            yellow_count += 1
                        c += 1
                        r += 1
        return ""
    

    def _check_left(self):
        for row in range(5,-1,-1):
            for col in range(6,-1,-1):
                red_count = 0
                yellow_count = 0

                if self.board[row][col] == 0:
                    continue
                elif self.board[row][col] == "red":
                    red_count += 1
                    for c in range(col-1,-1,-1):
                        if red_count == 4:
                            return "RED"
                        if self.board[row][c] == 0 or self.board[row][c] == "yellow":
                            break
                        if self.board[row][c] == "red":
                            red_count += 1
                else:
                    yellow_count += 1
                    for c in range(col-1,-1,-1):
                        if yellow_count == 4:
                            return "YELLOW"
                        if self.board[row][c] == 0 or self.board[row][c] == "red":
                            break
                        if self.board[row][c] == "yellow":
                            yellow_count += 1
        
        return ""

    def _check_right(self):

        for row in range(5,-1,-1):
            for col in range(6,-1,-1):
                red_count = 0
                yellow_count = 0

                if self.board[row][col] == 0:
                    continue
                elif self.board[row][col] == "red":
                    red_count += 1
                    for c in range(col+1,7,1):
                        if red_count == 4:
                            return "RED"
                        if self.board[row][c] == 0 or self.board[row][c] == "yellow":
                            break
                        if self.board[row][c] == "red":
                            red_count += 1
                else:
                    yellow_count += 1
                    for c in range(col+1,7,1):
                        if yellow_count == 4:
                            return "YELLOW"
                        if self.board[row][c] == 0 or self.board[row][c] == "red":
                            break
                        if self.board[row][c] == "yellow":
                            yellow_count += 1
        
        return ""


'''
Add Helper functions as needed to handle moves and update board and turns
'''


    
