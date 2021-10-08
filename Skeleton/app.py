from re import match
from flask import Flask, render_template, request, jsonify
from json import dump
from Gameboard import Gameboard
import db
import logging

app = Flask(__name__)


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

game = None

'''
Implement '/' endpoint
Method Type: GET
return: template player1_connect.html and status = "Pick a Color."
Initial Webpage where gameboard is initialized
'''


@app.route('/', methods=['GET'])
def player1_connect():

    global game
    game = Gameboard()

    db.clear()
    record = db.getMove()
    if record is not None:
        # clear table fails
        raise Exception("db clear table fails")
    db.init_db()

    return render_template('player1_connect.html', status="Pick a Color.")


'''
Helper function that sends to all boards don't modify
'''


@app.route('/autoUpdate', methods=['GET'])
def updateAllBoards():
    try:
        return jsonify(move=game.board, winner=game.game_result,
                       color=game.player1)
    except Exception:
        return jsonify(move="")


'''
Implement '/p1Color' endpoint
Method Type: GET
return: template player1_connect.html and status = <Color picked>
Assign player1 their color
'''


@app.route('/p1Color', methods=['GET'])
def player1_config():
    try:
        saved_state = db.getMove()
        if saved_state is not None:
            game.set_player_1(saved_state[3])
            game.set_player_2(saved_state[4])
            game.current_turn = saved_state[0]
            game.game_result = saved_state[2]
            game.remaining_moves = saved_state[5]
            game.board = game.get_board_from_str(saved_state[1])

            return render_template('player1_connect.html', status=saved_state[3])
        else:    
            player1_color = request.args.get('color', '')
            game.set_player_1(player1_color)

            return render_template('player1_connect.html', status=player1_color)
    except KeyError:
        return render_template('player1_connect.html', status="")


'''
Implement '/p2Join' endpoint
Method Type: GET
return: template p2Join.html and status = <Color picked> or Error
if P1 didn't pick color first

Assign player2 their color
'''


@app.route('/p2Join', methods=['GET'])
def p2Join():
    saved_state = db.getMove()
    if saved_state is not None:
        game.set_player_1(saved_state[3])
        game.set_player_2(saved_state[4])
        game.current_turn = saved_state[0]
        game.game_result = saved_state[2]
        game.remaining_moves = saved_state[5]
        game.board = game.get_board_from_str(saved_state[1])

        return render_template('p2Join.html', status=saved_state[4])



    if game.player1 == 'red':
        game.player2 = 'yellow'
        return render_template('p2Join.html', status=game.player2)
    elif game.player1 == 'yellow':
        game.player2 = 'red'
        return render_template('p2Join.html', status=game.player2)
    else:
        return render_template('p2Join.html',
                               status="ERROR: player 1 pick the color first!")


'''
Implement '/move1' endpoint
Method Type: POST
return: jsonify (move=<CurrentBoard>,
invalid=True or False, winner = <currWinner>)
If move is valid --> invalid = False else invalid = True
If invalid == True, also return reason= <Why Move is Invalid>

Process Player 1's move
'''


@app.route('/move1', methods=['POST'])
def p1_move():
    global game
    column = -1
    if request.method == 'POST':
        column = int(request.get_json()["column"][-1])

    verify_result = game.verify_game_status_and_move(column, 'p1')
    if verify_result == "NO_COLOR_P1":
        return jsonify(move=game.board, invalid=True,
                       reason="You have not picked a color to start!",
                       winner='')
    if verify_result == "NO_COLOR_P2":
        return jsonify(move=game.board, invalid=True,
                       reason="Player 2 has not picked a color to start!",
                       winner='')
    if verify_result == "WINNER_P1":
        return jsonify(move=game.board,
                       invalid=True,
                       winner=game.game_result)
    if verify_result == "WINNER_P2":
        return jsonify(move=game.board, invalid=True, winner=game.game_result)
    if verify_result == "DRAW":
        return jsonify(move=game.board,
                       invalid=True, reason="The game is a draw!",
                       winner='')
    if verify_result == "NOT_YOUR_TURN_p1":
        return jsonify(move=game.board,
                       invalid=True, reason="This is not your turn right now!",
                       winner='')
    if verify_result == "INVALID":
        return jsonify(move=game.board,
                       invalid=True, reason="Invalid move: The column is full",
                       winner='')
    if verify_result == "VALID":
        game.move(column, game.player1)
        game.determine_winner()
        game.change_turn()
        game.decrease_remaining_moves()

        pending_save_move = (game.current_turn,game.get_board_str(),game.game_result,game.player1,game.player2,game.remaining_moves)
        print(pending_save_move)
        db.add_move(pending_save_move)
        return jsonify(move=game.board, invalid=False, winner=game.game_result)


'''
Same as '/move1' but instead proccess Player 2
'''


@app.route('/move2', methods=['POST'])
def p2_move():
    global game
    column = -1
    if request.method == 'POST':
        column = int(request.get_json()["column"][-1])
    verify_result = game.verify_game_status_and_move(column, 'p2')
    if verify_result == "NO_COLOR_P1":
        return jsonify(move=game.board, invalid=True,
                       reason="Player 1 has not picked a color to start!",
                       winner='')
    if verify_result == "NO_COLOR_P2":
        return jsonify(move=game.board, invalid=True,
                       reason="You have not picked a color to start!",
                       winner='')
    if verify_result == "WINNER_P1":
        return jsonify(move=game.board, invalid=True, winner=game.game_result)
    if verify_result == "WINNER_P2":
        return jsonify(move=game.board, invalid=True, winner=game.game_result)
    if verify_result == "DRAW":
        return jsonify(move=game.board, invalid=True,
                       reason="The game is a draw!", winner='')
    if verify_result == "NOT_YOUR_TURN_p2":
        return jsonify(move=game.board, invalid=True,
                       reason="This is not your turn right now!", winner='')
    if verify_result == "INVALID":
        return jsonify(move=game.board, invalid=True,
                       reason="Invalid move: The column to insert is full!",
                       winner='')
    if verify_result == "VALID":
        game.move(column, game.player2)
        game.determine_winner()
        game.change_turn()
        game.decrease_remaining_moves()

        pending_save_move = (game.current_turn,game.get_board_str(),game.game_result,game.player1,game.player2,game.remaining_moves)

        db.add_move(pending_save_move)

        return jsonify(move=game.board, invalid=False, winner=game.game_result)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
