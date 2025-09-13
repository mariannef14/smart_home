from transitions import Machine
from dataclasses import dataclass, field

from smart_home.core.dispositivos import StatusIrrigador, TiposDispostivos
from smart_home.core.dispositivos import Dispositivo


transitions = [

    {
        "trigger": "ligar",
        "source": StatusIrrigador.DESLIGADO,
        "dest": StatusIrrigador.LIGADO
    },

    {
        "trigger": "irrigar",
        "source": StatusIrrigador.LIGADO,
        "dest": StatusIrrigador.IRRIGANDO
    },

    {
        "trigger": "desligar",
        "source": [StatusIrrigador.LIGADO, StatusIrrigador.IRRIGANDO],
        "dest": StatusIrrigador.DESLIGADO
    }

]


@dataclass
class Irrigador(Dispositivo):

    tipo:TiposDispostivos = field(init = False, default = TiposDispostivos.IRRIGADOR)


    def __post_init__(self):
        self.machine = Machine(model = self, states = StatusIrrigador, transitions = transitions, initial = StatusIrrigador.DESLIGADO, auto_transitions = False)


    def __str__(self):
        return super().__str__() + f" | {self.state}"
        

    def on_enter_IRRIGANDO(self):

        for i in range(2):
            print(f"Irrigando Plantas há {i+1}h...")
        
        self.desligar()
    


if __name__ == "__main__":

    irrigador = Irrigador("irrigador_jardim", "irrigador do jardim")
    print("Id", irrigador.id)
    print("Tipo do dispositivo:", irrigador.tipo)
    irrigador.ligar()
    print("Status:", irrigador.state)
    irrigador.irrigar()
    print("Status:", irrigador.state)