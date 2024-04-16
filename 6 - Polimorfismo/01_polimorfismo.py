class Passaro:
    def __init__(self, voo=None):
        self.voo = voo

    def voar(self):
        self.voo = self.voo
            
    def __str__(self):
        return f"{self.__class__.__name__} {'pode' if (self.voo == True) else 'não pode'} voar!"

class Pardal(Passaro):
    def __init__(self, voo=True):
        super().__init__(voo)

    def voar(self):
        super().voar()

class Avestruz(Passaro):
    def __init__(self, voo=False):
        super().__init__(voo)

    def voar(self):
        super().voar()

class Avião(Passaro):
    def __init__(self, voo=True):
        super().__init__(voo)
    
    def voar(self):
        super().voar()

# aqui ocorre o polimorfismo
def fly_skill(obj):
    print(obj())


fly_skill(Pardal)
#fly_skill(Avestruz)
#fly_skill(Avião)