from transitions import Machine
from dataclasses import dataclass, field
from typing import List

from smart_home.core.dispositivos import TiposDispostivos
from smart_home.dispositivos.porta import Porta
from smart_home.dispositivos.luz import Luz


@dataclass
class Hub:

    dispositivos:List = field(default_factory = list)

    
    def adicionar_dispositivo(self):
        print("Tipos suportados:", TiposDispostivos.all_dispositives())
        tipo_dispositivo = input("Tipo do dispositivo: ").title().strip()
        id_dispositivo = input("Id (sem espacos): ")
        nome_dispositivo = input("Nome: ")


        if tipo_dispositivo == "Porta":
            self.dispositivos.append(Porta(id_dispositivo, nome_dispositivo))
        
        #TODO: TESTAR SE A LUZ ESTÁ FUNCIONANDO SOZINHA COM O PYTHON -M E DEPOIS COM O HUB
        #TODO: PROCURAR SE TEM COMO DEFINIR VALOR PADRÃO COM O DATACLASS
        elif tipo_dispositivo == "Luz":

            brilho_luz = input("Digite o valor do brilho: ")
            cor_luz = input("Digite a cor: ").upper().strip()
            brilho_luz = 50 if brilho_luz == "" else brilho_luz
            cor_luz = "NEUTRA" if cor_luz == "" else cor_luz

            self.dispositivos.append(Luz(id_dispositivo, nome_dispositivo, int(brilho_luz), cor_luz))
        
        elif tipo_dispositivo == "":
            self.dispositivos.append(Tomada(id_dispositivo, nome_dispositivo))
    

    def mostrar_dispositivo(self, id_dispositivo):

        # id_dispositivo = input("Digite o id do dispositivo que deseja ver mais detalhes:")

        
        for dispositivo in self.dispositivos:
            
            if dispositivo.id == id_dispositivo.lower().strip():
                # print("ID | NOME | TIPO | ESTADO")
                # return f"{dispositivo.get('id')} | {dispositivo.get('nome')} | {dispositivo.get('tipo')} | {dispositivo.get('estado')}"
                return f"ID: {dispositivo.id} | Nome: {dispositivo.nome} | Tipo: {dispositivo.tipo} | Estado: {dispositivo.state}"
                
        #TODO: LANÇAR EXCEÇÃO PERSONALIZADA PARA DISPOSITIVO NÃO ENCONTRADO
        print("Não encontrou")


    #TODO: PRINT COM CADA DISPOSITIVO IMPRIMINDO COM O REP DE CADA DISPOSITIVO
    def listar_dispositivos(self):
        
        # print("ID | TIPO | ESTADO")
        for dispositivo in self.dispositivos:
            print(f"{dispositivo.id} | {dispositivo.tipo} | {dispositivo.state}")
            # print(f"ID: {dispositivo.get('id')} | Tipo: {dispositivo.get('tipo')} | Estado: {dispositivo.get('estado')}")
            # print(f"{dispositivo.get('id')} | {dispositivo.get('tipo')} | {dispositivo.get('estado')}")


    def remover_dispositivo(self):

        id_dispositivo = input("Id do dispositivo: ")

        for dispositivo in self.dispositivos:
            
            if dispositivo.get("id") == id_dispositivo.lower().strip():
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
    # porta = Porta("porta_sala", "porta da sala")
    hub = Hub()
    # dispositivos = [{"id": porta.id, "nome": porta.nome, "tipo": porta.tipo, "estado": porta.state.name}]
    hub.adicionar_dispositivo()
    hub.listar_dispositivos()
    # hub.executar_comando()
    hub.remover_dispositivo()