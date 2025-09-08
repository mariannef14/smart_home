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

    id:str
    nome:str
    # brilho:int = field(init = False, default = BrilhoValidator())
    brilho:int = field(default = BrilhoValidator())
    # cor:CorEnum = field(init= False, default = CorValidator())
    cor:CorEnum = field(default = CorValidator())

    #TODO: CRIAR __INIT__ PARA ADICIONAR VALOR PADRÃO??

    def __post_init__(self):
        self.machine = Machine(model = self, states = ["Off", "On"], transitions = transitions, initial = "Off")
        # self.brilho = 35
        # self.cor = "neutra"
        self.tipo = TiposDispostivos.LUZ
     

    def mudar_brilho_luz(self, value:int):
        
        # value = int(input("Digite o valor do brilho: "))

        self.brilho = value

    
    def mudar_cor_luz(self, value:str):

        # value = input("Digite a cor: ").upper().strip()

        self.cor = value
       


if __name__ == '__main__':

    luz = Luz("luz_sala", "luz da sala")
    print(luz.brilho)
    print(luz.cor)
    luz.ligar()
    print("Status luz: ", luz.state)

    luz.definir_brilho(value = 50)
    print(luz.brilho)

    luz.definir_cor(value = "fria")
    print(luz.cor)

    luz.desligar()
    print("Status luz: ", luz.state)