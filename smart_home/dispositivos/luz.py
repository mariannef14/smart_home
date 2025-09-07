from transitions import Machine
from dataclasses import dataclass, field

from smart_home.core.validators import BrilhoValidator, CorValidator
from smart_home.core.dispositivos import CorEnum


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
class Luz:

    brilho:int = field(init = False, default = BrilhoValidator())
    cor:CorEnum = field(init = False, default = CorValidator())


    def __post_init__(self):
        self.machine = Machine(model = self, states = ["Off", "On"], transitions = transitions, initial = "Off")
     

    def mudar_brilho_luz(self):
        
        value = int(input("Digite o valor do brilho: "))

        self.brilho = value

    
    def mudar_cor_luz(self):

        value = input("Digite a cor: ").upper().strip()

        self.cor = value
       


if __name__ == '__main__':

    luz = Luz()
    luz.ligar()
    print("Status luz: ", luz.state)

    luz.definir_brilho()
    print(luz.brilho)

    luz.definir_cor()
    print(luz.cor)

    luz.desligar()
    print("Status luz: ", luz.state)