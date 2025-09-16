from enum import Enum


class Eventos(Enum):
    ADICIONAR_DISPOSITIVO = "adicionar"
    EXECUTAR_COMANDO_DISPOSITIVO  ="executar comando"
    REMOVER_DISPOSITIVO = "remover"
    ADICIONAR_DISPOSITIVOS_JSON = "json"
    EXECUTAR_ROTINA = "rotina"