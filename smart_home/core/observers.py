# Observer (console/arquivo)
from abc import ABC, abstractmethod
import csv
import json
from datetime import datetime

from smart_home.core.eventos import Eventos
from smart_home.core.dispositivos import TiposDispostivos


class Sujeito:

    def __init__(self):
        self.observadores = []


    def adicionar_observador(self, observador):

        if isinstance(observador, Observador):
            self.observadores.append(observador)
    

    def remover_observador(self, observador):
        self.observadores.remove(observador)

    
    def notificar(self, tipo_evento, dispositivo, trigger = ""):

        for observador in self.observadores:
            observador.atualizar(tipo_evento, dispositivo, trigger)



class Observador(ABC):

    @abstractmethod
    def atualizar(self, tipo_evento, dispositivo, trigger):
        pass



class CliObserver(Observador):
    
    def atualizar(self, tipo_evento, dispositivo, trigger):

        if tipo_evento == Eventos.ADICIONAR_DISPOSITIVO.value:
            self._adicionar_dispositivo_json(dispositivo)
        
        if tipo_evento == Eventos.ADICIONAR_DISPOSITIVOS.value:
            self._adicionar_dispositivos_json(dispositivo)
        
        elif tipo_evento == Eventos.REMOVER_DISPOSITIVO.value:
            self._remover_dispositivo_json(dispositivo)
        
        elif tipo_evento == Eventos.EXECUTAR_COMANDO_DISPOSITIVO.value:
            self._adicionar_transicao_csv(dispositivo, trigger)
            #TODO: MODIFICAR NO JSON
        

    def _adicionar_dispositivo_json(self, dispositivo):

        #TODO: pegar objeto e converter para dicionario
        #TODO: pegar esse objeto dicionario e adicionar em uma lista 
        #TODO: pegar essa lista e adicionar no json
        with open(file = "data/configuracao.json", mode = "r", encoding = "utf-8") as file:
            dispositivos = json.load(file)

        with open(file = "data/configuracao.json", mode = "w", encoding = "utf-8") as file:

             if dispositivo.tipo == TiposDispostivos.LUZ or dispositivo.tipo == TiposDispostivos.PERSIANA or dispositivo.tipo == TiposDispostivos.TOMADA:
                estado = dispositivo.state
                print("entrei")
             
             else:
                estado = dispositivo.state.name
    
        
             if dispositivo.tipo == TiposDispostivos.LUZ:
                
                dispositivo_dict = {
                    "id": dispositivo.id,
                    "tipo": dispositivo.tipo,
                    "nome": dispositivo.nome,
                    "estado": estado,
                    "atributos": {
                        "brilho": dispositivo.brilho,
                        "cor": dispositivo.cor
                    }
                }
            
             elif dispositivo.tipo == TiposDispostivos.PERSIANA:
                dispositivo_dict = {
                    "id": dispositivo.id,
                    "tipo": dispositivo.tipo,
                    "nome": dispositivo.nome,
                    "estado": estado,
                    "atributos": {"percentual_abertura": dispositivo.percentual_abertura}
                }
            
             elif dispositivo.tipo == TiposDispostivos.TOMADA:
                dispositivo_dict = {
                    "id": dispositivo.id,
                    "tipo": dispositivo.tipo,
                    "nome": dispositivo.nome,
                    "estado": estado,
                    "atributos": {"potencia": dispositivo.potencia_w}
                }
            
             else:
                dispositivo_dict = {
                    "id": dispositivo.id,
                    "tipo": dispositivo.tipo,
                    "nome": dispositivo.nome,
                    "estado": estado,
                    "atributos": {}
                }

             dispositivos["dispositivos"].append(dispositivo_dict)
             json.dump(dispositivos, file, indent = 2)


    def _adicionar_dispositivos_json(self, dispositivos):

        with open(file = "data/configuracao.json", mode = "r", encoding = "utf-8") as file:
            dispositivos_json = json.load(file)

        with open(file = "data/configuracao.json", mode = "w", encoding = "utf-8") as file:
             
            #TODO: adicionar chave com o nome dispositivos tipo o da tarefa
             lista_dispositivos = dispositivos_json.get("dispositivos")

             ids = [dispositivo.get("id") for dispositivo in lista_dispositivos]
            
             for dispositivo in dispositivos:

                if dispositivo.id not in ids:
                    print(dispositivo.id, "não está")

                    if dispositivo.tipo == TiposDispostivos.LUZ or dispositivo.tipo == TiposDispostivos.PERSIANA or dispositivo.tipo == TiposDispostivos.TOMADA:
                        estado = dispositivo.state
                    
                    else:
                        estado = dispositivo.state.name
            
                
                    if dispositivo.tipo == TiposDispostivos.LUZ:
                        
                        dispositivo_dict = {
                            "id": dispositivo.id,
                            "tipo": dispositivo.tipo,
                            "nome": dispositivo.nome,
                            "estado": estado,
                            "atributos": {
                                "brilho": dispositivo.brilho,
                                "cor": dispositivo.cor
                            }
                        }
                    
                    elif dispositivo.tipo == TiposDispostivos.PERSIANA:
                        dispositivo_dict = {
                            "id": dispositivo.id,
                            "tipo": dispositivo.tipo,
                            "nome": dispositivo.nome,
                            "estado": estado,
                            "atributos": {"percentual_abertura": dispositivo.percentual_abertura}
                        }
                    
                    else:
                        dispositivo_dict = {
                            "id": dispositivo.id,
                            "tipo": dispositivo.tipo,
                            "nome": dispositivo.nome,
                            "estado": estado,
                            "atributos": {}
                        }

                    dispositivos_json["dispositivos"].append(dispositivo_dict)
                
                json.dump(dispositivos_json, file, indent = 2)


    def _remover_dispositivo_json(self, dispositivo):

        with open(file = "data/configuracao.json", mode = "r") as file:
            dispositivos = json.load(file)

            lista_dispositivos = dispositivos.get("dispositivos")

            for i, d in enumerate(lista_dispositivos):
                if d.get("id") == dispositivo.id:
                    lista_dispositivos.pop(i)
                    break
            
        
        with open(file = "data/configuracao.json", mode = "w") as file: 

            json.dump(dispositivos, file, indent = 2)


    def _adicionar_transicao_csv(self, dispositivo, trigger):

        evento = dispositivo.machine.events[trigger]

        for source, transicoes in evento.transitions.items():
            for t in transicoes:
               source = t.source
               dest = t.dest


        with open(file = "data/events.csv", mode = "a", newline = "", encoding = "utf-8") as file:

            writer = csv.writer(file)
            
            writer.writerow([datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), dispositivo.id, trigger, source.lower(), dest.lower()])

