import sqlite3

def connect_BD():
    conn = sqlite3.connect('databaseMK.db')
    return conn