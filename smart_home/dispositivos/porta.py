from transitions import Machine
from transitions.core import MachineError

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

class Porta(Dispositivo):

    def __init__(self, id:str, nome:str):
        super().__init__(id, nome)
        self.machine = Machine(model = self, states = StatesPorta, transitions = transitions, initial = StatesPorta.TRANCADA, on_exception = "machine_error", send_event = True)
        # self.id = id
        # self.nome = nome
        self.tipo = TiposDispostivos.PORTA
        self.tentativas_invalidas = 0
    

    def machine_error(self, event):

        if event.state.name == "ABERTA" and event.event.name == "trancar": 

            self.tentativas_invalidas += 1

        print(event.error)

        #TODO: lançar o raise quando estiver com o menu com o tratamento do try
        raise MachineError(event)
        

if __name__ == '__main__':

    porta = Porta("porta_sala", "porta da sala")
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