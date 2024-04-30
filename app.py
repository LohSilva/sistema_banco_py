from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
import textwrap

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\nOperação inválida! Você não tem saldo suficiente.")

        elif valor > 0:
            self._saldo -= valor
            print("\nSaque realizado com sucesso!")
            return True

        else:
            print("\nOperação falhou! O valor informado é inválido.")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\nDepósito realizado com sucesso!")
            return True
        else:
            print("\nOperação falhou! O valor informado é inválido.")
            return False

    
    def transferir(self, conta_destino, valor):
        if valor > 0:
            transferencia = Transferencia(valor, self, conta_destino)
            transferencia.registrar()
            print("\nTransferência realizada com sucesso!")
            return True
        else:
            print("\nOperação inválida! O valor informado é negativo.")
            return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite_valor_saque=500, limite_transferencia = 1000, limite_numero_saques=3):
        super().__init__(numero, cliente)
        self.limite_valor_saque = limite_valor_saque
        self.limite_numero_saques = limite_numero_saques
        self.limite_transferencia = limite_transferencia

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite_valor_saque
        excedeu_saques = numero_saques >= self.limite_numero_saques

        if excedeu_limite:
            print("\nOperação inválida! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("\nOperação inválida! Número máximo de saques excedido.")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

    def transferir(self, conta_destino, valor):
        if valor > 0 and valor <= self.limite_transferencia:
            return super().transferir(conta_destino, valor)
            
        else:
            print("\nOperação inválida! O valor da transferência excede o limite.")
            

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Transferencia(Transacao):
    def __init__(self, valor, conta_origem, conta_destino):
        self.valor = valor
        self.conta_origem = conta_origem
        self.conta_destino = conta_destino

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor (self, novo_valor):
        if novo_valor <= 0:
            raise ValueError("Operação inválida. O valor deve ser positivo!")
        self._valor = novo_valor

    def registrar(self):
        if self.conta_origem.saldo >= self.valor:
            self.conta_origem.sacar(self.valor) and self.conta_destino.depositar(self.valor)
            self.conta_origem.historico.adicionar_transacao(self)
            self.conta_destino.historico.adicionar_transacao(self)
        else:
            print("Operação inválida. Transferência não realizada, seu saldo é insuficiente.")     

def menu():
    menu = """\n
   
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tTransferir
    [5]\tCadastrar Conta
    [6]\tListar contas
    [7]\tCadastrar Cliente
    [0]\tSair
    """

    opcao = input(menu + "\nEscolha a opção desejada: ")
    return opcao.lower()
    
def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nCliente não possui conta!")
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def transferir(clientes):
    cpf_origem = input("Informe o CPF do cliente remetente: ")
    cliente_origem = filtrar_cliente(cpf_origem, clientes)

    if not cliente_origem:
        print("\nCliente remetente não encontrado!")
        return

    cpf_destino = input("Informe o CPF do cliente destinatário: ")
    cliente_destino = filtrar_cliente(cpf_destino, clientes)

    if not cliente_destino:
        print("\nCliente destinatário não encontrado!")
        return

    conta_origem = recuperar_conta_cliente(cliente_origem)
    conta_destino = recuperar_conta_cliente(cliente_destino)

    if not conta_origem or not conta_destino:
        return

    valor = float(input("Informe o valor a ser transferido: "))

    conta_origem.transferir(conta_destino, valor)    


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\nJá existe cliente com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\nCliente criado com sucesso!")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado, fluxo de criação de conta encerrado!")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\nConta criada com sucesso!")


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))
       
def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            depositar(clientes)

        elif opcao == "2":
            sacar(clientes)

        elif opcao == "3":
            exibir_extrato(clientes)

        elif opcao == "4":
            transferir(clientes)

        elif opcao == "5":
            criar_conta(len(contas) + 1, clientes, contas)

        elif opcao == "6":
            listar_contas(contas)

        elif opcao == "7":
            criar_cliente(clientes)

        elif opcao == "0":
            break

        else:
            print("\nOperação inválida, por favor selecione novamente a operação desejada.")


main()
