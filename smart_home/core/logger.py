from smart_home.core.eventos import Eventos

class Singleton():

    _instance = None

    def __new__(cls, *args, **kwargs):

        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance



class Logger(Singleton):

    def evento(self, dispositivo, tipo_evento, trigger = ""):

        if tipo_evento == Eventos.ADICIONAR_DISPOSITIVO.value:
            self._adicionar_dispositivo(dispositivo)
        
        elif tipo_evento == Eventos.REMOVER_DISPOSITIVO.value:
            self._remover_dispositivo(dispositivo)
        
        elif tipo_evento == Eventos.EXECUTAR_COMANDO_DISPOSITIVO.value:
            self._comando_executado(dispositivo, trigger)
    

    def _adicionar_dispositivo(self, dispositivo):
        print(f"[EVENTO]: Dispositivo Adicionado: Id:{dispositivo.id}, Tipo: {dispositivo.tipo}")
        print(f"Dispositivo {dispositivo.id} adicionado.")
    

    def _remover_dispositivo(self, dispositivo):
        print(f"[EVENTO]: Dispositivo Removido: Id:{dispositivo.id}, Tipo: {dispositivo.tipo}")
        print(f"Dispositivo {dispositivo.id} removido.")
    

    def _comando_executado(self, dispositivo, trigger):
        evento = dispositivo.machine.events[trigger]

        for source, transicoes in evento.transitions.items():
            for t in transicoes:
                print(f"[EVENTO] Comando Executado: Id:{dispositivo.id}, Comando: {trigger}, Antes: {t.source}, Depois: {t.dest}")