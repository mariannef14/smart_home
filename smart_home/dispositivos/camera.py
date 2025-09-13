from transitions import Machine
from dataclasses import dataclass, field

from smart_home.core.dispositivos import StatusCamera, TiposDispostivos
from smart_home.core.dispositivos import Dispositivo


transitions = [

    {
        "trigger": "ligar",
        "source": StatusCamera.OFF,
        "dest": StatusCamera.ON,
    },

    {
        "trigger": "gravar",
        "source": StatusCamera.ON,
        "dest": StatusCamera.GRAVANDO

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


@dataclass
class Camera(Dispositivo):

    tipo:TiposDispostivos = field(init = False, default = TiposDispostivos.CAMERA)


    def __post_init__(self):
        self.machine = Machine(model = self, states = StatusCamera, transitions = transitions, initial = StatusCamera.OFF, auto_transitions = False)    

    def __str__(self):
        return super().__str__() + f" | {self.state}"



if __name__ == '__main__':

    camera = Camera("camera_quintal", "camera do quintal")
    print("Id:", camera.id)
    print("Tipo do dispositivo:", camera.tipo)
    camera.ligar()
    print("Status:", camera.state)
    camera.gravar()
    print("Status:", camera.state)
    camera.parar_gravar()
    print("Status:", camera.state)
    camera.desligar()
    print("Status:", camera.state)