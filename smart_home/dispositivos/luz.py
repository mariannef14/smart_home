from transitions import Machine
from enum import Enum
from dataclasses import dataclass, field


class BrilhoValidator:

    def __get__(self, instance, owner):
        return getattr(instance, self.private_name)
    

    def __set__(self, instance, value):
        
        if value >= 0 and value <= 100:
           setattr(instance, self.private_name, value)
        
        else:
            raise ValueError("Valor do brilho precisa estar entre 0 e 100")
    

    def __set_name__(self, owner, name):
        self.private_name = "_" + name


class CorEnum(Enum):

    NEUTRA = 0,
    FRIA = 1,
    QUENTE = 2


class CorValidator:

    def __get__(self, instance, owner):
        return getattr(instance, self.private_name)
    

    def __set__(self, instance, value):

        if value.upper() in [cor.name for cor in CorEnum]:
            setattr(instance, self.private_name, value)

        else:
            raise ValueError(f"A cor {value} não existe")
    

    def __set_name__(self, owner, name):
        self.private_name = "_" + name


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
        "after": "mudar_brilho_luz"
    },

    {
        "trigger": "definir_cor",
        "source": "On",
        "dest": "On",
        "after": "mudar_cor_luz"
    }

]


class Luz:

    def __init__(self):
        self.machine = Machine(model = self, states = ["Off", "On"], transitions = transitions, initial = "Off")
        self.brilho = BrilhoValidator()
        self.cor = CorValidator()
    

    def mudar_brilho_luz(self):
        
        value = int(input("Digite o valor do brilho: "))

        if value < 0 or value > 100:
            raise ValueError("Valor do brilho precisa estar entre 0 e 100")

        self.brilho = value

    
    def mudar_cor_luz(self):

        value = input("Digite a cor: ").upper().strip()

        if value in [cor.name for cor in CorEnum]:
            self.cor = value
        
        else:
            raise ValueError(f"A cor de luz {value} não existe")

       

if __name__ == '__main__':

    luz = Luz()
    luz.ligar()
    print("Status luz: ", luz.state)

    luz.definir_brilho()
    print(luz.brilho)

    luz.definir_cor()
    print(luz.cor)

    luz.desligar()
    print("Status luz: ", luz.state)