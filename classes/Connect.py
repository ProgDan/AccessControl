#!/usr/bin/python3
# -*- coding: utf8 -*-

"""
    Esta classe gerencia um banco de dados sqlite3.
     
    Banco de dados: '../DB/access.db'
    Schema: '../DB/Scripts/Usr_Schema.sql'
"""

import sqlite3

class Connect(object):
    '''A classe Connect representa o banco de dados'''
    def __init__(self, db_name):
        try:
            # Connect to database
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
            # Show database information
            print("Database: ",db_name)
            # Read SQLite version
            self.cursor.execute('SELECT SQLITE_VERSION()')
            self.data = self.cursor.fetchone()
            # Show the SQLite version
            print("SQLite version: %s" % self.data)
        except sqlite3.Error:
            print("Database open error!")

    
    def commit_db(self):
        if self.conn:
            self.conn.commit()
    
    def close_db(self):
        if self.conn:
            self.conn.close()
            print("Database closed.")
    
