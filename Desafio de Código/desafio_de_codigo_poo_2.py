import textwrap
from abc import ABC, abstractmethod
from datetime import datetime


class SistemaDaAgencia:
    def __init__(self):
        self._agencia = "0150"

    def __str__(self) -> str:
        return f"\n**** Sistema de Operações Internas **** \n************ Agência: {self._agencia} ************"

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

    def __str__(self):
        return f"{self.nome}"


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0150"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod  # OK
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property  # OK
    def saldo(self):
        return self._saldo
    
    @property  # OK
    def numero(self):
        return self._numero
    
    @property  # OK
    def agencia(self):
        return self._agencia
    
    @property  # OK
    def cliente(self):
        return self._cliente

    @property  # OK
    def historico(self):
        return self._historico

    def sacar(self, valor):  # OK 
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\nErro na operação! Limite excedido.")

        elif valor > 0:
            self._saldo += valor

        else:
            print("\nErro na operação! O valor informado é inválido.")

        return False


    def depositar(self, valor):  # OK
        if valor > 0:
            self._saldo = valor
            print(f"\nOperação realizada com sucesso! O depósito de R$ {valor} foi concluído.")

        else:
            print("\nErro na operação! O valor informado é inválido.")
            return False

        return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
    
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saque = numero_saques >= self.limite_saques

        if excedeu_limite:
            print(f"\nErro na operação! O valor do saque excede o limite de {self.limite}.")

        elif excedeu_saque:
            print(f"\nErro na operação! O número máximo de {self.limite_saques} foi excedido.")

        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"Agência:\t{self.agencia} \nC/C:\t\t{self.numero} \nTitular:\t{self.cliente.nome}"


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
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


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


# abre o programa e informa o número da agência
#x = SistemaDaAgencia()
#print(x)

def menu():  #OK
    menu = """
    ================= MENU =================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def depositar(clientes):  #[OK]
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

def sacar (clientes):  #[OK]
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

def exibir_extrato(clientes):  #[OK]
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado! ")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n=============== EXTRATO ===============")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"
    
    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("\n=======================================")

def criar_cliente(clientes):  #[OK]
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\nJá existe cliente com esse CPF! ")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/UF): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n========= CRIADO COM SUCESSO ==========")
    print(cliente)
    print("=======================================")
    
def filtrar_cliente(cpf, clientes):  #[OK]
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def criar_conta(numero_conta, clientes, contas):  #[OK]
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado, fluxo de criação de conta encerrado! ")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n========= CRIADO COM SUCESSO ==========")
    print(conta)
    print("\n=======================================")

def listar_contas(contas):  #[OK]
    for conta in contas:
        print("=" * 39)
        print(textwrap.dedent(str(conta)))

def recuperar_conta_cliente(cliente):  #[OK]
    if not cliente.contas:
        print("\nCliente não possui conta!")
        return
    
    # Não permite ainda cliente escolher a conta
    return cliente.contas[0]

def main():  #
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":  #[OK]
            depositar(clientes)

        elif opcao == "s":  #[OK]
           sacar(clientes)

        elif opcao == "e":  #[OK]
            exibir_extrato(clientes)

        elif opcao == "nu":  #[OK]
            criar_cliente(clientes)
        
        elif opcao == "nc":  #[OK]
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":  #[OK]
            listar_contas(contas)

        elif opcao == "q":  #[OK]
            break

        else:  #[OK]
            print("Operação inválida, por favor selecione novamente a operação desejada.")

print(SistemaDaAgencia())
main()