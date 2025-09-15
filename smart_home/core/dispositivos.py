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



class StatesPorta(StrEnum):

    TRANCADA = "trancada"
    DESTRANCADA = "destrancada"
    ABERTA = "aberta"


    def __str__(self) -> str:
        return self.name



class CorEnum(StrEnum):

    NEUTRA = "neutra",
    FRIA = "fria",
    QUENTE = "quente"

    
    def __str__(self) -> str:
        return self.name


    def all_colors():
        
        cores = [cor.name for cor in list(CorEnum)]

        return ", ".join(cores)



class StatusCamera(StrEnum):

    ON = "on"
    GRAVANDO = "gravando"
    STOP = "stop"
    OFF = "off"


    def __str__(self) -> str:
        return self.name



class StatusIrrigador(StrEnum):

    LIGADO = "ligado",
    IRRIGANDO = "irrigando",
    DESLIGADO = "desligado"


    def __str__(self) -> str:
        return self.name