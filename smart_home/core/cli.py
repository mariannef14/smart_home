from smart_home.core.hub import Hub


hub = Hub()
hub.adicionar_dispositivos_json_in_list()

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
    print()

    try:

        if opcao == 1:
            print("--- LISTA DISPOSITIVOS ---")
            hub.listar_dispositivos()
            print()
        
        elif opcao == 2:
            print("--- DISPOSITIVO ---")
            print(hub.mostrar_dispositivo())
            print()

        elif opcao == 3:
            print("--- EXECUTAR COMANDO ---")
            hub.executar_comando()
            print()

        
        elif opcao == 4:
            print("--- ALTERAR ATRIBUTO DISPOSITIVO ---")
            hub.alterar_atributo()
            print()
        
        elif opcao == 5:
            hub.executar_rotina()
            print()

        
        elif opcao == 6:
            print("--- RELATÓRIOS ---")
            hub.gerar_relatorio()
            print()

        
        elif opcao == 7:
            hub.salvar_configuracao()
            print()

        elif opcao == 8:
            print("--- ADICIONAR DISPOSITIVO ---")
            hub.adicionar_dispositivo()
            print()

        elif opcao == 9:
            print("--- REMOVER DISPOSITIVO ---")
            hub.remover_dispositivo()
            print()

        elif opcao == 10:
            hub.salvar_configuracao_lista_dispositivos()
            break
    
    except Exception as error:
        print(error)