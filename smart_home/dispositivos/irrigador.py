from transitions import Machine

from smart_home.core.dispositivos import StatusIrrigador


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


class Irrigador:

    def __init__(self):
        self.machine = Machine(model = self, states = StatusIrrigador, transitions = transitions, initial = StatusIrrigador.DESLIGADO) 
    


if __name__ == "__main__":

    irrigador = Irrigador()
    irrigador.ligar()
    print(irrigador.state)
    irrigador.irrigar()
    print(irrigador.state)
    irrigador.desligar()
    print(irrigador.state)