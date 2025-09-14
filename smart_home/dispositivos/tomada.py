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

    _potencia_w:int = PotenciaValidator()
    tipo:TiposDispostivos = field(init = False, default = TiposDispostivos.TOMADA)


    def __post_init__(self):
        self.machine = Machine(model = self, states = ["On", "Off"], transitions = transitions, initial = "Off", auto_transitions = False)
        self.hora_tomada_ligou = None
        self._consumo_wh = 0
    
    
    @property
    def potencia_w(self):
        return self._potencia_w


    @property
    def consumo_wh(self):
        return self._consumo_wh
    

    def on_enter_On(self):
        self.hora_tomada_ligou = datetime.now()


    def on_enter_Off(self):
        hora_tomada_desligou = datetime.now()
        horas_ligada = ((hora_tomada_desligou - self.hora_tomada_ligou).total_seconds() / 3600)
        self._consumo_wh = abs(self._potencia_w * horas_ligada)



if __name__ == '__main__':
    
    tomada = Tomada("tomada_tv", "tomada da tv", 220)
    print("Id:", tomada.id)
    print("Tipo do dispositivo:", tomada.tipo)
    print("Potência: ", tomada.potencia_w)
    tomada.ligar()
    print("Status:", tomada.state)
    print(tomada.hora_tomada_ligou)
    sleep(4)
    tomada.desligar()
    print("Consumo total:", tomada.consumo_wh)
    print("Status:", tomada.state)


    if tomada.state != "On":
        tomada.desligar()