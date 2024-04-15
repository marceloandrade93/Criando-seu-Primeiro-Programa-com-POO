#  MÉTODOS ESPECIAIS 
# construtor: __init__
# destrutor: __del__

class Cachorro:
    # "acordado=True" significa que o atributo já recebe o valor padrão,
    # não sendo necessário no início.
    def __init__(self, nome, cor, acordado=True):
        print("Inicializando a classe...")
        self.nome = nome
        self.cor = cor
        self.acordado = acordado
        print(f"{self.nome} correu para o portão!")

    def __del__(self):
        print(f"{self.nome} voltou para dormir...")
        print("Removendo a instância da classe...")

    def falar(self):
        print(f"{self.nome} latiu para o carro na rua!")


c = Cachorro("Cacau", "branca")
c.falar()
