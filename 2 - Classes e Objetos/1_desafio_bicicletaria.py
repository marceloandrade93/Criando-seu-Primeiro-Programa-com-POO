#O que é o self? É uma referência explicita para o objeto.

class Bicicleta:
    def __init__(self, cor, modelo, ano, valor):
        self.cor = cor
        self.modelo = modelo
        self.ano = ano
        self.valor = valor
    
    def buzinar(self):
        print("Plim plim...")

    def parar(self):
        print("Parando bicileta...")
        print("Bicicleta parada.")
    
    def correr(self):
        print("Vrummmmm...")

    def __str__(self):
        return f"{self.__class__.__name__}: {', '.join([f'{chave}={valor}' for chave, valor in self.__dict__.items()])}"


b1 = Bicicleta("vermelha", "caloi", 2024, 600)


#b1.buzinar()
#b1.correr()
#b1.parar()

print(b1)