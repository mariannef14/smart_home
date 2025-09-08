from enum import Enum


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