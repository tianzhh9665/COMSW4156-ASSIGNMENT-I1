import sqlite3
from sqlite3 import Error
from sqlite3.dbapi2 import Cursor

'''
Initializes the Table GAME
Do not modify
'''


def init_db():
    # creates Table
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        conn.execute('CREATE TABLE GAME(current_turn TEXT, board TEXT,'
                     + 'winner TEXT, player1 TEXT, player2 TEXT'
                     + ', remaining_moves INT)')
        print('Database Online, table created')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


'''
move is a tuple (current_turn, board, winner, player1, player2,
remaining_moves)
Insert Tuple into table
'''


def add_move(move):  # will take in a tuple
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO GAME(current_turn, board,winner, player1, player2,remaining_moves) VALUES (?,?,?,?,?,?)",move)
        conn.commit()
        print('move added')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


'''
Get the last move played
return (current_turn, board, winner, player1, player2, remaining_moves)
'''


def getMove():
    # will return tuple(current_turn, board, winner, player1, player2,
    # remaining_moves) or None if db fails
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * from GAME order by remaining_moves asc").fetchall()
        result = None
        if(len(rows) == 0):
            return result
        
        row = rows[0]
        result = (row[0],row[1],row[2],row[3],row[4],row[5])
        
        print('move got')
        return result
        
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


'''
Clears the Table GAME
Do not modify
'''


def clear():
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        conn.execute("DROP TABLE GAME")
        print('Database Cleared')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()
