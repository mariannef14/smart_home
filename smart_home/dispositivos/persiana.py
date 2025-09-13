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

    tipo:TiposDispostivos = field(init = False, default = TiposDispostivos.PERSIANA)
    _percentual_abertura:int = field(init = False, default = PorcentagemValidator())


    def __post_init__(self):
        self.machine = Machine(model = self, states = ["Open", "Closed"], transitions = transitions, initial = "Closed", auto_transitions = False)
    

    @property
    def percentual_abertura(self):
        return self._percentual_abertura


    def on_enter_Closed(self):
        self._percentual_abertura = 0
    

    def porcentagem_abertura(self, value):
        self._percentual_abertura = value


    def __str__(self):
        return super().__str__() + f" | {self.state}"



if __name__ == "__main__":

    persiana = Persiana("persiana_quarto", "persiana do quarto")
    print("Id:", persiana.id)
    print("Tipo do dispositivo:", persiana.tipo)
    persiana.abrir()
    print("Status:", persiana.state)
    persiana.definir_porcentagem_abertura(value = 15)
    print("Status:", persiana.state)
    print(f"Persiana com {persiana.percentual_abertura}% aberta")
    persiana.fechar()
    print("Status:", persiana.state)
    print(f"Persiana com {persiana.percentual_abertura}% aberta")