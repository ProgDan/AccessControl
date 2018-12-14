#!/usr/bin/python3
# -*- coding: utf8 -*-

from datetime import datetime

class Movimento:
    def __init__(self,data=datetime.now(),cartao='',sentido='P',bloqueado=0,forahorario=0,provisorio=0,usuario=0):
        self.MovData = data
        self.MovBarra = cartao
        self.MovSentido = sentido
        self.MovBloqueado = bloqueado
        self.MovForaHorario = forahorario
        self.MovProvisorio = provisorio
        self.UsrCodigo = usuario
