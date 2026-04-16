import Carta
import random as rd


class Baraja():
    def __init__(self):
        self.total = []

    def crearmazo(self):
        for numero in range(1, 10):
            for color in ["Azul", "Rojo", "Verde", "Amarillo"] * 2:
                self.total.append(Carta.Cartas(numero, color))

        for _ in range(4):
            self.total.append(Carta.Cartas("@", "negro"))   # Comodín color
            self.total.append(Carta.Cartas("+4", "negro"))  # +4

        for color in ["Azul", "Rojo", "Verde", "Amarillo"]:
            for _ in range(2):
                self.total.append(Carta.Cartas("+2", color))
                self.total.append(Carta.Cartas("*", color))

        rd.shuffle(self.total)

    def tomarcarta(self):
        return self.total.pop()

    def dejarCarta(self, coso):
        self.total.append(coso)

    def __repr__(self):
        return f"{self.total})"

    def __str__(self):
        return f"{self.total})"
