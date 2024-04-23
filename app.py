# Sistema do Banco Py
def imprimir_mensagem_erro(mensagem):
    print(f"Operação falhou! {mensagem}")
    
def depositar(valor, saldo, /, extrato):
    if valor <= 0.00:
        imprimir_mensagem_erro("O valor do depósito deve ser positivo.")
        return saldo, extrato
    else:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        return saldo, extrato

def sacar(*, valor, saldo, extrato, numero_saque_diario, limite_maximo_por_saque, LIMITE_SAQUE_DIARIO):
    if valor > 0.00:      
        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite_maximo_por_saque
        excedeu_quantidade_saques = numero_saque_diario >= LIMITE_SAQUE_DIARIO

        if excedeu_saldo:
            imprimir_mensagem_erro("Saldo insuficiente.")
        elif excedeu_limite:
            imprimir_mensagem_erro("O valor do saque excede o limite.")
        elif excedeu_quantidade_saques:
            imprimir_mensagem_erro("Número máximo de saques excedido.")
        else:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saque_diario += 1
    else:
        imprimir_mensagem_erro("O valor informado é inválido!")
                
    return saldo, extrato        

def exibir_extrato(saldo, /, *, extrato):
    movimentacoes_realizadas = saldo != 0.00 or extrato.strip() != ""
    print("\n================ EXTRATO BANCÁRIO ================")
    if movimentacoes_realizadas:
        print(extrato.strip())
    else:
        print("Não foram realizadas movimentações.")
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==================================================")

def cadastrar_cliente(clientes):
    nome = input("Informe seu nome: ")
    data_nascimento = input("Digite sua data de nascimento (DD/MM/AAAA): ")
    CPF = input("Informe seu CPF: ")
    endereco_logradouro = input("Digite o logradouro: ")
    endereco_numero = input("Digite o número: ")
    endereco_complemento = input("Digite o complemento(opcional): ")
    endereco_cidade = input("Qual a cidade: ")
    endereco_estado = input("Qual o estado: ")
    endereco_CEP = input("Digite o CEP do endereço: ")

    endereco = {
        "logradouro": endereco_logradouro,
        "numero": endereco_numero,
        "complemento": endereco_complemento,
        "cidade": endereco_cidade,
        "estado": endereco_estado,
        "CEP": endereco_CEP
    }

    cliente = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "CPF": CPF,
        "endereco": endereco
    }
    clientes.append(cliente)
    print("\nCliente cadastrado com sucesso!")
    return clientes

def cadastrar_conta_corrente(cliente, agencia, numero_conta):
    CPF = input("Informe o CPF do usuário: ")
  
    if cliente:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "cliente": cliente}
    print("\nConta corrente cadastrada com sucesso!")
    
def valida_cpf(CPF, clientes):
    for cliente in clientes:
        if cliente["CPF"] == CPF:
            print("CPF já cadastrado!")
            return True
    return False    
    
def exibir_informacoes(clientes, contas):
    print("\nLista de clientes e suas respectivas contas:\n")
    for cliente, conta in zip(clientes, contas):
        print("Nome: ", cliente["nome"])
        print("CPF: ",cliente["CPF"])
        print("Agência:",conta["agencia"])
        print("Número da conta: ",conta["numero_conta"])
        print("=" * 100)
              
def transferir(saldo, extrato):
    valor = float(input("Digite o valor a ser transferido: "))
    conta_destino = input("Digite o número da conta de destino: ")

    if valor > 0.00:
        if valor <= saldo:
            saldo -= valor
            extrato += f"Transferência para conta {conta_destino}: R$ {valor:.2f}\n"
        else:
            imprimir_mensagem_erro("Saldo insuficiente.")
    else:
        imprimir_mensagem_erro("O valor informado é inválido.")

    return saldo, extrato

def main():    
    LIMITE_SAQUE_DIARIO = 3
    
    saldo = 0.00
    extrato = ""
    numero_saque_diario = 0.00
    limite_maximo_por_saque = 500.00    
    agencia="0001"
    clientes = []
    contas = []

    while True:
        print("\nOpções disponíveis: \n")
        menu_eletronico = {
            1: "Depositar",
            2: "Sacar",
            3: "Extrato",
            4: "Transferir",
            5: "Cadastrar Cliente",
            6: "Cadastrar Conta Corrente",
            7: "Listar Informações",
            0: "Sair"
        }
        for opcao, descricao in menu_eletronico.items():
            print(f"[{opcao}] {descricao}")

        opcao = int(input("\nEscolha a opção desejada: "))    

        if opcao == 1:
            valor= float(input("Digite o valor do depósito: "))
            saldo, extrato = depositar(valor, saldo, extrato)
        elif opcao == 2:
            valor = float(input("Digite o valor do saque: "))
            saldo, extrato = sacar(valor=valor, 
                                   saldo=saldo, 
                                   extrato=extrato, 
                                   numero_saque_diario=numero_saque_diario, 
                                   limite_maximo_por_saque=limite_maximo_por_saque, 
                                   LIMITE_SAQUE_DIARIO=LIMITE_SAQUE_DIARIO)
        elif opcao == 3:
            exibir_extrato(saldo, extrato=extrato)        
        elif opcao == 4:
            saldo, extrato = transferir(saldo, extrato)
        elif opcao == 5:
            clientes = cadastrar_cliente(clientes)
        elif opcao == 6:
            numero_conta = len(contas) + 1
            conta = cadastrar_conta_corrente(agencia, numero_conta, clientes)            
            if conta:
                contas.append(conta)            
        elif opcao == 7:
            exibir_informacoes(clientes,contas)    
        elif opcao == 0:
            break
        else:
            print("Opção inválida. Por favor, digite uma opção válida.")


main()



