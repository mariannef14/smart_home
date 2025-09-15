from smart_home.core.hub3 import Hub


#TODO: ADICIONAR TODOS OS DISPOSITIVOS DO JSON NA LISTA ANTES DE INICIAR O PROGRAMA
#TODO: renomear para hub e não hub3
hub = Hub()
hub.adicionar_dispositivos_json_list()

while True:
    print("=== SMART HOME HUB ===")
    print("1. Listar dispositivos")
    print("2. Mostrar dispositivo")
    print("3. Executar comando em dispositivo")
    print("4. Alterar atributo de dispositivo")
    print("5. Executar rotina")
    print("6. Gerar relatorio")
    print("7. Salvar configuracao")
    print("8. Adicionar dispositivo")
    print("9. Remover dispositivo")
    print("10. Sair")
    opcao = int(input("Escolha uma opcao: "))


    try:

        if opcao == 1:
            hub.listar_dispositivos()
        
        elif opcao == 2:
            print(hub.mostrar_dispositivo())
        
        elif opcao == 3:
            hub.executar_comando()
        
        elif opcao == 4:
            hub.alterar_atributo()
        
        elif opcao == 5:
            hub.executar_rotina()
        
        elif opcao == 6:
            hub.gerar_relatorio()
        
        elif opcao == 7:
            hub.salvar_configuracao()

        elif opcao == 8:
            hub.adicionar_dispositivo()

        elif opcao == 9:
            hub.remover_dispositivo()

        elif opcao == 10:
            hub.salvar_configuracao_lista_dispositivos()
            break
    
    except Exception as error:
        print(error)