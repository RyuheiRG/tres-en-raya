"""
Juego del 3 en raya
"""
import math
import random

tablero = []  # Tablero inicial está vacío
casillasVacias = []
TABLERO_FILAS = 3
TABLERO_COLUMNAS = 3

# Inicializamos el tablero
for i in range(9):
    tablero.append(' ')
    casillasVacias.append(i)


def numero(literal, inferior, superior):
    """
    Solicita un número al usuario dentro de un rango específico
    """
    while True:
        valor = input(literal)
        if valor.isnumeric():
            coor = int(valor)
            if inferior <= coor <= superior:
                return coor
        print(f"Solo se admiten números entre {inferior} y {superior}")


def numeros_hermanos(casilla, ficha, v, h):
    """
    Cuenta las fichas contiguas en una dirección específica (v, h)
    """
    f = math.floor(casilla / TABLERO_COLUMNAS)  # Obtenemos la fila
    c = casilla % TABLERO_COLUMNAS  # Obtenemos la columna
    fila_nueva = f + v
    columna_nueva = c + h

    if fila_nueva < 0 or fila_nueva >= TABLERO_FILAS:
        return 0

    if columna_nueva < 0 or columna_nueva >= TABLERO_COLUMNAS:
        return 0

    pos = fila_nueva * TABLERO_COLUMNAS + columna_nueva

    if tablero[pos] != ficha:
        return 0
    else:
        return 1 + numeros_hermanos(pos, ficha, v, h)


def hemos_ganado(casilla, ficha):
    """
    Verifica si la ficha en la casilla ha ganado el juego
    """
    if tablero[casilla] != ficha:  # Asegura que la casilla tenga la ficha correcta
        return False
    if numeros_hermanos(casilla, ficha, -1, 0) + numeros_hermanos(casilla, ficha, 1, 0) >= 2:  # Vertical
        return True
    if numeros_hermanos(casilla, ficha, 0, -1) + numeros_hermanos(casilla, ficha, 0, 1) >= 2:  # Horizontal
        return True
    if numeros_hermanos(casilla, ficha, -1, -1) + numeros_hermanos(casilla, ficha, 1, 1) >= 2:  # Diagonal principal
        return True
    if numeros_hermanos(casilla, ficha, -1, 1) + numeros_hermanos(casilla, ficha, 1, -1) >= 2:  # Diagonal secundaria
        return True
    return False


def colocar_ficha(ficha):
    """
    Solicita al jugador una posición para colocar su ficha
    """
    print("Dame la posición de la ficha")
    while True:
        fila = numero("Fila entre [1 y 3]: ", 1, 3) - 1
        columna = numero("Columna entre [1 y 3]: ", 1, 3) - 1
        casilla = fila * TABLERO_COLUMNAS + columna

        if tablero[casilla] != ' ':
            print("La casilla está ocupada")
        else:
            tablero[casilla] = ficha
            return casilla


def colocar_ficha_maquina(ficha, ficha_contrincante):
    random.shuffle(casillasVacias)

    for casilla in casillasVacias:
        if tablero[casilla] == ' ' and hemos_ganado(casilla, ficha_contrincante):
            tablero[casilla] = ficha
            casillasVacias.remove(casilla)
            return casilla

    # Si no puede ganar, coloca en cualquier lugar disponible
    for casilla in casillasVacias:
        if tablero[casilla] == ' ':
            tablero[casilla] = ficha
            casillasVacias.remove(casilla)
            return casilla


def pintar_tablero():
    """
    Pinta el tablero en la terminal
    """
    pos = 0
    print("-" * 18)
    for fila in range(3):
        for columna in range(3):
            print("| ", tablero[pos], " ", end="")
            pos += 1
        print("|\n", "-" * 18)


jugadores = []
numero_de_jugadores = numero("Coloque el número de jugadores: ", 0, 2)
for i in range(numero_de_jugadores):
    jugadores.append({"nombre": input("Nombre del jugador " + str(i + 1) + ": "), "tipo": "H"})
for i in range(2 - numero_de_jugadores):
    jugadores.append({"nombre": "Máquina " + str(i + 1), "tipo": "M"})

print("\n Empezamos la partida con los jugadores")
for jugador in jugadores:
    print("\t", jugador["nombre"])

empieza = numero(
    f"¿Qué jugador empieza? [1={jugadores[0]['nombre']}, 2={jugadores[1]['nombre']}]: ", 1, 2
)

if empieza == 2:
    jugadores.reverse()

# Iniciamos el juego
continuar = True
fichas_en_el_tablero = 0
while continuar:
    # Pedimos posición de la ficha
    pintar_tablero()
    num_jugador = fichas_en_el_tablero % 2
    ficha = 'X' if num_jugador == 0 else 'O'

    if jugadores[num_jugador]["tipo"] == "H":
        casilla = colocar_ficha(ficha)
    else:
        casilla = colocar_ficha_maquina(ficha, 'X' if num_jugador == 1 else 'O')

    if casilla in casillasVacias:
        casillasVacias.remove(casilla)

    if hemos_ganado(casilla, ficha):
        continuar = False
        print(jugadores[num_jugador]["nombre"], "¡Has ganado!")
    else:
        fichas_en_el_tablero += 1

    if fichas_en_el_tablero == 9 and continuar:  # Si hay empate
        continuar = False
        print("¡Empate!")
        break

pintar_tablero()
