
import ahorcado
import serpiente

# Class Juegos ----------------------------------------------------------------


class Juegos():

    estado = False
    nombreJuego = False

# Metodo constructor ----------------------------------------------------------

    def __init__(self, nombre):

        self.nombreJuego = nombre
        self.juegoAhorcado = ahorcado.Ahorcado()
        self.juegoSerpiente = serpiente.Serpiente()

# Metodo procResp -------------------------------------------------------------

    def procResp(self, socket, sunick, context, info, estado):

        if estado == self.nombreJuego:
            if self.nombreJuego == "ahorcado":
                self.juegoAhorcado.proceso(socket, sunick, context, info, estado)
            elif self.nombreJuego == "serpiente":
                self.juegoSerpiente.proceso(socket, sunick, context, info, estado)

        if self.estado is False and estado == self.nombreJuego:
            self.start(True, socket, sunick, context, estado)

# Metodo start ----------------------------------------------------------------

    def start(self, opcion, socket, sunick, context, estado):
        if opcion:
            salida = 'PRIVMSG '+ context +' :Juego '+estado+' activado por '+sunick+' recuerde pararlo con !stop.\n'
            socket.send(salida.encode("utf-8"))
            self.estado = True

# Metoro stop -----------------------------------------------------------------

    def stop(self, socket, sunick, context, estado):
        salida = 'PRIVMSG '+context+' :Juego '+estado+' desactivado por '+sunick+' Gracias.\n'
        socket.send(salida.encode("utf-8"))
        self.estado = False

        if estado == "ahorcado":
            self.juegoAhorcado.parar()
        elif estado == "serpiente":
            self.juegoSerpiente.parar()
