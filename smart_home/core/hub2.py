from transitions import Machine
from dataclasses import dataclass, field, asdict
from typing import List

from smart_home.core.dispositivos import TiposDispostivos, CorEnum
from smart_home.dispositivos.porta import Porta
from smart_home.dispositivos.luz import Luz
from smart_home.dispositivos.tomada import Tomada
from smart_home.dispositivos.irrigador import Irrigador
from smart_home.dispositivos.persiana import Persiana
from smart_home.dispositivos.camera import Camera


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

            brilho_luz = input("Digite o valor do brilho (0-100): ")
            cor_luz = input(f"Digite a cor [{CorEnum.all_colors()}]: ")
            brilho_luz = 50 if brilho_luz == "" else brilho_luz
            cor_luz = "NEUTRA" if cor_luz == "" else cor_luz

            self.dispositivos.append(Luz(id_dispositivo, nome_dispositivo, int(brilho_luz), cor_luz))
        

        elif tipo_dispositivo == TiposDispostivos.TOMADA.name:
            potencia_w = int(input("Potência da tomada: "))
            self.dispositivos.append(Tomada(id_dispositivo, nome_dispositivo, potencia_w))
        

        elif tipo_dispositivo == TiposDispostivos.IRRIGADOR.name:
            self.dispositivos.append(Irrigador(id_dispositivo, nome_dispositivo))
        

        elif tipo_dispositivo == TiposDispostivos.PERSIANA.name:
            porcentagem = int(input("Deseja abrir quantos porcentos da persiana? (0-100): "))
            self.dispositivos.append(Persiana(id_dispositivo, nome_dispositivo, porcentagem))
        
        elif tipo_dispositivo == TiposDispostivos.CAMERA.name:
            self.dispositivos.append(Camera(id_dispositivo, nome_dispositivo))
    

    def mostrar_dispositivo(self):

        id_dispositivo = input("Digite o id do dispositivo: ")
        
        for dispositivo in self.dispositivos:
            
            if dispositivo.id == id_dispositivo.lower().strip():
                return dispositivo

        #TODO: LANÇAR EXCEÇÃO PERSONALIZADA PARA DISPOSITIVO NÃO ENCONTRADO
        raise ValueError("Não encontrou")


    def listar_dispositivos(self):
        
        for dispositivo in self.dispositivos:
            print(dispositivo)


    def remover_dispositivo(self):

        dispositivo = self.mostrar_dispositivo()
        index = self.dispositivos.index(dispositivo)
        self.dispositivos.pop(index)


    def executar_comando(self):

        dispositivo = self.mostrar_dispositivo()
        comandos_possiveis = ",".join(dispositivo.machine.get_triggers(dispositivo.state))
        print(f"Comandos possíveis no estado atual do dispositivo -> {comandos_possiveis}")
        comando = input("Qual comando deseja executar? ")
        #TODO: COLOCAR BLOCO DE MUDAR DE ESTADO DENTRO DE UM TRY CATCH E LANÇAR EXCEÇÃO PERSONALIZADA(TransicaoInvalida)
        dispositivo.trigger(comando)
        #TODO: TIRAR ESSE PRINT
        print(dispositivo.state)

        if dispositivo.tipo == TiposDispostivos.LUZ or dispositivo.tipo == TiposDispostivos.PERSIANA: 

            print("Atributos que podem ser modificados [LUZ]: brilho e cor, [PERSIANA]: porcentagem de abertura(abertura)")
            argumentos = input("Argumentos (k=v separados por espaco) ou ENTER: ")
            
            if argumentos != "":
                argumentos_dict = dict(argumento.split("=") for argumento in argumentos.split())

                #TODO: TIRAR ESSE PRINT
                print(argumentos_dict)
                self.mudar_atributos(argumentos_dict, dispositivo)
            #TODO: TIRAR ESSE PRINT
            print(dispositivo)
                

    def mudar_atributos(self, argumentos, dispositivo):

        if "brilho" in argumentos:
            dispositivo.definir_brilho(value = int(argumentos.get("brilho")))
            #TODO: TIRAR ESSE PRINT
            print(dispositivo.brilho)
        
        if "cor" in argumentos:
            dispositivo.definir_cor(value = argumentos.get("cor"))
            #TODO: TIRAR ESSE PRINT
            print(dispositivo.cor)
        
        if "abertura" in argumentos:
            dispositivo.definir_porcentagem_abertura(value = int(argumentos.get("abertura")))
            #TODO: TIRAR ESSE PRINT
            print(dispositivo.percentual_abertura)


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
    hub.executar_comando()
    # hub.remover_dispositivo()
    # hub.remover_dispositivo()