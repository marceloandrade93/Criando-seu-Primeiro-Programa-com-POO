from abc import ABC, abstractmethod
from datetime import datetime

class SistemaDaAgencia:
    def __init__(self):
        self._agencia = "0150"

    def __str__(self) -> str:
        return f"\n**** Sistema de Operações Internas **** \n************ Agência: {self._agencia} ************ \n"

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
        self._agencia = SistemaDaAgencia()
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
        return f"""
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


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
x = SistemaDaAgencia()
print(x)

