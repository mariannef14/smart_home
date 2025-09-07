from transitions import Machine


class PotenciaValidator:

    def __get__(self, instance, owner):
        return getattr(instance, self.private_name)


    def __set__(self, instance, value):
        
        if value >= 0:
            setattr(instance, self.private_name, value)


    def __set_name__(self, owner, name):
        self.private_name = "_" + name


transitions = [

    {
        "trigger": "ligar",
        "source": "Off",
        "dest": "On",
        "after": "registro_consumo"
    },

    {
        "trigger": "desligar",
        "source": "On",
        "dest": "Off",
        "after": "registro_consumo"
    }

]


class Tomada:

    def __init__(self, potencia):
        self.machine = Machine(model = self, states = ["On", "Off"], transitions = transitions, initial = "Off")
        self.potencia_w = PotenciaValidator()
        self.consumo_wh = 0
    
    #TODO: calcular consumo
    def registro_consumo(self):
        
        continue_ = True
        horas_ligada = 0

        while continue_:

            if self.state == "Off":
                self.consumo_wh = self.potencia_w * (horas_ligada / 60)
                break
            
            # else:
            #     return registro_consumo()
            horas_ligada += 30



if __name__ == '__main__':
    
    tomada = Tomada(50)
    tomada.ligar()
    print(tomada.state)
    tomada.desligar()
    print(tomada.consumo_wh)
    print(tomada.state)
