from transitions import Machine
from dataclasses import dataclass, field

from smart_home.core.validators import PorcentagemValidator
from smart_home.core.dispositivos import TiposDispostivos


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
class Persiana:

    porcentagem_aberta:int = field(init = False, default = PorcentagemValidator())


    def __post_init__(self, id = "", nome = ""):
        self.machine = Machine(model = self, states = ["Open", "Closed"], transitions = transitions, initial = "Closed")
        self.id = id
        self.nome = nome
        self.tipo = TiposDispostivos.PERSIANA
        self.porcentagem_aberta = 10


    def on_enter_Closed(self):
        self.porcentagem_aberta = 0
    

    def porcentagem_abertura(self):
        
        porcentagem = int(input("Deseja abrir quantos porcentos da persiana?"))

        self.porcentagem_aberta = porcentagem


if __name__ == "__main__":

    persiana = Persiana()
    persiana.abrir()
    print(persiana.state)
    persiana.definir_porcentagem_abertura()
    print(persiana.state)
    print(f"Persiana com {persiana.porcentagem_aberta}% aberta")
    persiana.fechar()
    print(persiana.state)
    print(persiana.porcentagem_aberta)