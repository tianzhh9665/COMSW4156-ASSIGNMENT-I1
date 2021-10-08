import unittest
from Gameboard import Gameboard
import sqlite3
from sqlite3 import Error
from sqlite3.dbapi2 import Cursor
import db


class Test_TestDb(unittest.TestCase):
    def setUp(self):
        self.board = Gameboard()
        db.clear()
    def tearDown(self):
        self.board = Gameboard()
        db.clear()

    def test_init_db(self):
        # check if init_db which initializing table works
        db.init_db()

        conn = None
        try:
            conn = sqlite3.connect('sqlite_db')
            cursor = conn.cursor()
            result = cursor.execute("SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name = 'GAME'").fetchone()
            self.assertEqual(result[0], 1, "init_db failed")

        except Error as e:
            print(e)

        finally:
            if conn:
                conn.close()
    
    def test_getMove(self):
        # check if getMove which retrives current game info works
        db.init_db()
        move = db.getMove()
        self.assertEqual(move, None, "getMove failed")

        pending_save_move = ('p2', '0 0 0 0 0 0 0,0 0 0 0 0 0 0,0 0 0 0 0 0 0,0 0 0 0 0 0 0,0 0 0 0 0 0 0,red 0 0 0 0 0 0', '', 'red', 'yellow', 41)
        db.add_move(pending_save_move)
        move = db.getMove()
        self.assertEqual(move, pending_save_move, "getMove failed")

    def test_addMove(self):
        # check if addMove which adds a move to the data base works
        db.init_db()
        pending_save_move = ('p2', '0 0 0 0 0 0 0,0 0 0 0 0 0 0,0 0 0 0 0 0 0,0 0 0 0 0 0 0,0 0 0 0 0 0 0,red 0 0 0 0 0 0', '', 'red', 'yellow', 41)
        db.add_move(pending_save_move)
        move = db.getMove()
        self.assertEqual(move, pending_save_move, "addMove failed")

        pending_save_move = ('p1', '0 0 0 0 0 0 0,0 0 0 0 0 0 0,0 0 0 0 0 0 0,0 0 0 0 0 0 0,0 0 0 0 0 0 0,red yellow 0 0 0 0 0', '', 'red', 'yellow', 40)
        db.add_move(pending_save_move)
        move = db.getMove()
        self.assertEqual(move, pending_save_move, "addMove failed")

    def test_clear(self):
        db.init_db()
        db.clear()

        conn = None
        try:
            conn = sqlite3.connect('sqlite_db')
            cursor = conn.cursor()
            result = cursor.execute("SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name = 'GAME'").fetchone()
            self.assertEqual(result[0], 0, "clear failed") # no GAME table

        except Error as e:
            print(e)

        finally:
            if conn:
                conn.close()