#!/usr/bin/python3
# -*- coding: utf8 -*-

class Usuario:
    def __init__(self,codigo,nome,cartao):
        self.UsrCodigo = codigo
        self.UsrNome = nome
        self.UsrBarra = cartao
        self.UsrProvisorio = ''
        self.UsrProvisorioValidade = 0
    
    def __str__(self):
        return self.UsrNome
