from transitions import Machine

from smart_home.core.dispositivos import StatusCamera, TiposDispostivos


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


class Camera:

    def __init__(self, id = "", nome = ""):
        self.machine = Machine(model = self, states = StatusCamera, transitions = transitions, initial = StatusCamera.OFF)
        self.id = id
        self.nome = nome
        self.tipo_dispositivo = TiposDispostivos.CAMERA
    


if __name__ == '__main__':

    camera = Camera()
    camera.ligar()
    print(camera.state)
    camera.gravar()
    print(camera.state)
    camera.parar_gravar()
    print(camera.state)
    print(camera.bateria)
    camera.desligar()
    print(camera.state)