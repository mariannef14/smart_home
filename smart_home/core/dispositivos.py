from enum import Enum
from abc import ABC


class TiposDispostivos(Enum):

    CAMERA = 0,
    IRRIGADOR = 1,
    LUZ = 2,
    PERSIANA = 3,
    PORTA = 4,
    TOMADA = 5


    def __str__(self) -> str:
        return self.name


    def all_dispositives():
        
        dispositivos = [dispositivo.name for dispositivo in list(TiposDispostivos)]

        return ", ".join(dispositivos)



class Dispositivo(ABC):

    def __init__(self, id:str, nome:str, tipo_dispositivo: TiposDispostivos):
        self.id = id
        self.nome = nome
        self.tipo = tipo_dispositivo

    def __str__(self):
        return f"{self.id} | {self.tipo}"



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