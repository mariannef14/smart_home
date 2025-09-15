from enum import Enum


class Eventos(Enum):
    ADICIONAR_DISPOSITIVO = "adicionar"
    ADICIONAR_DISPOSITIVOS = "adicionar dispositivos"
    ALTERAR_ATRIBUTO_DISPOSITIVO = "alterar atributo"
    EXECUTAR_COMANDO_DISPOSITIVO  ="executar comando"
    REMOVER_DISPOSITIVO = "remover"