# Sistema do Banco Py

menu_eletronico = f'''

    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Transferir
    [0] Sair

'''

saldo = 0
extrato = " "
numero_saque_diario = 0
limite_maximo_por_saque = 500.00
LIMITE_SAQUE_DIARIO = 3

while True:

    opcao = int(input(menu_eletronico))

    if opcao == 1:
        valor = float (input("Digite o valor do depósito: "))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"

        else:
            print ("Operação falhou. O valor informado não é válido!")

        print(f"\nDepósito realizado com sucesso!")    
    
    elif opcao == 2:
        valor = float(input("Digite o valor do saque: "))

        if valor > 0:
            excedeu_saldo = valor > saldo
            excedeu_limite = valor > limite_maximo_por_saque
            excedeu_quantidade_saques = numero_saque_diario >= LIMITE_SAQUE_DIARIO

            if excedeu_saldo:
                print("Operação falhou! Saldo insuficiente.")
            elif excedeu_limite:
                print("Operação falhou! O valor do saque excede o limite.")
            elif excedeu_quantidade_saques:
                print("Operação falhou! Número máximo de saques excedido.")
            else:
                saldo -= valor
                extrato += f"Saque: R$ {valor:.2f}\n"
                numero_saque_diario += 1
                print (f"\nSaque realizado com sucesso!")  
        else:
            print("Operação falhou! O valor informado é inválido.")         

    
    elif opcao == 3:
        print("\n================ EXTRATO BANCÁRIO ================")
        print(extrato.strip() if extrato.strip() else "Não foram realizadas movimentações.")
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==================================================")


    elif opcao == 4:  
        valor = float(input("Digite o valor a ser transferido: "))
        conta_destino = input("Digite o número da conta de destino: ")

        if valor > 0:
            if valor <= saldo:
                saldo -= valor
                extrato += f"Transferência para conta {conta_destino}: R$ {valor:.2f}\n"
                print (f"\nTransferência realizado com sucesso!") 
            else:
                print("Operação falhou! Saldo insuficiente.")
        else:
            print("Operação falhou! O valor informado é inválido.")
    

    elif opcao == 0:
        print (f"\nObrigado por utilizar o nosso caixa eletrônico!")
        break

    else:
        print ("Opção inválida. Por favor digite uma opção válida.")





