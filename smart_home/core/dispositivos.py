from enum import Enum, StrEnum
from abc import ABC
from dataclasses import dataclass


class TiposDispostivos(StrEnum):

    CAMERA = "camera",
    IRRIGADOR = "irrigador",
    LUZ = "luz",
    PERSIANA = "persiana",
    PORTA = "porta",
    TOMADA = "tomada"


    def __str__(self) -> str:
        return self.name


    def all_dispositives():
        
        dispositivos = [dispositivo.value.upper() for dispositivo in list(TiposDispostivos)]

        return ", ".join(dispositivos)



@dataclass
class Dispositivo(ABC):

    _id:str
    nome:str
    tipo:TiposDispostivos
    

    @property
    def id(self):
        return self._id


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


    def all_colors():
        
        cores = [cor.name for cor in list(CorEnum)]

        return ", ".join(cores)



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