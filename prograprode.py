import random
import re
from functools import reduce

golesPosibles = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
probabilidadGoles = [0.25, 0.3, 0.2, 0.15, 0.05, 0.03, 0.01, 0.005, 0.002, 0.001]

def registrarExcepcion(e):
    """ Función para registrar excepciones en un archivo de log """
    try:
        archivo = open('errores.log', 'a')
        try:
            error = f"Tipo: {type(e)} - Mensaje: {str(e)}\n"
            print(f"Ocurrió un error: {error}")
            archivo.write(error)
        finally:
            archivo.close()
    except Exception as logError:
        print(f"Error al escribir en el log: {logError}")

def ingresarPartidos():
    """
    Lee los partidos desde un archivo y los almacena en una lista de diccionarios.
    Cada línea del archivo representa un partido con el formato 'EquipoLocal,EquipoVisitante'.
    
    Returns:
        list: Lista de diccionarios con los detalles de cada partido.
        [
            {"homeTeam": "Boca", "awayTeam": "River", "predHomeScore": -1, "predAwayScore": -1},
            {"homeTeam": "Ferro", "awayTeam": "River", "predHomeScore": -1, "predAwayScore": -1},
        ]
    """
    partidos = []
    
    try:
        # Abre el archivo y procesa cada linea
        archivo = open("partidos.txt", "r")
        for linea in archivo:
            equipos = linea.strip().split(",")  # Elimina espacios al principio, final y saltos de linea, y separa por coma
            if len(equipos) == 2:  # Verifica que haya exactamente dos equipos
                partido = {
                    "homeTeam": equipos[0],
                    "awayTeam": equipos[1],
                    "homeScore": -1,
                    "awayScore": -1,
                }
                partidos.append(partido)
            else:
                print("Línea con formato incorrecto:", linea)
        archivo.close()
    
    except FileNotFoundError as e:
        registrarExcepcion(e)
        print("Intente nuevamente.")
    
    except Exception as e:
        registrarExcepcion(e)
        print("Intente nuevamente.")
    
    return partidos

def resultadoUsuarios(partidos):
    """
    Permite a los usuarios ingresar sus predicciones para una lista de partidos.
    
    Se solicita al usuario ingresar su nombre y predecir los goles para cada partido.
    Las predicciones se almacenan en un diccionario, donde la clave es el nombre del usuario
    y el valor es una lista de diccionarios donde cada diccionario representa la prediccion de un partido.
    
    Args:
        partidos (list): Lista de diccionarios que representan los partidos.
        partidosConResultado = [
            {"homeTeam": "Boca", "awayTeam": "River", "homeScore": 1, "awayScore": 1},
            {"homeTeam": "Ferro", "awayTeam": "River", homeScore: 2, "awayScore": 0}
        ]
    
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
    
    while True:
        nombreUsuario = input("Ingrese el nombre del usuario ('fin' para salir no son validos los numeros ni un nombre vacio): ").lower()
        if nombreUsuario == 'fin':
            break
        
        try:
            if nombreUsuario in usuarioResultados:
                raise ValueError("El nombre ya ha sido ingresado.")
            
            if not validarNombre(nombreUsuario):
                raise ValueError("El nombre ingresado no es valido. No debe contener numeros.")
            
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
                        registrarExcepcion(e)
                        print("Intente nuevamente.")
                
                while True:
                    try:
                        predAwayScore = int(input(f"Ingrese goles de {partido['awayTeam']}: "))
                        if predAwayScore < 0:
                            raise ValueError("Los goles no pueden ser negativos.")
                        break
                    except ValueError as e:
                        registrarExcepcion(e)
                        print("Intente nuevamente.")

                usuarioResultados[nombreUsuario].append({
                    "homeTeam": partido['homeTeam'],
                    "awayTeam": partido['awayTeam'],
                    "predHomeScore": predHomeScore,
                    "predAwayScore": predAwayScore,
                })
        except ValueError as e:
            registrarExcepcion(e)
            continue
        
    return usuarioResultados

def validarNombre(nombre):
    """
    Verifica que el nombre ingresado no sea un número y que sea valido (permitiendo letras, tildes, diéresis y espacios 
    entre las palabras, pero no permitiendo solo espacios ni nombres vacíos).
    
    Args:
        nombre (str): El nombre ingresado por el usuario.
    
    Returns:
        bool: True si el nombre es valido, False si es un nombre invalido.
    """
    # La expresión regular verifica si el nombre contiene letras (incluyendo tildes y diéresis)
    # y al menos un espacio entre palabras, pero no permite nombres con solo espacios.
    if re.match("^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ]+(?:[ ]+[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ]+)*$", nombre):
        return True
    else:
        return False

def generarResultadosAleatorios(partidos):
    """
    Asigna resultados aleatorios teniendo en cuenta los goles con mayor posibilidad 
    a cada partido, los imprime y los guarda en un archivo.
    
    Args:
        partidos (list): Lista de diccionarios que representan los partidos.
    
    Returns:
        list: La lista de partidos con los resultados asignados.
    """
    try:
        archivo = open("resultados_partidos.txt", "w")
        for partido in partidos:
            partido['homeScore'] = random.choices(golesPosibles, probabilidadGoles)[0]
            partido['awayScore'] = random.choices(golesPosibles, probabilidadGoles)[0]
            resultado = f"{partido['homeTeam']} {partido['homeScore']} - {partido['awayScore']} {partido['awayTeam']}\n"
            print(f"El Partido: {partido['homeTeam']} vs {partido['awayTeam']} tuvo el resultado de:")
            print(resultado.strip())  
            archivo.write(resultado) 
            print("Los resultados se guardaron en 'resultados_partidos.txt'.")
    except Exception as e:
        registrarExcepcion(e)
    finally:
        archivo.close()
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
                print(f"{usuario.title()} adivinó el resultado exacto en el partido de {partidos[i]['homeTeam']} y {partidos[i]['awayTeam']}")
                print("Suma 3 puntos \n")
            elif (golesLocalUsuario > golesVisitanteUsuario) and (golesLocalReal > golesVisitanteReal):
                puntuacion += 1
                print(f"{usuario.title()} adivinó el resultado en el partido de {partidos[i]['homeTeam']} y {partidos[i]['awayTeam']}")
                print("Suma 1 punto \n")
            elif (golesLocalUsuario < golesVisitanteUsuario) and (golesLocalReal < golesVisitanteReal):
                puntuacion += 1
                print(f"{usuario.title()} adivinó el resultado en el partido de {partidos[i]['homeTeam']} y {partidos[i]['awayTeam']}")
                print("Suma 1 punto \n")
            elif (golesLocalUsuario == golesVisitanteUsuario) and (golesLocalReal == golesVisitanteReal):
                puntuacion += 1
                print(f"{usuario.title()} adivinó el resultado en el partido de {partidos[i]['homeTeam']} y {partidos[i]['awayTeam']}")
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
                print(ganador.title())
    else:
        print("Nadie adivinó el resultado de ningún partido :( \n")


def mostrarTop3(puntuacionesOrdenadas):
    """
    Muestra los primeros 3 lugares de la tabla de posiciones y los guarda en un archivo.
    
    Args:
        list: Lista de tuplas ordenada de mayor a menor puntuación.
        puntuaciones = [("lucas",3),("maria",1)]
    """
    print("Top 3 en la Tabla de Posiciones")
    print("---------------------")
    print("Usuario | Puntos")
    print("---------------------")
    
    try:
        archivo = open("top3_posiciones.txt", "w")
        for puntuacion in puntuacionesOrdenadas[:3]: 
            linea = f"{puntuacion[0].title()} | {puntuacion[1]}"
            print(linea) 
            archivo.write(linea + "\n") 
        print("\nEl Top 3 se guardó en 'top3_posiciones.txt'.\n")
    except Exception as e:
        registrarExcepcion(e)
    finally:
        archivo.close()

def mostrarUltimos3Recursivo(puntuacionesOrdenadas):
    """
    Muestra recursivamente las últimas 3 posiciones de la tabla de puntuaciones.
    
    Args:
        list: Lista de tuplas ordenada de mayor a menor puntuación.
        puntuaciones = [("lucas",3),("maria",1)]
    """
    
    if len(puntuacionesOrdenadas) == 3:  # Caso base: si quedan 3 elementos, se imprimen.
        try:
            archivo = open("ultimas3_posiciones.txt", "w")
            print("Últimos 3 en la Tabla de Posiciones")
            print("---------------------")
            print("Usuario | Puntos")
            print("---------------------")
            for usuario, puntos in puntuacionesOrdenadas:
                linea = f"{usuario.title()} | {puntos}"
                print(linea)
                archivo.write(linea + "\n")
            print("\Los ultimos 3 se guardaron en 'ultimas3_posiciones.txt'.\n")
        except Exception as e:
            registrarExcepcion(e)
        finally:
            archivo.close()
    else:
        # Llamada recursiva eliminando el primer elemento hasta que queden 3.
        mostrarUltimos3Recursivo(puntuacionesOrdenadas[1:])


def mostrarTablaDePosiciones(puntuacionesOrdenadas):
    """
    Muestra la tabla de posiciones en formato de texto y la guarda en un archivo si el usuario quiere.

    Args:
        puntuacionesOrdenadas (list): Lista de tuplas con los usuarios y sus puntuaciones, ordenada de mayor a menor.
    """
    decision = input("¿Desea ver la tabla de posiciones completa y la cantidad de puntos totales? (Ingrese 'si' o 'no'): ").lower()
    if decision == "si":
        try:
            archivo = open("tabla_posiciones.txt", "w")
            
            print("Tabla de Posiciones")
            archivo.write("Tabla de Posiciones\n")
            
            print("---------------------")
            archivo.write("---------------------\n")
            
            print("Usuario | Puntos")
            archivo.write("Usuario | Puntos\n")
            
            print("---------------------")
            archivo.write("---------------------\n")
            
            # Filas de la tabla
            for puntuacion in puntuacionesOrdenadas:
                linea = f"{puntuacion[0].title()} | {puntuacion[1]}"
                print(linea)  
                archivo.write(linea + "\n") 
            
            # Total de puntos
            totalPuntos = calcularTotalPuntos(puntuacionesOrdenadas)
            totalTexto = f"\nTotal de puntos: {totalPuntos}"
            print(totalTexto)
            archivo.write(totalTexto + "\n")
            
            print("\nLa tabla de posiciones se guardó en 'tabla_posiciones.txt'.\n")
        except Exception as e:
            registrarExcepcion(e)
        finally:
            archivo.close()
    print("Fin del programa")

def calcularTotalPuntos(puntuaciones):
    """
    Calcula el total de puntos acumulados por todos los usuarios.
    Args:
        puntuaciones (list): Lista de tuplas donde cada tupla contiene el usuario y su puntuación.
        puntuaciones = [("lucas",3),("maria",1)]
    Returns:
        int: El total de puntos acumulados por todos los usuarios.
    """
    return reduce(lambda acumulador, puntos: acumulador + puntos[1], puntuaciones, 0)

def mostrarTotalDePuntuaciones(puntuaciones):
    print("El numero total de puntuaciones es de: ", puntuaciones)

if __name__== "__main__":
    partidos = ingresarPartidos()

    usuariosResultados = resultadoUsuarios(partidos)

    if len(usuariosResultados) > 0:
        partidosConResultado = generarResultadosAleatorios(partidos)

        puntuaciones = calcularPuntuaciones(usuariosResultados, partidosConResultado)

        puntuacionesOrdenadas = armarTablaDePosicionesDescendente(puntuaciones)

        totalPuntuaciones = calcularTotalPuntos(puntuaciones)

        mostrarNombreGanadores(puntuacionesOrdenadas)

        mostrarTop3(puntuacionesOrdenadas)

        mostrarUltimos3Recursivo(puntuacionesOrdenadas)

        mostrarTablaDePosiciones(puntuacionesOrdenadas)