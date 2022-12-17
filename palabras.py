
from random import randrange


# Class Palabras --------------------------------------------------------------

class Palabras():


    frases = {
    0: ["Lo malo del trabajo es que apenas te has acostumbrado a uno, cuando ya lo quieres cambiar.", "Hay quien piensa que el trabajo es una de las cosas más sagradas que existen. Por eso yo he decidido no tocarlo jamás.", "Algo malo debe tener el trabajo, o los ricos ya lo habrían acaparado.", "A los vagos cuesta mucho trabajo encontrarlos.", "Me gusta el trabajo, me fascina. Podría permanecer sentada horas y horas mirando cómo trabajan."],
    1: ["Oye, te amo como aman los patos. ¿Cómo? Patodalavida.", "¿Crees en el amor a primera vista o vuelvo a pasar?", "El amor no existe, es un invento de las noches de borrachera.", "El amor tocó mi puerta, y yo había salido a por el pan.", "He aprendido que el amor es como un ladrillo, se puede construir una casa o hundir un cadáver."],
    2: ["El sexo alarga la vida y yo te quiero hacer inmortal.", "Tú y yo tenemos unos orgasmos pendientes.", "Un intelectual es una persona que ha descubierto algo más interesante que el sexo", "El sexo sólo es sucio si se hace bien", "El sexo forma parte de la naturaleza. Y yo me llevo de maravilla con la naturaleza"],
    3: ["¿Los verdaderos amigos? No son los que te limpian las lágrimas, son los que te preguntan, ¿A quién matamos?", "Voy a eliminar mi cuenta de Facebook. Prefiero juzgar a mis amigos en persona.", "Antes de pedir dinero prestado a un amigo, decide cuál de las dos cosas necesitas más.", "En la vida es difícil encontrar a una persona guapa, inteligente, dulce y buen amigo, así que estate feliz por conocerme.", "Un amigo es alguien que sabe todo sobre ti y todavía te ama"],
    4: ["La verdadera amistad se ve a través del corazón, no a través de los ojos.", "Es el privilegio de la amistad decir tonterías, y que sus tonterías sean respetadas.", "La amistad consiste en olvidar lo que uno da y recordar lo que uno recibe.", "La amistad es como el dinero es más fácil de hacer que conservar", "Todo el mundo sabe que una bola de nieve en la cara es el comienzo perfecto de una amistad duradera."],
    5: ["Frío en invierno y calor en verano, eso es lo sano.", "Soy una mujer razonable, pero este jodido calor me esta volviendo loca.", "Dios, por favor, permite que este calor derrita la grasa que hay en mi cuerpo. ", "Un café helado, en un día caluroso, puede hacer milagros. ", "Un poco más de calor y juro que paso de ser bombón a chocolate a la taza."],
    6: ["Las oportunidades solo se presentan una vez en la vida", "Las mejores cosas de la vida te arruinan el peinado", "Estoy segura de que el universo está lleno de vida inteligente. Simplemente ha sido demasiado inteligente como para venir aquí.", "Cuando la vida te da limones, arrójaselo a alguien a los ojos ;-)", "No te tomes la vida demasiado en serio. Nunca saldrás vivo de ella."],
    7: ["Recuerda que cuanto menos tienes, más vas a poder obtener", "El dinero no da la felicidad, pero prefiero llorar en un Ferrari", "Demasiado dinero nunca es suficiente", "Un banco, es un lugar que te prestará dinero si puedes demostrar que no lo necesitas", "El dinero no es lo más importante en el mundo. El amor lo es. Afortunadamente, amo el dinero"],
    8: ["Cada verano tiene su historia.", "Ningún verano dura eternamente ni ninguna pena para siempre.", "Una vida sin amor es como un año sin verano.", "Algunos de los mejores recuerdos están hechos en chanclas y bañador", "Todo lo bueno, todo lo mágico sucede entre los meses de junio y agosto"],
    9: ["El corazón puede enfriarse mucho si todo lo que has conocido es el invierno.", "La gente no se da cuenta de si es invierno o verano cuando es feliz.", "Una palabra amable puede calentar tres meses de invierno.", "Mantener un corazón cálido en invierno es la verdadera victoria.", "En invierno nos acurrucamos con un buen libro y soñamos alejados del frío"],
    10: ["Tú deberías ser besad@ y por alguien que sepa cómo hacerlo", "Las mujeres todavía recuerdan el primer beso después de que los hombres han olvidado el último", "Besos como el suyo deberían venir con una etiqueta de advertencia. No pueden ser buenos para el corazón", "Tú no sabías lo que era un beso, le preguntaste a mi lengua y hallaste la respuesta", "Me habría gustado poder guardar ese beso en una botella y tomarlo en pequeñas dosis cada hora o cada día "],
    11: ["No tomen drogas, no tengan sexo sin protección, no sean violent@s. Dejen eso para mi.", "Las drogas pueden ser muy divertidas, pero te hacen ver el lado más terrible del ser humano.", "Si es que Dios ha creado algo mejor que el hackís o la marihuana, se lo ha guardado para él.", "Me enamoré de alguien por quien hubiese dado la vida, y eso es como una droga.", "La marihuana causa amnesia y… otras cosas que no recuerdo."],
    12: ["Hasta la guapura cansa. ¿Será por eso que yo siempre estoy cansada?", "Sin maquillaje soy fantastica, maquillada soy una obra de arte", "Todas las mujeres tienen algo bonito... aunque sea una prima lejana.", "Ser guapa no es fácil, pero te acostumbras.", "Soy más que una cara bonita, también tengo un buen culo."],
    13: ["", "", "", "", ""]
}

    palabras= [
    "trabajo",
    "amor",
    "sexo",
    "amigo",
    "amistad",
    "calor",
    "vida",
    "dinero",
    "verano",
    "invierno",
    "beso",
    "droga",
    "guap"
]


# Metodo respuesta ------------------------------------------------------------

    def respuesta(self, socket, sunick, context, info):
        hay = False
        for p,e in enumerate(self.palabras):
            if e in info.lower():
                hay = True
                break
        if hay:
            offset = randrange(5)
            salida = 'PRIVMSG '+context +' '+sunick+' '+self.frases[p][offset]+'\r\n'
            socket.send(salida.encode("utf-8"))









