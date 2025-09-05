from enum import Enum
from transitions import Machine
from transitions.core import MachineError


class StatesPorta(Enum):

    TRANCADA = 0
    DESTRANCADA = 1
    ABERTA = 2


    def __str__(self) -> str:
        return self.name


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

class Porta:

    def __init__(self):
        self.machine = Machine(model = self, states = StatesPorta, transitions = transitions, initial = StatesPorta.TRANCADA, on_exception = "machine_error", send_event = True)
        self.tentativas_invalidas = 0
    

    def machine_error(self, event):

        if event.state.name == "ABERTA" and event.event.name == "trancar": 

            self.tentativas_invalidas += 1

        print(event.error)

        #TODO: lançar o raise quando estiver com o menu com o tratamento do try
        # raise MachineError(event)
        

if __name__ == '__main__':

    porta = Porta()
    porta.destrancar()
    print("Status porta", porta.state)
    porta.abrir()
    print("Status porta", porta.state)
    porta.fechar()
    print("Status porta", porta.state)
    porta.trancar()
    print("Status porta", porta.state)
    porta.destrancar()
    print("Status porta", porta.state)
    porta.abrir()
    print("Status porta", porta.state)
    porta.trancar()
    print("Status porta", porta.state)
    print(porta.tentativas_invalidas)