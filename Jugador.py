import Mazo


class Player:
    def __init__(self):
        self.mano = []

    def robar(self, mazo):
        self.mano.append(mazo.tomarcarta())

    def iniciar(self, mazo):
        for _ in range(7):
            self.mano.append(mazo.tomarcarta())

    def dejar(self, destino, carta):
        destino.mano.append(self.mano.pop(carta))

    def __repr__(self):
        return f"{self.mano}"

    def __str__(self):
        return f"{self.mano}"