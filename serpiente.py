
class Serpiente():
    estado = False

    def __init__(self):
        pass

    def procResp(self, socket, sunick, context, info, estado):

        if estado == "serpiente":
            print("El juego "+estado+" corriendo ejecutado")
        if self.estado == False and estado == "serpiente":
            self.start(True, socket, sunick, context,estado)


    def start(self, opcion, socket, sunick, context,estado):
        if opcion:
            salida = 'PRIVMSG '+ context +' :Juego '+estado+' activado'\
' por '+sunick+' recuerde pararlo con !stop.\n'
            socket.send(salida.encode("utf-8"))
            self.estado = True

    def stop(self, socket, sunick, context,estado):
        salida = 'PRIVMSG '+ context +' :Juego ' +estado+ ' desactivado'\
' por '+sunick+' Gracias.\n'
        socket.send(salida.encode("utf-8"))
        self.estado = False
       





