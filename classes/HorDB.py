#!/usr/bin/python3
# -*- coding: utf8 -*-
 
"""
    Esta Classe representa um horario em um banco de dados sqlite3.
     
    Banco de dados: '../DB/access.db'
    Schema: '../DB/Scripts/Usr_Schema.sql'
    Tabela: 'Horario'
"""

import sqlite3
import csv
from datetime import datetime
from datetime import timedelta
from classes.Connect import Connect as Connect


############### Settings ####################
# DB Name
DB_NAME = "./DB/access.db"

class HorDb(object):
    tb_name = 'Horario'
    
    '''A classe HorDB representa um horário no banco de dados.'''
    def __init__(self, db):
        self.db = db
        self.tb_name
    
    # create_schema
    def create_schema(self, schema_name='./DB/Scripts/Hor_Schema.sql'):
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
            INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo)
            VALUES (1,'00:00','23:59','A',0,5079)
            """)
            # commit to db
            self.db.commit_db()
            print("Horário inserido com sucesso.")
        except sqlite3.IntegrityError:
            print("Aviso: O horário deve ser único para um usuário.")
            return False
    
    # insert with list
    def insert_with_list(self):
        # create a data list
        lista = [(1,'00:00','23:59','A',0,5079),
                 (2,'00:00','23:59','A',0,5079),
                 (3,'00:00','23:59','A',0,5079),
                 (4,'00:00','23:59','A',0,5079),
                 (5,'00:00','23:59','A',0,5079)
                ]
        try:
            self.db.cursor.executemany("""
            INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo)
            VALUES (?,?,?,?,?,?)
            """, lista)
            # commit to db
            self.db.commit_db()
            print("Dados inseridos na lista com sucesso: %s registros." %
                  len(lista))
        except sqlite3.IntegrityError:
            print("Aviso: O horário deve ser único para um usuário.")
            return False
    
    # insert for file
    def insert_for_file(self):
        try:
            with open('./DB/data/Horario_dados.sql', 'rt') as f:
                dados = f.read()
                self.db.cursor.executescript(dados)
                # commit to db
                self.db.commit_db()
                print("Dados inseridos do arquivo com sucesso.")
        except sqlite3.IntegrityError:
            print("Aviso: O horário deve ser único para um usuário.")
            return False
    
    # insert from CSV file
    def insert_from_csv(self, file_name='csv/horarios.csv'):
        try:
            reader = csv.reader(
                open(file_name,'rt'), delimiter=',')
            linha = (reader,)
            for linha in reader:
                self.db.cursor.execute("""
                INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo)
                VALUES (?,?,?,?,?,?)
                """, linha)
            # commit to db
            self.db.commit_db()
            print("Dados importados do csv com sucesso.")
        except sqlite3.IntegrityError:
            print("Aviso: O horário deve ser único para um usuário.")
            return False
    
    # insert with parameter
    def insert_with_parameter(self):
        # solicitando os dados ao usuário
        self.HorDia = input('Dia da semana: ')
        self.HoraInicio = input('Horario inicial: ')
        self.HoraFim = input('HorarioFinal: ')
        self.HoraSentido = input('Sentido permitido: ')
        self.HoraValidacao = input('Validacao: ')
        self.UsrCodigo = input('Código: ')

        try:
            self.db.cursor.execute("""
            INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo)
            VALUES (?,?,?,?,?,?)
            """, (self.HorDia,self.HoraInicio,self.HoraFim,self.HoraSentido,self.HoraValidacao,self.UsrCodigo))
            # commit to db
            self.db.commit_db()
            print("Dados inseridos com sucesso.")
        except sqlite3.IntegrityError:
            print("Aviso: O horário deve ser único para um usuário.")
            return False
    
    ''' READ '''

    # read all horarios
    def read_all_horarios(self):
        sql = 'SELECT * FROM Horario ORDER BY UsrCodigo'
        r = self.db.cursor.execute(sql)
        return r.fetchall()
    
    # print all users
    def print_all_horarios(self):
        lista = self.read_all_horarios()
        print('{:>3s} {:5s} {:5s} {:3s} {:3s} {:>3s}'.format(
              'dia', 'inicio', 'fim', 'sentido', 'validacao', 'usuario'))
        for c in lista:
            print('{:4d} {:7s} {:7s} {:4s} {:4s} {:4d}'.format(
                  c[0], c[1], c[2], c[3], c[4], c[5]))
    
    # find user
    def find_user(self, id):
        r = self.db.cursor.execute(
            'SELECT * FROM Horario WHERE UsrCodigo = ?',(id,))
        return r.fetchone()
    
    def check_horario_by_user(self, id, day = (datetime.today().weekday()+1)%7, hora = datetime.now()):
        r = self.db.cursor.execute(
            'SELECT * FROM Horario WHERE UsrCodigo = ? AND HorDia = ?',(id, day,))
        lista = r.fetchall()
        for row in lista:
            ini = datetime.strptime(datetime.now().strftime('%Y-%m-%d') + ' ' + row[2],'%Y-%m-%d %H:%M')
            fim = datetime.strptime(datetime.now().strftime('%Y-%m-%d') + ' ' + row[3],'%Y-%m-%d %H:%M')
            if(hora > ini and hora < fim):
                return True
        return False

    # print user
    def print_user(self,id):
        if self.find_user(id) == None:
            print('Não existe horário para o usuário com o id informado.')
        else:
            print(self.find_user(id))
    
    # count user
    def count_user(self):
        r = self.db.cursor.execute(
            'SELECT COUNT(*) FROM Horario')
        print("Total de horarios: ", r.fetchone()[0])
    
    # read file
    def read_file(self, file_name='sql/horarios.sql'):
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
