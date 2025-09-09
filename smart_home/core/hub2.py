from transitions import Machine
from dataclasses import dataclass, field
from typing import List

from smart_home.core.dispositivos import TiposDispostivos
from smart_home.dispositivos.porta import Porta
from smart_home.dispositivos.luz import Luz
from smart_home.dispositivos.tomada import Tomada
from smart_home.dispositivos.irrigador import Irrigador
from smart_home.dispositivos.persiana import Persiana
from smart_home.dispositivos.camera import Camera
from smart_home.core.dispositivos import TiposDispostivos


@dataclass
class Hub:

    dispositivos:List = field(default_factory = list)

    
    def adicionar_dispositivo(self):
        print("Tipos suportados:", TiposDispostivos.all_dispositives())
        tipo_dispositivo = input("Tipo do dispositivo: ").upper().strip()
        id_dispositivo = input("Id (sem espacos): ").lower().strip()
        nome_dispositivo = input("Nome: ")


        if tipo_dispositivo == TiposDispostivos.PORTA.name:
            self.dispositivos.append(Porta(id_dispositivo, nome_dispositivo))
        

        elif tipo_dispositivo == TiposDispostivos.LUZ.name:

            brilho_luz = input("Digite o valor do brilho: ")
            cor_luz = input("Digite a cor: ").upper().strip()
            brilho_luz = 50 if brilho_luz == "" else brilho_luz
            cor_luz = "NEUTRA" if cor_luz == "" else cor_luz

            self.dispositivos.append(Luz(id_dispositivo, nome_dispositivo, int(brilho_luz), cor_luz))
        

        elif tipo_dispositivo == TiposDispostivos.TOMADA.name:
            potencia_w = int(input("Potência da tomada: "))
            self.dispositivos.append(Tomada(id_dispositivo, nome_dispositivo, potencia_w))
        

        elif tipo_dispositivo == TiposDispostivos.IRRIGADOR.name:
            self.dispositivos.append(Irrigador(id_dispositivo, nome_dispositivo))
        

        elif tipo_dispositivo == TiposDispostivos.PERSIANA.name:
            porcentagem = int(input("Deseja abrir quantos porcentos da persiana?"))
            self.dispositivos.append(Persiana(id_dispositivo, nome_dispositivo, porcentagem))
        
        elif tipo_dispositivo == TiposDispostivos.CAMERA.name:
            self.dispositivos.append(Camera(id_dispositivo, nome_dispositivo))
    

    def mostrar_dispositivo(self):

        id_dispositivo = input("Digite o id do dispositivo:")
        encontrou = False
        
        for dispositivo in self.dispositivos:
            
            if dispositivo.id == id_dispositivo.lower().strip():
                print(dispositivo)
                encontrou = True

        if encontrou == False: 
            #TODO: LANÇAR EXCEÇÃO PERSONALIZADA PARA DISPOSITIVO NÃO ENCONTRADO
            print("Não encontrou")


    def listar_dispositivos(self):
        
        for dispositivo in self.dispositivos:
            print(dispositivo)


    def remover_dispositivo(self):

        id_dispositivo = self.mostrar_dispositivo()
        print(id_dispositivo)

        for dispositivo in self.dispositivos:
            
            if dispositivo.id == id_dispositivo.lower().strip():
                print(self.dispositivos[dispositivo]) #ver se printa o dispositivo correto
                # self.dispositivos.remove(dispositivo)
                # del[dispositivo]
                dispositivo.remove(id_dispositivo)


    def executar_comando(self):

        id_dispositivo = input("Id do dispositivo: ")

        # print(self.mostrar_dispositivo(id_dispositivo).strip().split("|")[3].get_triggers())
        comando = input("Comando: ")
        argumentos = input("Argumentos (k=v separados por espaco) ou ENTER: ")


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



if __name__ == "__main__":
    hub = Hub()
    hub.adicionar_dispositivo()
    # hub.adicionar_dispositivo()
    # hub.listar_dispositivos()
    # hub.mostrar_dispositivo()
    hub.remover_dispositivo()
    # hub.executar_comando()
    # hub.remover_dispositivo()