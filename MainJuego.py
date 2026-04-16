import Mazo
import Jugador
import tkinter as tk
from tkinter import messagebox


juegoUNO = tk.Tk()
juegoUNO.title("UNO")
juegoUNO.geometry("700x500")
juegoUNO.config(bg="#845b5b")

tk.Label(juegoUNO, font=("Arial", 12), text="Pila").pack()

Pila = tk.Frame(juegoUNO, bg="#845b5b", width=100,
                height=150, relief="ridge", border=4)
Pila.pack(anchor="n")


tk.Label(juegoUNO, font=("Arial", 12), text="Mano del jugador").pack()

mesa = tk.Frame(juegoUNO, bg="#845b5b", width=400,
                height=150, relief="ridge", border=4)
mesa.pack(anchor="n")


class Juego:

    def __init__(self):
        self.jugadores = []
        self.coso = Mazo.Baraja()
        self.partida = None
        self.coso.crearmazo()
        self.turno = 0
        self.bot = tk.Button(juegoUNO, font=("Arial", 18), text="Iniciar juego", bg="#16ee51",
                             command=self.iniciarjuego)
        self.bot.pack(anchor="s")

    def iniciarjuego(self):
        for _ in range(4):
            humano = Jugador.Player()
            humano.iniciar(self.coso)
            self.jugadores.append(humano)
            self.partida = self.coso.tomarcarta()
        self.bot.destroy()
        self.hola = tk.Button(juegoUNO, font=("Arial", 18), text="Pasar turno", bg="#118beb",
                              command=self.pasarTurno)
        self.hola.pack(anchor="s")
        self.juegoReal()

    def mostrar_cartas(self, jugadorActual):

        isinstance(jugadorActual, Jugador.Player)
        for widget in mesa.winfo_children():
            widget.destroy()
        for posicion, card in enumerate(jugadorActual.mano, start=0):
            boton = card.mostrarCarta(mesa)
            boton.config(
                command=lambda eleccion=card: self.dejarCarta(eleccion))
            fila = posicion // 7
            columna = posicion % 7

            boton.grid(row=fila, column=columna)

            boton.bind("<Enter>", lambda event,
                       b=boton: self.aumentar_carta(b))
            boton.bind("<Leave>", lambda event, b=boton: self.reducir_carta(b))

    def aumentar_carta(self, boton):
        boton.config(font=(
            "Arial", 70))

    def reducir_carta(self, boton):
        boton.config(font=(
            "Arial", 46))

    def actualizar_pila(self):
        for widget in Pila.winfo_children():
            widget.destroy()

        self.partida.mostrarCarta(Pila).pack()

    def dejarCarta(self, carta):
            if carta.comprobar(self.partida):
                    self.jugadorActual.mano.remove(carta)
                    self.partida = carta

                    if self.partida.numero == "+2":
                        siguiente = self.jugadores[(self.turno + 1) % len(self.jugadores)]
                        siguiente.robar(self.coso)
                        siguiente.robar(self.coso)
                        self.juegoReal()

                    elif self.partida.numero == "+4":
                        siguiente = self.jugadores[(self.turno + 1) % len(self.jugadores)]
                        for _ in range(4):
                            siguiente.robar(self.coso)
                        self.eligeColor()

                    elif self.partida.numero == "@":
                        self.eligeColor() 

                    elif self.partida.numero == "*":
                        self.juegoReal()
                        self.juegoReal()

                    else:
                        self.juegoReal()

            else:
                messagebox.showwarning("no", "Carta no válida")

    def eligeColor(self):
        ventanaA = tk.Toplevel()
        ventanaA.title("Elige un color")
        ventanaA.geometry("300x250")
        ventanaA.config(bg="white")
        ventanaA.grab_set()

        tk.Label(ventanaA, text="Selecciona un color:", font=("Arial", 14)).pack(pady=10)

        colores = ["red", "blue", "green", "yellow"]
        for color in colores:
            tk.Button(
                ventanaA, text=color, bg=color, font=("Arial", 12),
                command=lambda c=color: self.cambiaColor(c, ventanaA)
            ).pack(pady=5, fill="x", padx=20)


    def cambiaColor(self, color, ventana):
        colores_validos = {
            "red": "Rojo",
            "blue": "Azul",
            "green": "Verde",
            "yellow": "Amarillo"
        }

        if color in colores_validos:

            self.partida.color = colores_validos[color]
            ventana.destroy()
            self.juegoReal()

    def pasarTurno(self):
        self.jugadorActual.robar(self.coso)
        self.juegoReal()

    def actualizar(self, turno):
        turno.destroy()
        self.actualizar_pila()
        self.mostrar_cartas(self.jugadorActual)

    def juegoReal(self):
            for jugador in self.jugadores:
                if len(jugador.mano) == 0:
                    self.hola.destroy()
                    messagebox.showinfo("Fin del juego", "¡Alguien ha ganado!")
                    self.reiniciar_juego()
                    return

            self.turno = (self.turno + 1) % len(self.jugadores)
            self.jugadorActual = self.jugadores[self.turno]

            for widget in mesa.winfo_children():
                widget.destroy()

            turno = tk.Label(juegoUNO, text="Cambiando de turno", font=("Arial", 14), bg="yellow")
            turno.pack()
            juegoUNO.after(2000, lambda: self.actualizar(turno))

    def reiniciar_juego(self):
        for widget in mesa.winfo_children():
            widget.destroy()
        for widget in Pila.winfo_children():
            widget.destroy()

        self.__init__()


uno = Juego()


juegoUNO.mainloop()
