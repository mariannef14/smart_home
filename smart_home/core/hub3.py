from transitions import Machine
from dataclasses import dataclass, field
from typing import List
import json
from collections import Counter

from smart_home.core.dispositivos import TiposDispostivos, CorEnum, StatesPorta
from smart_home.dispositivos.porta import Porta
from smart_home.dispositivos.luz import Luz
from smart_home.dispositivos.tomada import Tomada
from smart_home.dispositivos.irrigador import Irrigador
from smart_home.dispositivos.persiana import Persiana
from smart_home.dispositivos.camera import Camera

from smart_home.core.logger import Logger
from smart_home.core.observers import Sujeito, CliObserver


@dataclass
class Hub:

    dispositivos:List = field(default_factory = list)
    logger = Logger()
    sujeito = Sujeito()
    observer = CliObserver()
    sujeito.adicionar_observador(observer)
    dispositivo = None


    def adicionar_dispositivos_json_list(self):

      with open("data/configuracao.json") as file:
        dispositivos = json.load(file)

        for dispositivo in dispositivos.get("dispositivos"):

            if dispositivo.get("tipo") == TiposDispostivos.PORTA.value:
                self.dispositivo = Porta(dispositivo.get("id"), dispositivo.get("nome"))
                self.dispositivos.append(self.dispositivo)
            

            elif dispositivo.get("tipo") == TiposDispostivos.LUZ.value:
                self.dispositivo = Luz(dispositivo.get("id"), dispositivo.get("nome"), dispositivo.get("atributos").get("brilho"), dispositivo.get("atributos").get("cor"))
                self.dispositivos.append(self.dispositivo)
            

            elif dispositivo.get("tipo") == TiposDispostivos.TOMADA.value:
                self.dispositivo = Tomada(dispositivo.get("id"), dispositivo.get("nome"), )
                self.dispositivos.append(self.dispositivo)

        

            elif dispositivo.get("tipo") == TiposDispostivos.IRRIGADOR.value:
                self.dispositivo = Irrigador(dispositivo.get("id"), dispositivo.get("nome"))
                self.dispositivos.append(self.dispositivo)
        

            elif dispositivo.get("tipo") == TiposDispostivos.PERSIANA.value:
                self.dispositivo = Persiana(dispositivo.get("id"), dispositivo.get("nome"), dispositivo.get("atributos").get("percentual_abertura"))
                self.dispositivos.append(self.dispositivo)
            
            elif dispositivo.get("tipo") == TiposDispostivos.CAMERA.value:
                self.dispositivo = Camera(dispositivo.get("id"), dispositivo.get("nome"))
                self.dispositivos.append(self.dispositivo)
        
        #TODO: CHAMAR O OBSERVER QUE VAI ADICIONAR A LISTA DE DISPOSITIVOS(_adicionar_dispositivo_dict)
    def adicionar_dispositivo(self):

        #TODO: VERIFICAR SE O ID NÃO EXISTE, SE EXISTIR LANÇAR EXCEÇÃO
        print("Tipos suportados:", TiposDispostivos.all_dispositives())
        tipo_dispositivo = input("Tipo do dispositivo: ").upper().strip()
        id_dispositivo = input("Id (sem espacos): ").lower().strip()
        nome_dispositivo = input("Nome: ")


        if tipo_dispositivo == TiposDispostivos.PORTA.name:
            self.dispositivo = Porta(id_dispositivo, nome_dispositivo)
            self.dispositivos.append(self.dispositivo)
        

        elif tipo_dispositivo == TiposDispostivos.LUZ.name:

            brilho_luz = input("Digite o valor do brilho (0-100): ")
            cor_luz = input(f"Digite a cor [{CorEnum.all_colors()}]: ")
            brilho_luz = 50 if brilho_luz == "" else brilho_luz
            cor_luz = "NEUTRA" if cor_luz == "" else cor_luz

            self.dispositivo = Luz(id_dispositivo, nome_dispositivo, int(brilho_luz), cor_luz)

            self.dispositivos.append(self.dispositivo)
        

        elif tipo_dispositivo == TiposDispostivos.TOMADA.name:
            potencia_w = int(input("Potência da tomada: "))
            self.dispositivo = Tomada(id_dispositivo, nome_dispositivo, potencia_w)
            self.dispositivos.append(self.dispositivo)
        

        elif tipo_dispositivo == TiposDispostivos.IRRIGADOR.name:
            self.dispositivo = Irrigador(id_dispositivo, nome_dispositivo)
            self.dispositivos.append(self.dispositivo)
        

        elif tipo_dispositivo == TiposDispostivos.PERSIANA.name:
            porcentagem = int(input("Deseja abrir quantos porcentos da persiana? (0-100): "))
            self.dispositivo = Persiana(id_dispositivo, nome_dispositivo, porcentagem)
            self.dispositivos.append(self.dispositivo)
        
        elif tipo_dispositivo == TiposDispostivos.CAMERA.name:
            self.dispositivo = Camera(id_dispositivo, nome_dispositivo)
            self.dispositivos.append(self.dispositivo)
        
        else:
            #TODO: LANÇAR EXCEÇÃO PERSONALIZADA PARA TIPO DE DISPOSITIVO INVÁLIDO(ConfigInvalida)
            raise ValueError
        
        self.logger.evento(self.dispositivo, "adicionar")


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

        self.logger.evento(dispositivo, "remover")
        self.sujeito.notificar("remover", dispositivo)


    def executar_comando(self):

        dispositivo = self.mostrar_dispositivo()
        comandos_possiveis = ",".join(dispositivo.machine.get_triggers(dispositivo.state))
        print(f"Comandos possíveis no estado atual do dispositivo -> {comandos_possiveis}")
        comando = input("Qual comando deseja executar? ")
        #TODO: COLOCAR BLOCO DE MUDAR DE ESTADO DENTRO DE UM TRY CATCH E LANÇAR EXCEÇÃO PERSONALIZADA(TransicaoInvalida)
        
        try:
            dispositivo.trigger(comando)
            #TODO: TIRAR ESSE PRINT
            print(dispositivo.state)
            print("Atributos que podem ser modificados [LUZ]: brilho e cor, [PERSIANA]: porcentagem de abertura(abertura)")
            argumentos = input("Argumentos (k=v separados por espaco) ou ENTER: ")
                
            if argumentos != "":
                argumentos_dict = dict(argumento.split("=") for argumento in argumentos.split())

                #TODO: TIRAR ESSE PRINT
                print(argumentos_dict)
                self.mudar_atributos(argumentos_dict, dispositivo)
            #TODO: TIRAR ESSE PRINT
            print(dispositivo)
            
            self.logger.evento(dispositivo, "executar comando", comando)
            self.sujeito.notificar("executar comando", dispositivo, comando)  
           
        except:
            #TODO: LANÇAR EXCEÇÃO PERSONALIZADA PARA ESTADO INVÁLIDO(TransicaoInvalida)
            raise ValueError()
        
        # else:
            
        #     if dispositivo.tipo == TiposDispostivos.LUZ or dispositivo.tipo == TiposDispostivos.PERSIANA: 

        #         print("Atributos que podem ser modificados [LUZ]: brilho e cor, [PERSIANA]: porcentagem de abertura(abertura)")
        #         argumentos = input("Argumentos (k=v separados por espaco) ou ENTER: ")
                
        #         if argumentos != "":
        #             argumentos_dict = dict(argumento.split("=") for argumento in argumentos.split())

        #             #TODO: TIRAR ESSE PRINT
        #             print(argumentos_dict)
        #             self.mudar_atributos(argumentos_dict, dispositivo)
        #         #TODO: TIRAR ESSE PRINT
        #         print(dispositivo)
            
        #     self.logger.evento(dispositivo, "executar comando", comando)
        #     self.sujeito.notificar("executar comando", dispositivo, comando)    


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

        #TODO: colocar no observer
        with open(file = "data/configuracao.json", mode = "r", encoding = "utf-8") as file:
            dispositivos = json.load(file)
            
            # print(dispositivos["dispositivos"])
            # print(dispositivos["rotinas"].get(rotina))
            # print(dispositivos["rotinas"])
            dispositivos_rotina = dispositivos["rotinas"].get(rotina)
            lista_dispositivos = dispositivos.get("dispositivos")

            # print(lista_dispositivos)

            ids_dispositivos_rotina = [dispositivo.get("id") for dispositivo in dispositivos_rotina]

            for d in lista_dispositivos:
                print(d) 

            # print(ids)

            #TODO: pegar os dispositivos e ver se eles estão cadastrados na rotina
            #se tiver, executa a rotina e salva no arquivo o estado
        # for dispositivo in self.dispositivos:

        #     if rotina == "dormir":

        #         if isinstance(dispositivo, Porta):
                    
        #             state_porta = dispositivo.state

        #             while state_porta != StatesPorta.TRANCADA:

        #                 trigger = dispositivo.machine.get_triggers(dispositivo.state)
        #                 #TODO: TIRAR ESSE PRINT
        #                 print(trigger)
        #                 dispositivo.trigger(trigger[0])
        #                 state_porta = dispositivo.state
        #                 #TODO: TIRAR ESSE PRINT
        #                 print("Status: ", dispositivo.state)
                
        #             #TODO: TIRAR ESSE PRINT
        #             print("Status final da porta:", dispositivo.state)
                
        #         if isinstance(dispositivo, Luz):

        #             if dispositivo.state == "On":
        #                 dispositivo.desligar()

        #             #TODO: TIRAR ESSE PRINT
        #             print("Status final da luz:", dispositivo.state)
                
        #         if isinstance(dispositivo, Tomada):

        #             if dispositivo.state == "On":
        #                 dispositivo.desligar()
                    
        #             #TODO: TIRAR ESSE PRINT
        #             print("Status final da tomada:", dispositivo.state)

        #         if isinstance(dispositivo, Persiana):

        #             if dispositivo.state == "Open":
        #                 dispositivo.fechar()

        #             #TODO: TIRAR ESSE PRINT
        #             print("Status final da persiana:", dispositivo.state)


        #     elif rotina == "acordar":
                
        #         if isinstance(dispositivo, Luz):
        #             dispositivo.ligar()
        #             dispositivo.definir_brilho(value = 50)
        #             #TODO: TIRAR ESSE PRINT
        #             print("Status inicial da luz:", dispositivo.state)

                
        #         if isinstance(dispositivo, Persiana):
        #             dispositivo.abrir()
        #             dispositivo.definir_porcentagem_abertura(value = 50)
        #             #TODO: TIRAR ESSE PRINT
        #             print("Status inicial da persiana:", dispositivo.state)

                
        #         if isinstance(dispositivo, Irrigador):
        #             dispositivo.ligar()
        #             #TODO: TIRAR ESSE PRINT
        #             print("Status inicial do irrigador:", dispositivo.state)
        #             dispositivo.irrigar()

        # else:
        #     #TODO: LANÇAR EXCEÇÃO PERSONALIZADA PARA ROTINA NÃO EXISTENTE(ConfigInvalida)
        #     ...


    def salvar_configuracao(self):
        self.sujeito.notificar("adicionar", self.dispositivo)
        print("Configuração salva")
    

    def salvar_configuracao_lista_dispositivos(self):
        self.sujeito.notificar("adicionar dispositivos", self.dispositivos)
        print("Saindo...")


    def gerar_relatorio(self):

        print("Tipos de relatórios disponíveis: ")
        print("[1] Dispositivos mais usados")

        opcao = int(input("Escolha sua opção: "))

        if opcao == 1:
            self.dispositivos_mais_usados()


    def dispositivos_mais_usados(self):

        with open(file = "data/configuracao.json", mode = "r") as file:
            dispositivos = json.load(file)

            lista_dispositivos = dispositivos.get("dispositivos")

            tipos = [dispositivo.get("tipo") for dispositivo in lista_dispositivos]

            print(sorted(Counter(tipos)))
    



if __name__ == "__main__":
    hub = Hub()
    hub.adicionar_dispositivos_json_list()
    hub.adicionar_dispositivo()
    # hub.adicionar_dispositivo()
    # hub.adicionar_dispositivo()
    # hub.adicionar_dispositivo()
    # hub.adicionar_dispositivo()
    hub.listar_dispositivos()
    # hub.mostrar_dispositivo()
    # hub.alterar_atributo()
    # hub.executar_comando()
    # hub.executar_comando()
    # hub.remover_dispositivo()
    # hub.executar_rotina()
    # hub.executar_rotina()
