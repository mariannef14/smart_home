from transitions import Machine
from dataclasses import dataclass, field

from smart_home.core.validators import PorcentagemValidator
from smart_home.core.dispositivos import TiposDispostivos
from smart_home.core.dispositivos import Dispositivo


transitions = [

    {
        "trigger": "abrir",
        "source": "Closed",
        "dest": "Open"

    },

    {
        "trigger": "definir_porcentagem_abertura",
        "source": "Open",
        "dest": "Open",
        "after": "porcentagem_abertura"

    },

    {
        "trigger": "fechar",
        "source": "Open",
        "dest": "Closed"
    }
    
]


@dataclass
class Persiana(Dispositivo):

    id:str
    nome:str
    tipo = TiposDispostivos.PERSIANA
    porcentagem_aberta:int = field(default = PorcentagemValidator())


    def __post_init__(self):
        self.machine = Machine(model = self, states = ["Open", "Closed"], transitions = transitions, initial = "Closed", auto_transitions = False)
    

    def on_enter_Closed(self):
        self.porcentagem_aberta = 0
    

    def porcentagem_abertura(self, value):
        self.porcentagem_aberta = value


    def __str__(self):
        return super().__str__() + f" | {self.state}"



if __name__ == "__main__":

    persiana = Persiana("persiana_quarto", "persiana do quarto")
    persiana.abrir()
    print(persiana.state)
    persiana.definir_porcentagem_abertura(value = 10)
    print(persiana.state)
    print(f"Persiana com {persiana.porcentagem_aberta}% aberta")
    persiana.fechar()
    print(persiana.state)
    print(persiana.porcentagem_aberta)