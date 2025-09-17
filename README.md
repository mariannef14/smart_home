# 🏠 Smart Home — Hub de Automação Residencial

Este projeto é um **Hub de Automação Residencial**, que permite gerenciar dispositivos inteligentes como luzes, persianas, tomadas, câmeras, portas e irrigadores.  
Você pode **adicionar, listar, consultar, remover dispositivos, executar comandos, gerar relatório e executar rotinas**, além de registrar eventos em CSV.



## ⚙️ Requisitos

- **Python 3.10+**
- Ambiente virtual recomendado (`venv`)
- Instalar dependências do `requirements.txt`

Para criar e ativar a sua virtualenv, use os comandos abaixo:

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
pip install -r requirements.txt #instalar as dependências
```

## 📂Estrutura do Projeto
```
smart_home/
  README.md
  requirements.txt                      #dependências do projeto
  data/
    configuracao.json                   #dispositivos adicionados e rotinas definidas
    eventos.csv                         #logs de transições dos dispositivos
    relatorio.csv                       #relatório gerado de acordo com a escolha do usuário
  smart_home/
    __init__.py
    core/
      cli.py                            #opções da linha de comando
      hub.py                            #gerenciamento do dispositivo e observadores
      dispositivos.py                   #classe base dispositivo e enums
      eventos.py                        #enum com os tipos de eventos
      observers.py                      #observer cli
      logger.py                         #singleton para logging em CSV
      erros.py                          #exceções personalizadas
    dispositivos/                       #dispositivos inteligentes
      porta.py
      luz.py
      tomada.py
      irrigador.py
      persiana.py
      camera.py
      
```

## ▶️ Como executar o projeto

O projeto pode ser executado via CLI (linha de comando):
```python
python -m smart_home.core.cli
```

## ⚡ Menu de opções
```
=== SMART HOME HUB ===
1. Listar dispositivos
2. Mostrar dispositivo
3. Executar comando em dispositivo
4. Alterar atributo de dispositivo
5. Executar rotina
6. Gerar relatorio
7. Salvar configuracao
8. Adicionar dispositivo
9. Remover dispositivo
10. Sair
```

## 📋 Exemplos de uso

### ➕ Adicionar dispositivo(luz)
```
--- ADICIONAR DISPOSITIVO ---

Tipos suportados: CAMERA, IRRIGADOR, LUZ, PERSIANA, PORTA, TOMADA
Tipo do dispositivo: luz
Id (sem espacos): luz_sala
Nome: luz da sala
Digite o valor do brilho (0-100): 45
Digite a cor [NEUTRA, FRIA, QUENTE]: neutra
[EVENTO]: Dispositivo Adicionado: Id:luz_sala, Tipo: LUZ
Dispositivo luz_sala adicionado.
```

### 🔍 Mostrar dispositivo específico(luz adicionada anteriormente)
```
--- DISPOSITIVO ---
Digite o id do dispositivo: luz_sala    
luz_sala | LUZ | On

```

### 📑 Listar dispositivos
```
--- LISTA DISPOSITIVOS ---
irrigador_jardim | IRRIGADOR | DESLIGADO
luz_quarto | LUZ | Off
porta_quarto | PORTA | TRANCADA
tomada_tv | TOMADA | On
persiana_quarto | PERSIANA | Closed
tomada_ventilador | TOMADA | Off
luz_sala | LUZ | Off

```

### ❌ Remover dispositivo
```
--- REMOVER DISPOSITIVO ---
Digite o id do dispositivo: luz_sala 
[EVENTO]: Dispositivo Removido: Id:luz_sala, Tipo: LUZ
Dispositivo luz_sala removido.

```

## 📂Estrutura do arquivo configuracao.json
``` json
{
  "dispositivos": [
    {
      "id": "irrigador_jardim",
      "tipo": "irrigador",
      "nome": "irrigador do jardim",
      "estado": "DESLIGADO",
      "atributos": {}
    },
    {
      "id": "luz_quarto",
      "tipo": "luz",
      "nome": "luz do quarto",
      "estado": "Off",
      "atributos": {
        "brilho": 0,
        "cor": "FRIA"
      }
    },
    {
      "id": "porta_quarto",
      "tipo": "porta",
      "nome": "porta do quarto",
      "estado": "TRANCADA",
      "atributos": {}
    }
  ],
  "rotinas": {
    "dormir": [
      {
        "id": "porta_quarto",
        "comando": "trancar"
      },
      {
        "id": "luz_quarto",
        "comando": "desligar"
      },
      {
        "id": "persiana_quarto",
        "comando": "fechar"
      }
    ],
    "acordar": [
      {
        "id": "luz_quarto",
        "comando": "ligar",
        "argumentos": {
          "brilho": 50,
          "cor": "neutra"
        }
      },
      {
        "id": "persiana_quarto",
        "comando": "abrir",
        "argumentos": {
          "percentual_abertura": 30
        }
      },
      {
        "id": "irrigador_jardim",
        "comando": "ligar"
      }
    ]
  }
}
```

## 📂Estrutura do arquivo events.csv
```csv
timestamp,id_dispositivo,tipo,evento,estado_origem,estado_destino
2025-09-14T19:35:00,irrigador_jardim,irrigador,ligar,desligado,ligado
2025-09-14T19:59:22,camera_casa,camera,ligar,off,on
2025-09-15T20:43:26,luz_quarto,luz,ligar,off,on
```