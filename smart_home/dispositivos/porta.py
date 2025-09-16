from transitions import Machine
from transitions.core import MachineError
from dataclasses import dataclass, field

from smart_home.core.dispositivos import StatesPorta, TiposDispostivos
from smart_home.core.dispositivos import Dispositivo


transitions = [

    {
       "trigger": "destrancar",
       "source": StatesPorta.TRANCADA,
       "dest": StatesPorta.DESTRANCADA
    },

    {
        "trigger": "trancar",
        "source": StatesPorta.DESTRANCADA,
        "dest": StatesPorta.TRANCADA,
    },

    {
        "trigger": "abrir",
        "source": StatesPorta.DESTRANCADA,
        "dest": StatesPorta.ABERTA
    },


    {
        "trigger": "fechar",
        "source": StatesPorta.ABERTA,
        "dest": StatesPorta.DESTRANCADA
    }

]


@dataclass
class Porta(Dispositivo):

    tipo:TiposDispostivos = field(init = False, default = TiposDispostivos.PORTA)   


    def __post_init__(self):
        self.machine = Machine(model = self, states = StatesPorta, transitions = transitions, initial = StatesPorta.TRANCADA, auto_transitions = False, on_exception = "machine_error", send_event = True)
        self.__tentativas_invalidas = 0
    

    def machine_error(self, event):

        if event.state.name == "ABERTA" and event.event.name == "trancar": 

            self.__tentativas_invalidas += 1

        raise MachineError(event)
    

    @property
    def quantidade_tentativas_invalidas(self):
        return self.__tentativas_invalidas
    

    def __str__(self):
        return super().__str__() + f" | {self.state}"



if __name__ == '__main__':

    porta = Porta("porta_sala", "porta da sala")
    print("Id:", porta.id)
    print("Tipo do dispositivo:", porta.tipo)
    porta.destrancar()
    print("Status: ", porta.state)
    porta.abrir()
    print("Status: ", porta.state)
    # porta.fechar()
    # print("Status: ", porta.state)
    # porta.trancar()
    # print("Status: ", porta.state)
    # porta.destrancar()
    # print("Status: ", porta.state)
    # porta.abrir()
    # print("Status: ", porta.state)
    # porta.trancar()
    # print("Status: ", porta.state)
    # print(porta.quantidade_tentativas_invalidas)

    state_porta = porta.state

    while state_porta != StatesPorta.TRANCADA:
        if state_porta == StatesPorta.TRANCADA:
            print("Porta trancada")
        trigger = porta.machine.get_triggers(porta.state)
        print(trigger)
        porta.trigger(trigger[0])
        state_porta = porta.state
        print("Status: ", porta.state)