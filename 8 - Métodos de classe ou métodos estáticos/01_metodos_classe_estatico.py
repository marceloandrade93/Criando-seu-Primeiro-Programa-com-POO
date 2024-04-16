class Pessoa:
    def __init__(self, nome=None, idade=None):
        self.nome = nome
        self.idade = idade
    
    # para métodos de fábrica - que retornam instâncias dessa classe
    @classmethod
    def criar_de_nascimento(cls, ano, mes, dia, nome):
        idade = 2024 - ano
        return cls(nome, idade)
    
    # para métodos estáticos, que apenas fazem sentido estar na classe
    @staticmethod
    def e_maior_idade(idade):
        return f"{'É' if (idade >= 18) else 'Não é'} maior de idade!"
    

p = Pessoa.criar_de_nascimento(1991, 2, 15, "Mateus")
print(p.nome, p.idade)

print(Pessoa.e_maior_idade(10))
print(Pessoa.e_maior_idade(18))