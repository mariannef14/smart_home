import time
from transitions import Machine

from smart_home.core.dispositivos import StatusCamera


transitions = [

    {
        "trigger": "ligar",
        "source": StatusCamera.OFF,
        "dest": StatusCamera.ON,
    },

    {
        "trigger": "gravar",
        "source": StatusCamera.ON,
        "dest": StatusCamera.GRAVANDO,
        "conditions": ["tem_bateria"]

    },

    {
        "trigger": "parar_gravar",
        "source": StatusCamera.GRAVANDO,
        "dest": StatusCamera.STOP
    },

    {
        "trigger": "desligar",
        "source": [StatusCamera.STOP, StatusCamera.ON],
        "dest": StatusCamera.OFF
    }

]


class Camera:

    def __init__(self, bateria = 50):
        self.machine = Machine(model = self, states = StatusCamera, transitions = transitions, initial = StatusCamera.OFF)
        self.bateria = bateria
    

    def tem_bateria(self):
        return self.bateria > 15
    

    def on_enter_GRAVANDO(self):

        tempo_horas = int(input("Digite a quantidade de tempo em horas que a câmera irá gravar:"))

        for t in range(tempo_horas):

            if self.bateria > 15:
                print("Gravando...")
                self.bateria -= 5
            
            else:
                print("Bateria em 15%. A gravação será interrompida em alguns segundos...")
                time.sleep(2)
                self.parar_gravar()
                break



if __name__ == '__main__':

    camera = Camera()
    camera.ligar()
    print(camera.state)
    camera.gravar()
    print(camera.state)
    if camera.state == StatusCamera.GRAVANDO:
        camera.parar_gravar()
        print(camera.state)
    print(camera.bateria)
    camera.desligar()
    print(camera.state)