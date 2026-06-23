import sqlite3
from flask import g
import config

def get_connection():
    con = sqlite3.connect(config.database_file)
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con

def execute(sql, params=None):
    if params is None:
        params = []
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
    con.close()

def last_insert_id():
    return g.last_insert_id

def query(sql, params=None):
    if params is None:
        params = []
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result
