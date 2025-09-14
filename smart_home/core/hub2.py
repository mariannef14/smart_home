from transitions import Machine
from dataclasses import dataclass, field
from typing import List

from smart_home.core.dispositivos import TiposDispostivos, CorEnum, StatesPorta
from smart_home.dispositivos.porta import Porta
from smart_home.dispositivos.luz import Luz
from smart_home.dispositivos.tomada import Tomada
from smart_home.dispositivos.irrigador import Irrigador
from smart_home.dispositivos.persiana import Persiana
from smart_home.dispositivos.camera import Camera

from smart_home.core.logger import Logger


@dataclass
class Hub:

    dispositivos:List = field(default_factory = list)

    
    def adicionar_dispositivo(self):
        dispositivo = None

        print("Tipos suportados:", TiposDispostivos.all_dispositives())
        tipo_dispositivo = input("Tipo do dispositivo: ").upper().strip()
        id_dispositivo = input("Id (sem espacos): ").lower().strip()
        nome_dispositivo = input("Nome: ")


        if tipo_dispositivo == TiposDispostivos.PORTA.name:
            dispositivo = Porta(id_dispositivo, nome_dispositivo)
            self.dispositivos.append(dispositivo)
        

        elif tipo_dispositivo == TiposDispostivos.LUZ.name:

            brilho_luz = input("Digite o valor do brilho (0-100): ")
            cor_luz = input(f"Digite a cor [{CorEnum.all_colors()}]: ")
            brilho_luz = 50 if brilho_luz == "" else brilho_luz
            cor_luz = "NEUTRA" if cor_luz == "" else cor_luz

            dispositivo = Luz(id_dispositivo, nome_dispositivo, int(brilho_luz), cor_luz)

            self.dispositivos.append(dispositivo)
        

        elif tipo_dispositivo == TiposDispostivos.TOMADA.name:
            potencia_w = int(input("Potência da tomada: "))
            dispositivo = Tomada(id_dispositivo, nome_dispositivo, potencia_w)
            self.dispositivos.append(dispositivo)
        

        elif tipo_dispositivo == TiposDispostivos.IRRIGADOR.name:
            dispositivo = Irrigador(id_dispositivo, nome_dispositivo)
            self.dispositivos.append(dispositivo)
        

        elif tipo_dispositivo == TiposDispostivos.PERSIANA.name:
            porcentagem = int(input("Deseja abrir quantos porcentos da persiana? (0-100): "))
            dispositivo = Persiana(id_dispositivo, nome_dispositivo, porcentagem)
            self.dispositivos.append(dispositivo)
        
        elif tipo_dispositivo == TiposDispostivos.CAMERA.name:
            dispositivo = Camera(id_dispositivo, nome_dispositivo)
            self.dispositivos.append(dispositivo)
        
        else:
            #TODO: LANÇAR EXCEÇÃO PERSONALIZADA PARA TIPO DE DISPOSITIVO INVÁLIDO(ConfigInvalida)
            ...
        
        logger = Logger()
        logger.evento(dispositivo, "adicionar")


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


    def alterar_atributo(self):
        print("Atributos que podem ser modificados [LUZ]: brilho e cor, [PERSIANA]: porcentagem de abertura(abertura)")
        dispositivo = self.mostrar_dispositivo()

        if dispositivo.tipo == TiposDispostivos.LUZ or dispositivo.tipo == TiposDispostivos.PERSIANA: 


            argumentos = input("Argumentos (k=v separados por espaco) ou ENTER: ")


            if argumentos != "":
                    argumentos_dict = dict(argumento.split("=") for argumento in argumentos.split())

                    #TODO: TIRAR ESSE PRINT
                    print(argumentos_dict)
                    self.mudar_atributos(argumentos_dict, dispositivo)

        else:
            raise ValueError("Esse dispositivo não possui atributos que podem ser alterados")


    def executar_rotina(self):

        rotina = input("Digite o tipo de rotina que deseja executar (dormir ou acordar): ").lower().strip()

        for dispositivo in self.dispositivos:

            if rotina == "dormir":

                if isinstance(dispositivo, Porta):
                    
                    state_porta = dispositivo.state

                    while state_porta != StatesPorta.TRANCADA:

                        trigger = dispositivo.machine.get_triggers(dispositivo.state)
                        #TODO: TIRAR ESSE PRINT
                        print(trigger)
                        dispositivo.trigger(trigger[0])
                        state_porta = dispositivo.state
                        #TODO: TIRAR ESSE PRINT
                        print("Status: ", dispositivo.state)
                
                    #TODO: TIRAR ESSE PRINT
                    print("Status final da porta:", dispositivo.state)
                
                if isinstance(dispositivo, Luz):

                    if dispositivo.state == "On":
                        dispositivo.desligar()

                    #TODO: TIRAR ESSE PRINT
                    print("Status final da luz:", dispositivo.state)
                
                if isinstance(dispositivo, Tomada):

                    if dispositivo.state == "On":
                        dispositivo.desligar()
                    
                    #TODO: TIRAR ESSE PRINT
                    print("Status final da tomada:", dispositivo.state)

                if isinstance(dispositivo, Persiana):

                    if dispositivo.state == "Open":
                        dispositivo.fechar()

                    #TODO: TIRAR ESSE PRINT
                    print("Status final da persiana:", dispositivo.state)


            elif rotina == "acordar":
                
                if isinstance(dispositivo, Luz):
                    dispositivo.ligar()
                    dispositivo.definir_brilho(value = 50)
                    #TODO: TIRAR ESSE PRINT
                    print("Status inicial da luz:", dispositivo.state)

                
                if isinstance(dispositivo, Persiana):
                    dispositivo.abrir()
                    dispositivo.definir_porcentagem_abertura(value = 50)
                    #TODO: TIRAR ESSE PRINT
                    print("Status inicial da persiana:", dispositivo.state)

                
                if isinstance(dispositivo, Irrigador):
                    dispositivo.ligar()
                    #TODO: TIRAR ESSE PRINT
                    print("Status inicial do irrigador:", dispositivo.state)
                    dispositivo.irrigar()

        else:
            #TODO: LANÇAR EXCEÇÃO PERSONALIZADA PARA ROTINA NÃO EXISTENTE(ConfigInvalida)
            ...


    def salvar_configuracao(self):
                # dispositivo = {
        #     "id": id_dispostivo,
        #     "tipo": tipo_dispositivo,
        #     "nome": nome_dispositivo,
        #     "estado": 
        # }
        ...




if __name__ == "__main__":
    hub = Hub()
    hub.adicionar_dispositivo()
    # hub.adicionar_dispositivo()
    # hub.adicionar_dispositivo()
    # hub.adicionar_dispositivo()
    # hub.adicionar_dispositivo()
    hub.listar_dispositivos()
    hub.mostrar_dispositivo()
    hub.alterar_atributo()
    hub.executar_comando()
    # hub.executar_comando()
    # hub.remover_dispositivo()
    hub.executar_rotina()
    # hub.executar_rotina()
