from transitions import Machine

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


class Camera(Dispositivo):

    def __init__(self, id:str, nome:str):
        self.machine = Machine(model = self, states = StatusCamera, transitions = transitions, initial = StatusCamera.OFF)
        super().__init__(id, nome)
        # self.id = id
        # self.nome = nome
        self.tipo_dispositivo = TiposDispostivos.CAMERA
    


if __name__ == '__main__':

    camera = Camera("camera_quintal", "camera do quintal")
    camera.ligar()
    print(camera.state)
    camera.gravar()
    print(camera.state)
    camera.parar_gravar()
    print(camera.state)
    camera.desligar()
    print(camera.state)