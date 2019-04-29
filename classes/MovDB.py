#!/usr/bin/python3
# -*- coding: utf8 -*-
 
"""
    Esta Classe representa um movimento em um banco de dados sqlite3.
     
    Banco de dados: '../DB/access.db'
    Schema: '../DB/Scripts/Usr_Schema.sql'
    Tabela: 'Movimento'
"""

import sqlite3
import csv
from datetime import datetime
import Connect as Connect
import Movimento as Movimento

############### Settings ####################
# DB Name
DB_NAME = "./DB/access.db"

class MovDb(object):
    tb_name = 'Movimento'
    
    '''A classe MovDB representa um movimento no banco de dados.'''
    def __init__(self,db = Connect(DB_NAME)):
        self.db = db
        self.tb_name
    
    # create_schema
    def create_schema(self, schema_name='./DB/Scripts/Mov_Schema.sql'):
        print("Criando tabela %s ..." % self.tb_name)

        try:
            with open(schema_name, 'rt') as f:
                schema = f.read()
                self.db.cursor.executescript(schema)
        except sqlite3.Error:
            print("Aviso: A tabela %s já existe." % self.tb_name)
            return False
        
        print("Tabela %s criada com sucesso." % self.tb_name)
    
    ''' CREATE '''

    # insert one register
    def insert_one_register(self):
        try:
            self.db.cursor.execute("""
            INSERT INTO Movimento (MovData, MovBarra, MovSentido, MovBloqueado, MovForaHorario, MovProvisorio, UsrCodigo)
            VALUES (DateTime('now'),'72:8:6B:1F:E', 'P',0,0,0,5079)
            """)
            # commit to db
            self.db.commit_db()
            print("Movimento inserido com sucesso.")
        except sqlite3.IntegrityError:
            print("Aviso: O movimento deve ser único.")
            return False
    
    def insert_movimento(self, mov = Movimento()):
        try:
            self.db.cursor.execute("""
            INSERT INTO Movimento (MovData, MovBarra, MovSentido, MovBloqueado, MovForaHorario, MovProvisorio, UsrCodigo)
            VALUES (?,?,?,?,?,?,?)
            """, (mov.getMovData,mov.getMovBarra,mov.getMovSentido,mov.getMovBloqueado,mov.getMovForaHorario,
                    mov.getMovProvisorio,mov.getUsrCodigo))
            # commit to db
            self.db.commit_db()
            print("Movimento inserido com sucesso.")
        except sqlite3.IntegrityError:
            print("Aviso: O movimento deve ser único.")
            return False

    
    # insert with list
    def insert_with_list(self):
        # create a data list
        lista = [('72:8:6B:1F:E','P',0,0,0,5079),
                 ('72:8:6B:1F:E','P',0,0,0,1),
                ]
        try:
            self.db.cursor.executemany("""
            INSERT INTO Movimento (MovData, MovBarra, MovSentido, MovBloqueado, MovForaHorario, MovProvisorio, UsrCodigo)
            VALUES (DateTime('now'),?,?,?,?,?,?)
            """, lista)
            # commit to db
            self.db.commit_db()
            print("Dados inseridos na lista com sucesso: %s registros." %
                  len(lista))
        except sqlite3.IntegrityError:
            print("Aviso: O movimento deve ser único.")
            return False
    
    # insert for file
    def insert_for_file(self):
        try:
            with open('./DB/data/Movimento_dados.sql', 'rt') as f:
                dados = f.read()
                self.db.cursor.executescript(dados)
                # commit to db
                self.db.commit_db()
                print("Dados inseridos do arquivo com sucesso.")
        except sqlite3.IntegrityError:
            print("Aviso: O movimento deve ser único.")
            return False
    
    # insert from CSV file
    def insert_from_csv(self, file_name='csv/movimento.csv'):
        try:
            reader = csv.reader(
                open(file_name,'rt'), delimiter=',')
            linha = (reader,)
            for linha in reader:
                self.db.cursor.execute("""
                INSERT INTO Movimento (MovData, MovBarra, MovSentido, MovBloqueado, MovForaHorario, MovProvisorio, UsrCodigo)
                VALUES (DateTime('now'),?,?,?,?,?,?)
                """, linha)
            # commit to db
            self.db.commit_db()
            print("Dados importados do csv com sucesso.")
        except sqlite3.IntegrityError:
            print("Aviso: O movimento deve ser único.")
            return False
    
    # insert with parameter
    def insert_with_parameter(self):
        # solicitando os dados ao usuário
        self.MovData = datetime.now()
        self.MovBarra = input('Código de barra: ')
        self.MovSentido = input('Sentido solicitado: ')
        self.MovBloqueado = input('Movimento bloqueado: ')
        self.MovForaHorario = input('Movimento fora de horario: ')
        self.MovProvisorio = input('Cracha provisorio: ')
        self.UsrCodigo = input('Código do usuario: ')

        try:
            self.db.cursor.execute("""
            Movimento (MovData, MovBarra, MovSentido, MovBloqueado, MovForaHorario, MovProvisorio, UsrCodigo)
            VALUES (?,?,?,?,?,?,?)
            """, (self.MovData,self.MovBarra,self.MovSentido,self.MovBloqueado,self.MovForaHorario,
                    self.MovProvisorio,self.UsrCodigo))
            # commit to db
            self.db.commit_db()
            print("Dados inseridos com sucesso.")
        except sqlite3.IntegrityError:
            print("Aviso: O movimento deve ser único.")
            return False
    
    ''' READ '''

    # read all moviments
    def read_all_moviments(self):
        sql = 'SELECT * FROM Movimento ORDER BY MovData'
        r = self.db.cursor.execute(sql)
        return r.fetchall()
    
    # print all moviments
    def print_all_moviments(self):
        lista = self.read_all_moviments()
        print('{:>20s} {:14s} {:3s} {:3s} {:3s} {:3s} {:3s}'.format(
              'data', 'barra', 'sentido', 'bloqueado', 'forahorario', 'provisorio', 'usuario'))
        for c in lista:
            print('{:23d} {:14s} {:4s} {:4d} {:4d} {:4d} {:4d}'.format(
                  c[0], c[1], c[2], c[3], c[4], c[5], c[6]))
    
    # find user
    def find_user(self, id):
        r = self.db.cursor.execute(
            'SELECT * FROM Movimento WHERE UsrCodigo = ? ORDER BY MovDada DESC',(id,))
        return r.fetchone()
    
    # print user
    def print_user(self,id):
        if self.find_user(id) == None:
            print('Não existe movimento para o usuário com o id informado.')
        else:
            print(self.find_user(id))
    
    # count movimento
    def count_user(self):
        r = self.db.cursor.execute(
            'SELECT COUNT(*) FROM Movimen to')
        print("Total de movimentos: ", r.fetchone()[0])
    
    # read file
    def read_file(self, file_name='sql/movimento.sql'):
        with open(file_name, 'rt') as f:
            dados = f.read()
            sqlcommands = dados.split(';')
            print("Consulta feita a partir de um arquivo externo.")
            for command in sqlcommands:
                r = self.db.cursor.execute(command)
                for c in r.fetchall():
                    print(c)
        # commit to db
        self.db.commit_db()
