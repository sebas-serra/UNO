class Cartas:

    def __init__(self, numero, color):
        self.numero = numero
        self.color = color

    def __repr__(self):
        return f"({self.numero!r}, {self.color!r})"

    def __str__(self):
        return f"({self.numero!r}, {self.color!r})"

    def comprobar(self, pila):
        if self.color == pila.color or self.numero == pila.numero or self.color == "negro":
            return True
        else:
            return False