from transitions import Machine
from enum import Enum


class BrilhoValidator:

    def __get__(self, instance, owner):
        return getattr(instance, "brilho")
    

    def __set__(self, instance, value):
        
        if value >= 0 and value <= 100:
           setattr(instance, "brilho", value)
        
        else:
            raise ValueError("Valor do brilho precisa estar entre 0 e 100")
        

class CorEnum(Enum):

    NEUTRA = 0,
    FRIA = 1,
    QUENTE = 2


class CorValidator:

    def __get__(self, instance, owner):
        return getattr(instance, "cor")
    

    def __set__(self, instance, value):

        if value.upper() in [cor.name for cor in CorEnum]:
            setattr(instance, "cor", value)

        else:
            raise ValueError("Cor não disponível")


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
        "after": "definir_brilho_luz"
    },

    {
        "trigger": "definir_cor",
        "source": "on",
        "dest": "on",
        "after": "definir_cor_luz"
    }

]


class Luz:

    def __init__(self):
        self.machine = Machine(model = self, states = ["Off", "On"], transitions = transitions, initial = "Off")
        self.brilho = BrilhoValidator()
        self.cor = CorValidator()

    #TODO: verificar se a luz está ligada
    def definir_brilho_luz(self, value):
        self.brilho = value
    
    
    def definir_cor_luz(self, value):
        self.cor = value



if __name__ == '__main__':

    luz = Luz()
    luz.ligar()
    print("Status luz", luz.state)
    luz.definir_brilho(20)
    print("Status luz", luz.state)
    luz.definir_cor_luz("fria")
    print("Status luz", luz.state)
    print("Brilho: ", luz.brilho)
    print("Cor", luz.cor)
    luz.definir_brilho(101)
    luz.desligar()
    print("Status luz", luz.state)


