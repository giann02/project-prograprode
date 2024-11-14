import random
from functools import reduce

golesPosibles = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
probabilidadGoles = [0.25, 0.3, 0.2, 0.15, 0.05, 0.03, 0.01, 0.005, 0.002, 0.001]
def ingresarPartidos():
    """
    Permite al administrador ingresar los detalles de una lista de partidos.
    Se solicita que ingrese la cantidad de partidos y luego para cada uno
    se pide el nombre del equipo local y visitante. Los partidos se almacenan como 
    diccionarios con los equipos y los goles, inicialmente en 0.
    
    Returns:
        list: Lista de diccionarios, donde cada uno representa un partido.
        partidos = [
            {"homeTeam": "Boca", "awayTeam": "River", "homeScore": 0, "awayScore": 0},
            {"homeTeam": "Ferro", "awayTeam": "River", homeScore: 0, "awayScore": 0}
        ]
    """
    print("VISTA ADMINISTRADOR")
    while True:
        try:
            cantidadPartidos = int(input("Ingrese la cantidad de partidos: "))
            if cantidadPartidos <= 0:
                raise ValueError("Debe ingresar un número positivo")
            break
        except ValueError as e:
            print(f"Error: {e}. Por favor ingrese un número válido.")
    
    partidos = []
    for _ in range(cantidadPartidos):
        homeTeam = input("Nombre del equipo local: ")
        awayTeam = input("Nombre del equipo visitante: ")
        partido = {
            "homeTeam": homeTeam,
            "awayTeam": awayTeam,
            "homeScore": -1,
            "awayScore": -1,
        }
        partidos.append(partido)
    return partidos


def resultadoUsuarios(partidos):
    """
    Permite a los usuarios ingresar sus predicciones para una lista de partidos.
    
    Se solicita al usuario ingresar su nombre y predecir los goles para cada partido.
    Las predicciones se almacenan en un diccionario, donde la clave es el nombre del usuario
    y el valor es una lista de diccionarios donde cada diccionario representa la prediccion de un partido.
    
    Args:
        partidos (list): Lista de diccionarios que representan los partidos.
    
    Returns:
        dict: Diccionario con las predicciones de los usuarios.
        usuarioResultados= {
            "lucas": [
                {"homeTeam": "Boca", "awayTeam": "River", "predHomeScore": 1, "predAwayScore": 0},
                {"homeTeam": "Ferro", "awayTeam": "River", "predHomeScore": 3, "predAwayScore": 3},
            ],
            "maria": [
                {"homeTeam": "Boca", "awayTeam": "River", "predHomeScore": 2, "predAwayScore": 0},
                {"homeTeam": "Ferro", "awayTeam": "River", "predHomeScore": 1, "predAwayScore": 2},
            ]
        }
    """
    print("VISTA USUARIO \n")
    usuarioResultados = {}
    nombreUsuario = input("Ingrese el nombre del usuario ('fin' para salir): ").lower()
    while nombreUsuario != 'fin':
        if nombreUsuario in usuarioResultados:
            print("El nombre ya ha sido ingresado.")
            nombreUsuario = input("Ingrese otro nombre o 'fin' para salir: ").lower()
            continue
        
        usuarioResultados[nombreUsuario] = []
        for partido in partidos:
            print(f"Partido: {partido['homeTeam']} vs {partido['awayTeam']}")

            # Manejo de excepciones para los goles
            while True:
                try:
                    predHomeScore = int(input(f"Ingrese goles de {partido['homeTeam']}: "))
                    if predHomeScore < 0:
                        raise ValueError("Los goles no pueden ser negativos.")
                    break
                except ValueError as e:
                    print(f"Error: {e}. Intente nuevamente.")
            
            while True:
                try:
                    predAwayScore = int(input(f"Ingrese goles de {partido['awayTeam']}: "))
                    if predAwayScore < 0:
                        raise ValueError("Los goles no pueden ser negativos.")
                    break
                except ValueError as e:
                    print(f"Error: {e}. Intente nuevamente.")

            usuarioResultados[nombreUsuario].append({
                "homeTeam": partido['homeTeam'],
                "awayTeam": partido['awayTeam'],
                "predHomeScore": predHomeScore,
                "predAwayScore": predAwayScore,
            })
        
        nombreUsuario = input("Ingrese el nombre del usuario ('fin' para salir): ").lower()
    return usuarioResultados

def generarResultadosAleatorios(partidos):
    """
    Asigna resultados aleatorios teniendo en cuenta los goles con mayor posibilidad 
    a cada partido y los muestra por pantalla.
    
    Args:
        partidos (list): Lista de diccionarios que representan los partidos.
    
    Returns:
        list: La lista de partidos con los resultados asignados.
        partidosConResultado = [
            {"homeTeam": "Boca", "awayTeam": "River", "homeScore": 1, "awayScore": 1},
            {"homeTeam": "Ferro", "awayTeam": "River", homeScore: 2, "awayScore": 0}
        ]
    """
    for partido in partidos:
        partido['homeScore'] = random.choices(golesPosibles,probabilidadGoles)[0]
        partido['awayScore'] = random.choices(golesPosibles,probabilidadGoles)[0]
        print(f"El Partido: {partido['homeTeam']} vs {partido['awayTeam']} tuvo el resultado de: \n")
        print(f"{partido['homeTeam']} {partido['homeScore']} - {partido['awayScore']} {partido['awayTeam']} \n")
    return partidos

def calcularPuntuaciones(usuarioResultados, partidos):
    """
    Calcula la puntuación de cada usuario en función de sus predicciones.

    Los usuarios obtienen 3 puntos si adivinan el resultado exacto, y 1 punto si solo adivinan el ganador o el empate.
    También muestra mensajes indicando qué partidos acertó el usuario y cuántos puntos ganó.

    Args:
        usuarioResultados (dict): Diccionario con las predicciones de los usuarios.
        partidos (list): Lista de diccionarios que representan los partidos y sus resultados.

    Returns:
        list: Lista de tuplas donde cada una representa el usuario y su puntuación.
    """
    puntuaciones = []
    for usuario, predicciones in usuarioResultados.items():
        puntuacion = 0
        for i in range(len(partidos)):
            golesLocalUsuario = predicciones[i]['predHomeScore']
            golesVisitanteUsuario = predicciones[i]['predAwayScore']
            golesLocalReal = partidos[i]['homeScore']
            golesVisitanteReal = partidos[i]['awayScore']
            if golesLocalUsuario == golesLocalReal and golesVisitanteUsuario == golesVisitanteReal:
                puntuacion += 3
                print(f"{usuario} adivinó el resultado exacto en el partido de {partidos[i]['homeTeam']} y {partidos[i]['awayTeam']}")
                print("Suma 3 puntos \n")
            elif (golesLocalUsuario > golesVisitanteUsuario) and (golesLocalReal > golesVisitanteReal):
                puntuacion += 1
                print(f"{usuario} adivinó el resultado en el partido de {partidos[i]['homeTeam']} y {partidos[i]['awayTeam']}")
                print("Suma 1 punto \n")
            elif (golesLocalUsuario < golesVisitanteUsuario) and (golesLocalReal < golesVisitanteReal):
                puntuacion += 1
                print(f"{usuario} adivinó el resultado en el partido de {partidos[i]['homeTeam']} y {partidos[i]['awayTeam']}")
                print("Suma 1 punto \n")
            elif (golesLocalUsuario == golesVisitanteUsuario) and (golesLocalReal == golesVisitanteReal):
                puntuacion += 1
                print(f"{usuario} adivinó el resultado en el partido de {partidos[i]['homeTeam']} y {partidos[i]['awayTeam']}")
                print("Suma 1 punto \n")
        puntuaciones.append((usuario, puntuacion))
    return puntuaciones

def armarTablaDePosicionesDescendente(puntuaciones):
    """
    Ordena las puntuaciones de los usuarios en orden descendente.

    Utiliza el algoritmo de burbujeo para ordenar la lista de tuplas de puntuaciones.
    
    Args:
        puntuaciones (list): Lista de tuplas donde cada una representa el usuario y su puntuación.
    
    Returns:
        list: Lista de tuplas ordenada de mayor a menor puntuación.
        puntuaciones = [("lucas",3),("maria",1)]
    """
    for i in range(len(puntuaciones)):
        for j in range(0, len(puntuaciones) - i - 1):
            if puntuaciones[j][1] < puntuaciones[j + 1][1]:
                puntuaciones[j], puntuaciones[j + 1] = puntuaciones[j + 1], puntuaciones[j]
    return puntuaciones

def mostrarNombreGanadores(puntuacionesOrdenadas):
    """
    Muestra el nombre del ganador o ganadores (en caso de empate en la puntuación más alta).
    Args:
        puntuacionesOrdenadas (list): Lista de tuplas con los usuarios y sus puntuaciones, ordenada de mayor a menor.
        puntuaciones = [("lucas",3),("maria",1)]
    """
    mayorPuntuacion = puntuacionesOrdenadas[0][1]
    if mayorPuntuacion != 0:
        nombreGanadores = [usuario for usuario, puntos in puntuacionesOrdenadas if puntos == mayorPuntuacion]
        if len(nombreGanadores) > 1:
            print("Los ganadores son: ")
        else:
            print("El ganador es: ")
        for ganador in nombreGanadores:
                print(ganador)
    else:
        print("Nadie adivinó el resultado de ningún partido :( \n")


def mostrarTop3(puntuacionesOrdenadas):
    """
    Muestra los primeros 3 lugares de la tabla de posiciones.
    """
    print("Top 3 en la Tabla de Posiciones")
    print("---------------------")
    print("Usuario | Puntos")
    print("---------------------")
    for puntuacion in puntuacionesOrdenadas[:3]:  # Se usa rebanado para limitar los primeros 3.
        print(puntuacion[0].title() + " | " + str(puntuacion[1]))

def mostrarTablaDePosiciones(puntuacionesOrdenadas):
    """
    Muestra la tabla de posiciones en formato de texto si el usuario quiere.

    Args:
        puntuacionesOrdenadas (list): Lista de tuplas con los usuarios y sus puntuaciones, ordenada de mayor a menor.
    """
    decision = input("Desea ver la tabla de posiciones completa y la cantidad de puntos totales? (Ingrese la palabra 'si' o 'no')").lower()
    if decision == "si":
        print("Tabla de Posiciones")
        print("---------------------")
        print("Usuario | Puntos")
        print("---------------------")
        for puntuacion in puntuacionesOrdenadas:
            print(puntuacion[0].title() + " | " + str(puntuacion[1]))
        mostrarTotalDePuntuaciones(totalPuntuaciones)

def calcularTotalPuntos(puntuaciones):
    """
    Calcula el total de puntos acumulados por todos los usuarios.

    Args:
        puntuaciones (list): Lista de tuplas donde cada tupla contiene el usuario y su puntuación.

    Returns:
        int: El total de puntos acumulados por todos los usuarios.
    """
    return reduce(lambda acumulador, puntos: acumulador + puntos[1], puntuaciones, 0)

def mostrarTotalDePuntuaciones(puntuaciones):
    print("El numero total de puntuaciones es de: ", puntuaciones)

partidos = ingresarPartidos()

usuariosResultados = resultadoUsuarios(partidos)

partidosConResultado = generarResultadosAleatorios(partidos)

puntuaciones = calcularPuntuaciones(usuariosResultados, partidosConResultado)

puntuacionesOrdenadas = armarTablaDePosicionesDescendente(puntuaciones)

totalPuntuaciones = calcularTotalPuntos(puntuaciones)

mostrarNombreGanadores(puntuacionesOrdenadas)

mostrarTop3(puntuacionesOrdenadas)

mostrarTablaDePosiciones(puntuacionesOrdenadas)



