#!/usr/bin/python3
# -*- coding: utf8 -*-

from datetime import datetime

class Usuario:
    def __init__(self,codigo,nome,cartao,provisorio='',validade=0):
        self.UsrCodigo = codigo
        self.UsrNome = nome
        self.UsrBarra = cartao
        self.UsrProvisorio = provisorio
        self.UsrProvisorioValidade = validade
    
    def __str__(self):
        return self.UsrNome
