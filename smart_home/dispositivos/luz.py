from transitions import Machine
from dataclasses import dataclass, field

from smart_home.core.validators import BrilhoValidator, CorValidator
from smart_home.core.dispositivos import CorEnum, TiposDispostivos
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
    },

    {
        "trigger": "definir_brilho",
        "source": "On",
        "dest": "On",
        "after": "mudar_brilho_luz"
    },

    {
        "trigger": "definir_cor",
        "source": "On",
        "dest": "On",
        "after": "mudar_cor_luz"
    }

]


@dataclass
class Luz(Dispositivo):

    _brilho:int =  BrilhoValidator()
    _cor:CorEnum = CorValidator()
    tipo:TiposDispostivos = field(init = False, default = TiposDispostivos.LUZ)


    def __post_init__(self):
        self.machine = Machine(model = self, states = ["Off", "On"], transitions = transitions, initial = "Off", auto_transitions = False)
    

    @property
    def brilho(self):
        return self._brilho
    

    @property
    def cor(self):
        return self._cor


    def mudar_brilho_luz(self, value:int):
        self._brilho = value


    def mudar_cor_luz(self, value:str):
        self._cor = value
    

    def __str__(self):
        return super().__str__() + f" | {self.state}"



if __name__ == '__main__':

    luz = Luz("luz_sala", "luz da sala", 70, "FRIA")
    print("Id:", luz.id)
    print("Tipo do dispositivo:", luz.tipo)
    print("Brilho:", luz.brilho)
    print("Cor:", luz.cor)
    luz.ligar()
    print("Status luz: ", luz.state)

    luz.definir_brilho(value = 50)
    print("Brilho depois da definição:", luz.brilho)

    luz.definir_cor(value = "FRIA")
    print("Cor depois da definição:", luz.cor)

    luz.desligar()
    print("Status luz: ", luz.state)


    if luz.state == "On":
        luz.desligar()