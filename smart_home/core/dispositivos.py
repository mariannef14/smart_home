from enum import Enum


class StatesPorta(Enum):

    TRANCADA = 0
    DESTRANCADA = 1
    ABERTA = 2


    def __str__(self) -> str:
        return self.name


class CorEnum(Enum):

    NEUTRA = 0,
    FRIA = 1,
    QUENTE = 2

    
    def __str__(self) -> str:
        return self.name


class StatusCamera(Enum):

    ON = 0 
    GRAVANDO = 1
    STOP = 2
    OFF = 3


    def __str__(self) -> str:
        return self.name


class StatusIrrigador(Enum):

    LIGADO = 0,
    IRRIGANDO = 1,
    DESLIGADO = 2


    def __str__(self) -> str:
        return self.name


class TiposDispostivos(Enum):

    CAMERA = 0,
    IRRIGADOR = 1,
    LUZ = 2,
    PERSIANA = 3,
    PORTA = 4,
    TOMADA = 5