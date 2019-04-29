#!/usr/bin/python3
# -*- coding: utf8 -*-

class Horario:
    def __init__(self,dia=0,inicio='00:00',fim='23:59',sentido='B',usuario=0):
        self.HorDia = dia
        self.HorInicio = inicio
        self.HorFim = fim
        self.HorSentido = sentido
        self.UsrCodigo = usuario
    
    def getHorDia(self):
        return self.HorDia
    
    def getHorInicio(self):
        return self.HorInicio

    def getHorFim(self):
        return self.HorFim

    def getHorSentido(self):
        return self.HorSentido

    def getUsrCodigo(self):
        return self.UsrCodigo
