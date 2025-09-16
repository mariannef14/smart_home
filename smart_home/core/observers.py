# Observer (console/arquivo)
from abc import ABC, abstractmethod
import csv
import json
from datetime import datetime

from smart_home.core.eventos import Eventos
from smart_home.core.dispositivos import TiposDispostivos
from smart_home.dispositivos.porta import Porta
from smart_home.dispositivos.luz import Luz
from smart_home.dispositivos.irrigador import Irrigador
from smart_home.dispositivos.persiana import Persiana
from smart_home.core.dispositivos import StatesPorta
from smart_home.core.erros import ConfigInvalida


class Sujeito:

    def __init__(self):
        self.observadores = []


    def adicionar_observador(self, observador):

        if isinstance(observador, Observador):
            self.observadores.append(observador)
    

    def remover_observador(self, observador):
        self.observadores.remove(observador)

    
    def notificar(self, tipo_evento, dispositivo = "", trigger = ""):

        for observador in self.observadores:
            observador.atualizar(tipo_evento, dispositivo, trigger)



class Observador(ABC):

    @abstractmethod
    def atualizar(self, tipo_evento, dispositivo, trigger):
        pass



class CliObserver(Observador):
    

    def atualizar(self, tipo_evento, dispositivo, trigger):
        
        if tipo_evento == Eventos.ADICIONAR_DISPOSITIVOS_JSON.value:
            self._adicionar_dispositivos_json(dispositivo)
        
        elif tipo_evento == Eventos.EXECUTAR_COMANDO_DISPOSITIVO.value:
            self._adicionar_transicao_csv(dispositivo, trigger)
        
        elif tipo_evento == Eventos.EXECUTAR_ROTINA.value:
            self._executar_rotina(dispositivo, trigger)


    def _parse_object_to_dict(self, dispositivo):
                          
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
        

         return dispositivo_dict


    def _adicionar_dispositivos_json(self, dispositivos):

        with open(file = "data/configuracao.json", mode = "r") as file:
            dispositivos_json = json.load(file)

        with open(file = "data/configuracao.json", mode = "w") as file:

            dispositivos_json.get("dispositivos").clear()


            for dispositivo in dispositivos:
                dispositivo_dict = self._parse_object_to_dict(dispositivo)

                dispositivos_json["dispositivos"].append(dispositivo_dict)
            
            json.dump(dispositivos_json, file, indent = 2) 


    def _adicionar_transicao_csv(self, dispositivo, trigger):

        evento = dispositivo.machine.events[trigger]

        for source, transicoes in evento.transitions.items():
            for t in transicoes:
                source = t.source
                dest = t.dest


        with open(file = "data/events.csv", mode = "a", newline = "", encoding = "utf-8") as file:

            writer = csv.writer(file)
            
            writer.writerow([datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), dispositivo.id, dispositivo.tipo, trigger, source.lower(), dest.lower()])



    def _executar_rotina(self, dispositivos, trigger):

        with open(file = "data/configuracao.json", mode = "r") as file:
            dispositivos_json = json.load(file)


        if trigger not in dispositivos_json.get("rotinas"):
            raise ConfigInvalida("Essa rotina não existe")

        dispositivos_rotina = dispositivos_json.get("rotinas").get(trigger)
        ids_dispositivos_rotina = [dispositivo.get("id") for dispositivo in dispositivos_rotina]

        
        for dispositivo in dispositivos:

            if trigger == "dormir":
            
                if dispositivo.id in ids_dispositivos_rotina:

                    if isinstance(dispositivo, Porta):
                    
                        state_porta = dispositivo.state

                        while state_porta != StatesPorta.TRANCADA:

                            trigger = dispositivo.machine.get_triggers(dispositivo.state)
                            dispositivo.trigger(trigger[0])
                            state_porta = dispositivo.state
                
                    if isinstance(dispositivo, Luz):

                        if dispositivo.state == "On":
                            dispositivo.desligar()
                    
                    if isinstance(dispositivo, Persiana):

                        if dispositivo.state == "Open":
                            dispositivo.fechar()
            
            elif trigger == "acordar":
                
                if isinstance(dispositivo, Luz):
                    dispositivo.ligar()
                    dispositivo.definir_brilho(value = 50)
   
                if isinstance(dispositivo, Persiana):
                    dispositivo.abrir()
                    dispositivo.definir_porcentagem_abertura(value = 30)
                
                if isinstance(dispositivo, Irrigador):
                    dispositivo.ligar()
                    dispositivo.irrigar()