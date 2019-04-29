#!/usr/bin/python3
# -*- coding: utf8 -*-
 
"""
    Esta Classe representa um usuario em um banco de dados sqlite3.
     
    Banco de dados: '../DB/access.db'
    Schema: '../DB/Scripts/Usr_Schema.sql'
    Tabela: 'Usuario'
"""

import sqlite3
import csv
from classes.Connect import Connect as Connect
from classes.usuario import Usuario as Usuario

############### Settings ####################
# DB Name
DB_NAME = "./DB/access.db"

class UsrDb(object):
    tb_name = 'Usuario'
    
    '''A classe UsrDB representa um usuário no banco de dados.'''
    def __init__(self, db):
        self.db = db
        self.tb_name
    
    # create_schema
    def create_schema(self, schema_name='./DB/Scripts/Usr_Schema.sql'):
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
            INSERT INTO Usuario (UsrCodigo, UsrNome, UsrBarra, UsrProvisorio, UsrProvisorioValidade)
            VALUES (5079,'Daniel', '72:8:6B:1F:E','',0)
            """)
            # commit to db
            self.db.commit_db()
            print("Usuário inserido com sucesso.")
        except sqlite3.IntegrityError:
            print("Aviso: O código do usuário deve ser único.")
            return False
    
    # insert with list
    def insert_with_list(self):
        # create a data list
        lista = [(5079,'Daniel', '72:8:6B:1F:E','',0),
                 (1,'Teste', '72:8:6B:1F:E','',0),
                ]
        try:
            self.db.cursor.executemany("""
            INSERT INTO Usuario (UsrCodigo, UsrNome, UsrBarra, UsrProvisorio, UsrProvisorioValidade)
            VALUES (?,?,?,?,?)
            """, lista)
            # commit to db
            self.db.commit_db()
            print("Dados inseridos na lista com sucesso: %s registros." %
                  len(lista))
        except sqlite3.IntegrityError:
            print("Aviso: O código do usuário deve ser único.")
            return False
    
    # insert for file
    def insert_for_file(self):
        try:
            with open('./DB/data/Usuario_dados.sql', 'rt') as f:
                dados = f.read()
                self.db.cursor.executescript(dados)
                # commit to db
                self.db.commit_db()
                print("Dados inseridos do arquivo com sucesso.")
        except sqlite3.IntegrityError:
            print("Aviso: O código de usuário deve ser único.")
            return False
    
    # insert from CSV file
    def insert_from_csv(self, file_name='csv/usuarios.csv'):
        try:
            reader = csv.reader(
                open(file_name,'rt'), delimiter=',')
            linha = (reader,)
            for linha in reader:
                self.db.cursor.execute("""
                INSERT INTO Usuario (UsrCodigo, UsrNome, UsrBarra, UsrProvisorio, UsrProvisorioValidade)
                VALUES (?,?,?,?,?)
                """, linha)
            # commit to db
            self.db.commit_db()
            print("Dados importados do csv com sucesso.")
        except sqlite3.IntegrityError:
            print("Aviso: O código de usuário deve ser único.")
            return False
    
    # insert with parameter
    def insert_with_parameter(self):
        # solicitando os dados ao usuário
        self.UsrCodigo = input('Código: ')
        self.UsrNome = input('Nome: ')
        self.UsrBarra = input('Código de barra: ')
        self.UsrProvisorio = input('Código de barra provisório: ')
        self.UsrProvisorioValidade = input('Data da validade do provisório: ')

        try:
            self.db.cursor.execute("""
            INSERT INTO Usuario (UsrCodigo, UsrNome, UsrBarra, UsrProvisorio, UsrProvisorioValidade)
            VALUES (?,?,?,?,?)
            """, (self.UsrCodigo, self.UsrNome, self.UsrBarra, self.UsrProvisorio, self.UsrProvisorioValidade))
            # commit to db
            self.db.commit_db()
            print("Dados inseridos com sucesso.")
        except sqlite3.IntegrityError:
            print("Aviso: O código de usuário deve ser único.")
            return False
    
    ''' READ '''

    # read all users
    def read_all_users(self):
        sql = 'SELECT * FROM Usuario ORDER BY UsrNome'
        r = self.db.cursor.execute(sql)
        return r.fetchall()
    
    # print all users
    def print_all_users(self):
        lista = self.read_all_users()
        print('{:>3s} {:20s} {:14s} {:14s} {:s}'.format(
              'id', 'nome', 'barra', 'provisorio', 'validade'))
        for c in lista:
            print('{:4d} {:23s} {:14s} {:14s} {:s}'.format(
                  c[0], c[1], c[2], c[3], c[4]))
    
    # find user
    def find_user(self, id):
        r = self.db.cursor.execute(
            'SELECT * FROM Usuario WHERE UsrCodigo = ?',(id,))
        return r.fetchone()

    # find user by card
    def find_user_by_card(self, card):
        user = Usuario()
        r = self.db.cursor.execute(
            'SELECT COUNT(*) FROM Usuario WHERE UsrBarra = ?',(card,))
        if(r.fetchone()[0] > 0):
            # instancia o usuario e devolve
            r = self.db.cursor.execute(
                'SELECT * FROM Usuario WHERE UsrBarra = ?',(card,))
            usrdata = r.fetchone()
            user = Usuario(usrdata[0],usrdata[1],usrdata[2],usrdata[3],usrdata[4])
        else:
            r = self.db.cursor.execute(
                'SELECT COUNT(*) FROM Usuario WHERE UsrProvisorio = ?',(card,))
            if(r.fetchone()[0] > 0):
                # instancia o usuario e devolve
                r = self.db.cursor.execute(
                    'SELECT * FROM Usuario WHERE UsrBarra = ?',(card,))
                usrdata = r.fetchone()
                user = Usuario(usrdata[0],usrdata[1],usrdata[2],usrdata[3],usrdata[4])
        return user
    
    # print user
    def print_user(self,id):
        if self.find_user(id) == None:
            print('Não existe usuário com o id informado.')
        else:
            print(self.find_user(id))
    
    # count user
    def count_user(self):
        r = self.db.cursor.execute(
            'SELECT COUNT(*) FROM Usuario')
        print("Total de clientes: ", r.fetchone()[0])
    
    # read file
    def read_file(self, file_name='sql/usuarios.sql'):
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
    
    ''' UPDATE '''
 
    # update_data
    def update_data(self, id):
        try:
            c = self.find_user(id)
            if c:
                self.UsrProvisorio = input('Código de barra provisório: ')
                self.db.cursor.execute("""
                UPDATE Usuario
                SET UsrProvisorio = ?
                WHERE UsrCodigo = ?
                """, (self.UsrProvisorio, id,))
                self.db.commit_db()
                print("Dados atualizados com sucesso.")
            else:
                print('Não existe usuário com o código informado.')
        except sqlite3.Error:
            raise sqlite3.Error
     
 
    ''' DELETE '''
 
    # delete_data
    def delete_data(self, id):
        try:
            c = self.find_user(id)
            if c:
                self.db.cursor.execute("""
                DELETE FROM Usuario WHERE UsrCodigo = ?
                """, (id,))
                self.db.commit_db()
                print("Registro %d excluído com sucesso." % id)
            else:
                print('Não existe usuário com o código informado.')
        except sqlite3.Error:
            raise sqlite3.Error
