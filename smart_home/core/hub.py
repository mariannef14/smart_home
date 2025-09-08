from transitions import Machine

from smart_home.dispositivos import Porta, Luz, Tomada, Persiana


class Hub:

    def __init__(self, porta = None, luz = None, tomada = None, camera = None, irrigador = None, persiana = None):
        self.porta = porta
        self.luz = luz
        self.tomada = tomada
        self.camera = camera
        self.irrigador = irrigador
        self.persiana = persiana
        self.FMS = []

        for dispositivo in self.__dict__():
            if dispositivo is not None:
                self.FMS.append(dispositivo)
        #self.FMS = [self.porta, self.luz, self.tomada, self.camera, self.irrigador, self.persiana]
    

    @property
    def dispositivos_da_casa(self):
        return self.FMS


    def rotinas(self, tipo_rotina:str):

        for dispositivo in self.FMS:

            if tipo_rotina.lower().strip() == "modo_noite":

                if isinstance(dispositivo, Porta):
                    dispositivo.trancar()
                
                if isinstance(dispositivo, Luz):
                    dispositivo.desligar()
                
                if isinstance(dispositivo, Tomada):
                    dispositivo.desligar()
                
                if isinstance(dispositivo, Persiana):
                    dispositivo.fechar()

            elif tipo_rotina.lower().strip() == "acordar":
                
                if isinstance(dispositivo, Luz):
                    dispositivo.ligar()
                
                if isinstance(dispositivo, Persiana):
                    dispositivo.abrir()

