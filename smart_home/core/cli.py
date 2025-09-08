from smart_home.core.hub import Hub

hub = Hub()


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
            id_dispositivo = input("Digite o id do dispositivo que deseja ver mais detalhes:")
            print(hub.mostrar_dispositivo())
        
        #TODO: FALTA FINALIZAR
        elif opcao == 3:
            hub.executar_comando()

        elif opcao == 8:
            hub.adicionar_dispositivo()

        #TODO: FALTA INICIAR
        elif opcao == 9:
            hub.remover_dispositivo()

        elif opcao == 10:
            break
    
    except Exception as error:
        print(error)