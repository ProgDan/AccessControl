#!/usr/bin/python3
# -*- coding: utf8 -*-

class Movimento:
    def __init__(self,data,cartao,sentido,bloqueado,forahorario,provisorio,usuario):
        self.MovData = data
        self.MovBarra = cartao
        self.MovSentido = sentido
        self.MovBloqueado = bloqueado
        self.MovForaHorario = forahorario
        self.MovProvisorio = provisorio
        self.UsrCodigo = usuario
