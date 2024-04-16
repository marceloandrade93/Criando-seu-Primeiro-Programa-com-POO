class Estudante:
    escola = "DIO"

    def __init__(self, nome, matricula):
        self.nome = nome
        self.matricula = matricula 

    def __str__(self):
        return f"{self.nome} - {self.matricula} - {self.escola}"


def mostrar_valores(*objs):
    for obj in objs:
        print(obj)


aluno_1 = Estudante("Marcelo", 1)
aluno_2 = Estudante("Pâmela", 2)
mostrar_valores(aluno_1, aluno_2)

Estudante.escola = "Gran Faculdade"
aluno_3 = Estudante("Nala", 3)
mostrar_valores(aluno_1, aluno_2, aluno_3)