from transitions import Machine

from smart_home.core.dispositivos import StatusIrrigador, TiposDispostivos


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

    def __init__(self, id = "", nome = ""):
        self.machine = Machine(model = self, states = StatusIrrigador, transitions = transitions, initial = StatusIrrigador.DESLIGADO) 
        self.id = id
        self.nome = nome
        self.tipo = TiposDispostivos.IRRIGADOR
        

    def on_enter_IRRIGANDO(self):

        for i in range(2):
            print(f"Irrigando Plantas há {i+1} hora...")
        
        self.desligar()
    


if __name__ == "__main__":

    irrigador = Irrigador()
    irrigador.ligar()
    print(irrigador.state)
    irrigador.irrigar()
    print(irrigador.state)
    if irrigador.state.name == "IRRIGANDO":
        irrigador.desligar()
        print(irrigador.state)