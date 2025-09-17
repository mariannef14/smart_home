from dataclasses import dataclass, field
from datetime import datetime
from typing import List
import json
import csv
from functools import reduce
from transitions import MachineError
from collections import Counter

from smart_home.core.dispositivos import TiposDispostivos, CorEnum
from smart_home.dispositivos.porta import Porta
from smart_home.dispositivos.luz import Luz
from smart_home.dispositivos.tomada import Tomada
from smart_home.dispositivos.irrigador import Irrigador
from smart_home.dispositivos.persiana import Persiana
from smart_home.dispositivos.camera import Camera

from smart_home.core.logger import Logger
from smart_home.core.observers import Sujeito, CliObserver

from smart_home.core.erros import ConfigInvalida, DispositivoNaoExiste, TransicaoInvalida, ValidacaoAtributo


@dataclass
class Hub:

    dispositivos:List = field(default_factory = list)
    logger = Logger()
    sujeito = Sujeito()
    observer = CliObserver()
    sujeito.adicionar_observador(observer)
    dispositivo = None


    def adicionar_dispositivos_json_in_list(self):

      with open("data/configuracao.json") as file:

        dispositivos = json.load(file)

        for dispositivo in dispositivos.get("dispositivos"):

            if dispositivo.get("tipo") == TiposDispostivos.PORTA.value:
                self.dispositivo = Porta(dispositivo.get("id"), dispositivo.get("nome"))
                self._set_state_dispositivo(dispositivo.get("estado"), self.dispositivo)
                self.dispositivos.append(self.dispositivo)

            elif dispositivo.get("tipo") == TiposDispostivos.LUZ.value:
                self.dispositivo = Luz(dispositivo.get("id"), dispositivo.get("nome"), dispositivo.get("atributos").get("brilho"), dispositivo.get("atributos").get("cor"))
                self._set_state_dispositivo(dispositivo.get("estado"), self.dispositivo)
                self.dispositivos.append(self.dispositivo)

            elif dispositivo.get("tipo") == TiposDispostivos.TOMADA.value:
                self.dispositivo = Tomada(dispositivo.get("id"), dispositivo.get("nome"), dispositivo.get("atributos").get("potencia"))
                self._set_state_dispositivo(dispositivo.get("estado"), self.dispositivo)
                self.dispositivos.append(self.dispositivo)

            elif dispositivo.get("tipo") == TiposDispostivos.IRRIGADOR.value:
                self.dispositivo = Irrigador(dispositivo.get("id"), dispositivo.get("nome"))
                self._set_state_dispositivo(dispositivo.get("estado"), self.dispositivo)
                self.dispositivos.append(self.dispositivo)
    
            elif dispositivo.get("tipo") == TiposDispostivos.PERSIANA.value:
                self.dispositivo = Persiana(dispositivo.get("id"), dispositivo.get("nome"), dispositivo.get("atributos").get("percentual_abertura"))
                self._set_state_dispositivo(dispositivo.get("estado"), self.dispositivo)
                self.dispositivos.append(self.dispositivo)
            
            elif dispositivo.get("tipo") == TiposDispostivos.CAMERA.value:
                self.dispositivo = Camera(dispositivo.get("id"), dispositivo.get("nome"))
                self._set_state_dispositivo(dispositivo.get("estado"), self.dispositivo)
                self.dispositivos.append(self.dispositivo)
        
    
    def _set_state_dispositivo(self, estado_dispositivo_json, dispositivo_object):
         
        if (hasattr(dispositivo_object, "machine")):
            dispositivo_object.machine.set_state(estado_dispositivo_json)


    def adicionar_dispositivo(self):

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
            raise ConfigInvalida("Tipo de dispositivo inválido")
        
        self.logger.evento(self.dispositivo, "adicionar")


    def mostrar_dispositivo(self):

        id_dispositivo = input("Digite o id do dispositivo: ")
        
        for dispositivo in self.dispositivos:
            
            if dispositivo.id == id_dispositivo.lower().strip():
                return dispositivo

        raise DispositivoNaoExiste("Dispositivo não encontrado")


    def listar_dispositivos(self):
        
        for dispositivo in self.dispositivos:
            print(dispositivo)


    def remover_dispositivo(self):

        dispositivo = self.mostrar_dispositivo()
        index = self.dispositivos.index(dispositivo)
        self.dispositivos.pop(index)

        self.logger.evento(dispositivo, "remover")


    def executar_comando(self):

        dispositivo = self.mostrar_dispositivo()
        comando = input("Qual comando deseja executar? ").lower().strip()
        
        try:                
            dispositivo.trigger(comando)
        except MachineError:
            raise TransicaoInvalida("Não foi possível mudar o estado deste dispositivo. Verfique um estado possível para realizar a mudança")

        
        if comando != "desligar" and comando != "fechar":
            print("Atributos que podem ser modificados [LUZ]: brilho e cor, [PERSIANA]: porcentagem de abertura(abertura)")
            argumentos = input("Argumentos (k=v separados por espaco) ou ENTER: ")
                
            if argumentos != "":
                argumentos_dict = dict(argumento.split("=") for argumento in argumentos.split())

                try:
                    self._mudar_atributos(argumentos_dict, dispositivo)
                except ValidacaoAtributo as e:
                    raise ValidacaoAtributo(e.mensagem)
            
        self.sujeito.notificar("executar comando", dispositivo, comando)  
        self.logger.evento(dispositivo, "executar comando", comando)


    def _mudar_atributos(self, argumentos, dispositivo):

        try:
            if "brilho" in argumentos:
                dispositivo.definir_brilho(value = int(argumentos.get("brilho")))
            
            if "cor" in argumentos:
                dispositivo.definir_cor(value = argumentos.get("cor"))
            
            if "abertura" in argumentos:
                dispositivo.definir_porcentagem_abertura(value = int(argumentos.get("abertura")))

        except MachineError:
            raise TransicaoInvalida("Não foi possível mudar o estado deste dispositivo. Verfique um estado possível para realizar a mudança")


    def alterar_atributo(self):
        
        print("Atributos que podem ser modificados [LUZ]: brilho e cor, [PERSIANA]: porcentagem de abertura(abertura)")
        
        dispositivo = self.mostrar_dispositivo()

        if dispositivo.tipo == TiposDispostivos.LUZ or dispositivo.tipo == TiposDispostivos.PERSIANA: 

            argumentos = input("Argumentos (k=v separados por espaco) ou ENTER: ")

            if argumentos != "":
                    argumentos_dict = dict(argumento.split("=") for argumento in argumentos.split())
                    self._mudar_atributos(argumentos_dict, dispositivo)

        else:
            raise ConfigInvalida("Esse dispositivo não possui atributos que podem ser alterados")


    def executar_rotina(self):

        rotina = input("Digite o tipo de rotina que deseja executar (dormir ou acordar): ").lower().strip()
        self.sujeito.notificar("rotina", dispositivo = self.dispositivos, trigger = rotina)


    def salvar_configuracao(self):
        self.sujeito.notificar("json", self.dispositivos)
        print("Configuração salva")
    

    def salvar_configuracao_lista_dispositivos(self):
        self.sujeito.notificar("json", self.dispositivos)
        print("Saindo...")


    def gerar_relatorio(self):

        print()
        print("Tipos de relatórios disponíveis: ")
        print("1 - Dispositivos mais usados")
        print("2 - Tempo total em que cada luz permaneceu ligada")
        print("3 - Percentual médio de abertura de persianas")
        print("4 - Consumo por tomada inteligente")
        print("5 - Distribuição de comandos por tipo de dispositivo")
        print()


        opcao = int(input("Escolha sua opção: "))

        if opcao == 1:
            self._dispositivos_mais_usados()
        
        elif opcao == 2:
            self._tempo_luzes_ligadas()
        
        elif opcao == 3:
            self._percentual_medio_persiana()
        
        elif opcao == 4:
            self._consumo_tomada_inteligente()
        
        elif opcao == 5:
            self._comandos_por_tipo()


    def _dispositivos_mais_usados(self):

        with open(file = "data/events.csv", mode = "r") as file:
            dispositivos = csv.DictReader(file)

            tipos = [dispositivo.get("tipo") for dispositivo in dispositivos]

            tipos_com_quantidade = {tipo: tipos.count(tipo) for tipo in tipos}

            dispositivos_mais_usados = dict(sorted(tipos_com_quantidade.items(), key = lambda tipo: tipo[1], reverse = True))
        
        
        with open(file = "data/relatorio.csv", mode = "w", newline = "", encoding = "utf-8") as file:

            cabecalho = ["tipo", "quantidade"]
            writer = csv.DictWriter(file, fieldnames=cabecalho)
            writer.writeheader()

            for tipo, quantidade in dispositivos_mais_usados.items():
                writer.writerow({"tipo": tipo, "quantidade": quantidade})


    def _tempo_luzes_ligadas(self):

        with open(file = "data/events.csv", mode = "r") as file:
            dispositivos = csv.DictReader(file)

            dispositivos_luz = list(filter(lambda dispositivo: dispositivo.get("tipo") == "luz", dispositivos))


        with open(file = "data/relatorio.csv", mode = "w", newline = "", encoding = "utf-8") as file:

            cabecalho = ["id_dispositivo", "tempo_total"]
            writer = csv.DictWriter(file, fieldnames=cabecalho)
            writer.writeheader()

            
            for dispositivo in dispositivos_luz:
                
                tempo_total = 0

                if dispositivo.get("estado_origem") == "off":
                    ligou = datetime.strptime(dispositivo.get("timestamp"), "%Y-%m-%dT%H:%M:%S")
                else:
                    desligou = datetime.strptime(dispositivo.get("timestamp"), "%Y-%m-%dT%H:%M:%S")
                    tempo_total = ((desligou - ligou).total_seconds() / 3600)
                
                if tempo_total != 0:
                    writer.writerow({"id_dispositivo": dispositivo.get("id_dispositivo"), "tempo_total": tempo_total})


    def _percentual_medio_persiana(self):

        with open(file = "data/configuracao.json", mode = "r") as file:
            dispositivos_json = json.load(file)
            dispositivos_persiana_json = list(filter(lambda dispositivo: dispositivo.get("tipo") == "persiana", dispositivos_json["dispositivos"]))
            

        with open(file = "data/events.csv", mode = "r") as file:
            dispositivos = csv.DictReader(file)

            dispositivos_persiana = list(filter(lambda dispositivo: dispositivo.get("tipo") == "persiana" and dispositivo.get("estado_destino") == "open", dispositivos))

            porcentagens = []

            for persiana_json in dispositivos_persiana_json:

                for persiana_csv in dispositivos_persiana:

                    if persiana_json.get("id") == persiana_csv.get("id_dispositivo"):
                        porcentagens.append(persiana_json.get("atributos").get("percentual_abertura"))

        media = sum(porcentagens) / len(porcentagens)

        with open(file = "data/relatorio.csv", mode = "w", newline = "", encoding = "utf-8") as file:

            cabecalho = ["percentual_medio_persiana"]
            writer = csv.DictWriter(file, fieldnames=cabecalho)
            writer.writeheader()

            writer.writerow({"percentual_medio_persiana": media})


    def _consumo_tomada_inteligente(self):

        with open("data/tomada_events.csv") as file:
            dispositivos = csv.DictReader(file)
        
            consumo_tomadas = list(map(lambda dispositivo: dispositivo.get("total_wh"), dispositivos))
        

        consumo_total = reduce(lambda consumo_tomada_1, consumo_tomada_2: consumo_tomada_1 + consumo_tomada_2, consumo_tomadas)


        with open(file = "data/relatorio.csv", mode = "w", newline = "", encoding = "utf-8") as file:

            cabecalho = ["consumo_tomada_inteligente"]
            writer = csv.DictWriter(file, fieldnames=cabecalho)
            writer.writeheader()

            writer.writerow({"consumo_tomada_inteligente": consumo_total})


    def _comandos_por_tipo(self):

         with open(file = "data/events.csv", mode = "r") as file:

            dispositivos = csv.DictReader(file)
           
            comando_tipo = [(dispositivo["tipo"], dispositivo["evento"]) for dispositivo in dispositivos]
            contagem = Counter(comando_tipo)


            with open(file = "data/relatorio.csv", mode = "w", newline = "", encoding = "utf-8") as file:

                cabecalho = ["tipo_dispositivo", "evento", "quantidade"]
                writer = csv.DictWriter(file, fieldnames=cabecalho)
                writer.writeheader()


                for (tipo, evento), quantidade in contagem.items():
                    writer.writerow({"tipo_dispositivo": tipo, "evento": evento, "quantidade": quantidade})

        

if __name__ == "__main__":
    hub = Hub()
    hub.adicionar_dispositivos_json_in_list()
    hub.gerar_relatorio()
    # hub.adicionar_dispositivo()
    # hub.adicionar_dispositivo()
    # hub.adicionar_dispositivo()
    # hub.adicionar_dispositivo()
    # hub.adicionar_dispositivo()
    # hub.listar_dispositivos()
    # hub.mostrar_dispositivo()
    # hub.alterar_atributo()
    # hub.executar_comando()
    # hub.executar_comando()
    # hub.remover_dispositivo()
    # hub.executar_rotina()
    # hub.executar_rotina()
