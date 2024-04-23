# Sistema do Banco Py
saldo = 0.00
extrato = " "
numero_saque_diario = 0.00
limite_maximo_por_saque = 500.00
LIMITE_SAQUE_DIARIO = 3
clientes = []

def exibir_extrato(saldo, /, *, extrato):
    movimentacoes_realizadas = saldo != 0.00 or extrato.strip() != ""
    print("\n================ EXTRATO BANCÁRIO ================")
    if movimentacoes_realizadas:
        print(extrato.strip())
    else:
        print("Não foram realizadas movimentações.")
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==================================================")

def exibir_lista_clientes():
    print("Lista de clientes atualizada:\n")
    for cliente in clientes:
        print("Nome:", cliente['nome'])
        print("Data de Nascimento:", cliente['data_nascimento'])
        print("CPF:", cliente['CPF'])
        endereco = cliente['endereco']
        print("Endereço:")
        print("  Logradouro:", endereco['logradouro'])
        print("  Número:", endereco['numero'])
        print("  Complemento:", endereco['complemento'])
        print("  Cidade:", endereco['cidade'])
        print("  Estado:", endereco['estado'])
        print("  CEP:", endereco['CEP'])

def imprimir_mensagem_erro(mensagem):
    print(f"Operação falhou! {mensagem}")

def depositar(valor, /):
    #valor = float(input("Digite o valor do depósito: "))
    if valor > 0.00:
        global saldo, extrato
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        return saldo, extrato
    else:
        imprimir_mensagem_erro("O valor informado não é válido!")

def sacar(*, valor):
    #valor = float(input("Digite o valor do saque: "))
    if valor > 0.00:
        global saldo, extrato, numero_saque_diario
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
        imprimir_mensagem_erro("O valor informado é inválido.")

    return saldo, extrato     

def transferir():
    valor = float(input("Digite o valor a ser transferido: "))
    conta_destino = input("Digite o número da conta de destino: ")

    if valor > 0.00:
        global saldo, extrato
        if valor <= saldo:
            saldo -= valor
            extrato += f"Transferência para conta {conta_destino}: R$ {valor:.2f}\n"
        else:
            imprimir_mensagem_erro("Saldo insuficiente.")
    else:
        imprimir_mensagem_erro("O valor informado é inválido.")

def valida_cpf(CPF):  
    for cliente in clientes:
        if cliente["CPF"] == CPF:
            print("CPF já cadastrado!")
            return True   
    return False

def cadastrar_conta_corrente(cliente):
    numero_agencia = "0001"
    contador_numero_conta = 0
    contador_numero_conta += 1

    numero_conta_corrente = contador_numero_conta
    numero_conta_corrente = input("Digite o numero da conta corrente: ")

    conta_corrente = {
        "agencia": numero_agencia,
        "conta corrente": numero_conta_corrente,
        "cliente": cliente,
        "saldo":0.00,
        "extrato": ""
    }
    return conta_corrente
    print("\nConta corrente cadastrada com sucesso!")

def cadastrar_cliente(): 
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
    conta_corrente = cadastrar_conta_corrente(cliente)

    print("\nCliente cadastrado com sucesso!")
    print("\nNumero da agencia: ", conta_corrente["agencia"])
    print("\nNumero da conta: ", conta_corrente["conta corrente"])
    print("\nCliente vinculado a conta corrente: ",cliente)
   
menu_eletronico = {

    1: "Depositar",
    2: "Sacar",
    3: "Extrato",
    4: "Transferir",
    5: "Cadastrar Cliente",
    0: "Sair"
}
    
while True:

    print("\nOpções disponíveis: \n")
    for opcao, descricao in menu_eletronico.items():
        print(f"[{opcao}] {descricao}")

    opcao = int(input("\nEscolha a opção desejada: "))    

    if opcao == 1:
        valor_deposito = float(input("Digite o valor do depósito: "))
        saldo, extrato = depositar(valor_deposito)
    elif opcao == 2:
        valor_saque = float(input("Digite o valor do saque: "))
        saldo, extrato = sacar(valor = valor_saque)
    elif opcao == 3:
        exibir_extrato(saldo, extrato = extrato)        
    elif opcao == 4:
        transferir()
    elif opcao == 5:
        cadastrar_cliente()
    elif opcao == 6:
        if clientes:
            print("\nClientes cadastrado no sistema:")
            for i, cliente in enumerate(clientes):
                print(f"{i+1}. {cliente['nome']} - {cliente['CPF']}")
            cliente_index = int(input("Digite o número do cliente para vínculo com a nova conta: ")) - 1
            if 0 <= cliente_index < len(clientes):
                cliente_selecionado = clientes[cliente_index]
                conta_corrente = cadastrar_conta_corrente(cliente_selecionado)
                print("\nConta corrente cadastrada com sucesso!")
            else:
                print("\nOpção inválida!")
        else:
            print("\nNenhum cliente cadastrado. Cadastre um cliente primeiro.")
    elif opcao == 7:
        exibir_lista_clientes()    
    elif opcao == 0:
        break
    else:
        print("Opção inválida. Por favor, digite uma opção válida.")






