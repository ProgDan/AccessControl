#!/usr/bin/python3
# -*- coding: utf8 -*-
#
#    Copyright 2018 Daniel Arndt Alves <progdan@gmail.com>
#
#    This file is part of AccessControl
#    AccessControl is a simple Python implementation for
#    the MFRC522 NFC Card Reader and Access Control System 
#    for the Raspberry Pi.
#
#    AccessControl is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    AccessControl is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with AccessControl.  If not, see <http://www.gnu.org/licenses/>.
#
# Programa: Rotina de inicialização do Banco de Dados
# Apaga e cria novas tabelas

import sqlite3

############### Settings ####################
# DB Name
DB_NAME = "./DB/access.db"

# SQL File with Table Schema and Initialization Data
SQL_File_Name = "./DB/Scripts/Table_Schema.sql"
##############################################

# Read Table Schema into a Variable and remove all New Line Chars
TableSchema=""
with open(SQL_File_Name, 'r') as SchemaFile:
    TableSchema = SchemaFile.read().replace('\n','')

#Connect or Create DB File
conn = sqlite3.connect(DB_NAME)
curs = conn.cursor()

#Create Tables
sqlite3.complete_statement(TableSchema)
curs.executescript(TableSchema)

#Close DB
curs.close()
conn.close()
