from transitions import Machine
from datetime import datetime
from dataclasses import dataclass, field
from time import sleep

from smart_home.core.dispositivos import TiposDispostivos
from smart_home.core.validators import PotenciaValidator
from smart_home.core.dispositivos import Dispositivo


transitions = [

    {
        "trigger": "ligar",
        "source": "Off",
        "dest": "On"
    },

    {
        "trigger": "desligar",
        "source": "On",
        "dest": "Off"
    }

]


@dataclass
class Tomada(Dispositivo):

    id:str
    nome:str
    potencia_w:int = PotenciaValidator()
    tipo:TiposDispostivos = TiposDispostivos.TOMADA


    def __post_init__(self):
        self.machine = Machine(model = self, states = ["On", "Off"], transitions = transitions, initial = "Off")
        self.hora_tomada_ligou = None
        self.consumo_wh = 0
    

    def on_enter_On(self):
        self.hora_tomada_ligou = datetime.now()


    def on_enter_Off(self):
        hora_tomada_desligou = datetime.now()
        horas_ligada = ((hora_tomada_desligou - self.hora_tomada_ligou).total_seconds() / 3600)
        self.consumo_wh = abs(self.potencia_w * horas_ligada)



if __name__ == '__main__':
    
    tomada = Tomada("tomada_tv", "tomada da tv", 220)
    print(tomada.potencia_w)
    tomada.ligar()
    print(tomada.state)
    print(tomada.hora_tomada_ligou)
    sleep(4)
    tomada.desligar()
    print(tomada.consumo_wh)
    print(tomada.state)