
import requests
import lxml.html
import xml.etree.ElementTree as ET
from random import randrange

# Class Comandos --------------------------------------------------------------


class Comandos():

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) \
AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept-Language': 'es-ES,es;q=0.8,en;q=0.6'}

# Metodo respuesta ------------------------------------------------------------

    def respuesta(self, socket, sunick, context, info):

        if info == "!ayuda":
            self.ayuda(socket, sunick)
            return
        elif info == "!chiste":
            self.chistes(socket, context)
            return

        comando = info.lower().split()
        try:
            if comando[1] is not None:
                if comando[0] == "!horoscopo":
                    self.horoscopo(socket, sunick, context, comando[1].lower())
                elif comando[0] == "!noticias":
                    self.noticias(socket, sunick, context, comando[1].lower())

        except:
            if info == "!horoscopo":
                salida = 'PRIVMSG '+context + \
                    ' :Tienes que poner un signo del zodiaco\r\n'
                socket.send(salida.encode("utf-8"))
            elif info == "!noticias":
                salida = 'PRIVMSG '+context +\
                    ' :Hay que agregar un diaro, elmundo o abc\r\n'
                socket.send(salida.encode("utf-8"))

# Metodo horoscopo ------------------------------------------------------------

    def horoscopo(self, socket, sunick, context, info):
        if info == "aries" or info == "tauro" or info == "geminis" \
            or info == "cancer" or info == "leo" or info == "virgo" \
            or info == "libra" or info == "escorpio" or info == "sagitario" \
            or info == "capricornio" or info == "acuario" or info == "piscis":
            url = "http://es.horoscopofree.com/object/html/iframe-sign-"+info
            html = requests.get(url, headers=self.hdr)
            doc = lxml.html.fromstring(html.content)
            texto = doc.xpath("/html/body/div/div/p/text()")
            salida = 'PRIVMSG '+context+' :\00304<'+info +\
                '>\00303 :'+texto[0].strip()+'\r\n'
            socket.send(salida.encode("latin1"))

        else:
            salida = 'PRIVMSG '+context +\
                ' Error: Tienes que escribir un signo correcto y sin tilde\r\n'
            socket.send(salida.encode("utf-8"))

# Metodo noticias -------------------------------------------------------------

    def noticias(self, socket, sunick, context, info):

        if info == "abc":
            url = "https://www.abc.es/rss/feeds/abcPortada.xml"
        elif info == "elmundo":
            url = "https://e00-elmundo.uecdn.es/elmundo/rss/portada.xml"
        else:
            salida = 'PRIVMSG '+context +\
                ' Error: Tienes que escribir bien el nombre\r\n'
            socket.send(salida.encode("utf-8"))
            return

        html = requests.get(url, headers=self.hdr, verify=False)
        if html.status_code == 200:
            home = html.content.decode('utf-8')
        root = ET.fromstring(home)

        lista = []
        contador = 0
        for f in root.iter("title"):
            contador += 1
            if contador > 2 and contador <= 12:
                salida = 'PRIVMSG '+sunick +\
                    ' :\00304<'+str(contador-2)+'>\003 :'+f.text+'\r\n'
                socket.send(salida.encode("latin1"))

# Metodo chistes --------------------------------------------------------------

    def chistes(self, socket, context):

        with open('chistes.txt') as mis_chistes:
            total_lineas = sum(1 for line in mis_chistes)
        offset = randrange(total_lineas+1)

        count = 0
        with open('chistes.txt') as lineas:
            for linea in lineas:
                if count == offset:
                    linea = linea.rstrip()
                    break
                count += 1

        frase = linea.split('#')
        for lin in frase:
            salida = 'PRIVMSG '+context +' :'+lin +'\r\n'
            socket.send(salida.encode("latin1"))
            
# Metodo ayuda ----------------------------------------------------------------

    def ayuda(self, socket, sunick):

        salida = 'PRIVMSG '+sunick +\
            ' :Hay en estos momentos 6 opciones:\r\n'
        socket.send(salida.encode("latin1"))
        salida = 'PRIVMSG '+sunick +\
            ' :!ahorcado "Juego de trivial, se para con !stop"\r\n'
        socket.send(salida.encode("latin1"))
        salida = 'PRIVMSG '+sunick +\
            ' :!serpiente "Juego de palabras, se para con !stop"\r\n'
        socket.send(salida.encode("latin1"))
        salida = 'PRIVMSG '+sunick +\
            ' :!robar "Juego de adivinar codigo, se para con !stop"\r\n'
        socket.send(salida.encode("latin1"))
        salida = 'PRIVMSG '+sunick +\
            ' :!horoscopo <signo> "Lee tu horoscopo"\r\n'
        socket.send(salida.encode("latin1"))
        salida = 'PRIVMSG '+sunick +\
            ' :!noticias "Lee las noticias de algunos diarios"\r\n'
        socket.send(salida.encode("latin1"))
        salida = 'PRIVMSG '+sunick +\
            ' :!chiste "Te cuenta un chiste"\r\n'
        socket.send(salida.encode("latin1"))
        salida = 'PRIVMSG '+sunick +\
            ' :!ayuda "Esta ayuda :-)"\r\n'
        socket.send(salida.encode("latin1"))








