import pytest
from prograprode import (
    validarNombre,
    calcularTotalPuntos,
    armarTablaDePosicionesDescendente,
    mostrarUltimos3Recursivo,
    generarResultadosAleatorios,
    calcularPuntuaciones
)

def test_generar_resultados_aleatorios():
    partidos = [
        {"homeTeam": "Boca", "awayTeam": "River", "homeScore": -1, "awayScore": -1},
        {"homeTeam": "Ferro", "awayTeam": "Independiente", "homeScore": -1, "awayScore": -1}
    ]
    partidos_resultados = generarResultadosAleatorios(partidos)
    
    # Verifica que los resultados tengan los campos esperados
    assert len(partidos_resultados) == 2
    assert "homeTeam" in partidos_resultados[0]
    assert "awayTeam" in partidos_resultados[0]
    assert "homeScore" in partidos_resultados[0]
    assert "awayScore" in partidos_resultados[0]
    assert partidos_resultados[0]["homeScore"] >= 0  # Los goles no pueden ser negativos
    assert partidos_resultados[0]["awayScore"] >= 0
    
def test_calcular_puntuaciones():
    partidos = [
        {"homeTeam": "Boca", "awayTeam": "River", "homeScore": 2, "awayScore": 1},
        {"homeTeam": "Ferro", "awayTeam": "Independiente", "homeScore": 1, "awayScore": 1}
    ]
    usuarioResultados = {
        "lucas": [
            {"homeTeam": "Boca", "awayTeam": "River", "predHomeScore": 2, "predAwayScore": 1},
            {"homeTeam": "Ferro", "awayTeam": "Independiente", "predHomeScore": 1, "predAwayScore": 1}
        ],
        "maria": [
            {"homeTeam": "Boca", "awayTeam": "River", "predHomeScore": 1, "predAwayScore": 2},
            {"homeTeam": "Ferro", "awayTeam": "Independiente", "predHomeScore": 1, "predAwayScore": 0}
        ]
    }
    
    puntuaciones = calcularPuntuaciones(usuarioResultados, partidos)
    
    # Verifica que las puntuaciones esten calculadas correctamente
    assert puntuaciones == [("lucas", 6), ("maria", 0)]

def test_validar_nombre():
    assert validarNombre("Lucas") == True
    assert validarNombre("María") == True
    assert validarNombre("Juan Pablo") == True
    assert validarNombre("123") == False
    assert validarNombre("Juan123") == False
    assert validarNombre("") == False
    assert validarNombre(" ") == False

def test_calcular_total_puntos():
    puntuaciones = [("Lucas", 5), ("María", 3), ("Juan", 7)]
    assert calcularTotalPuntos(puntuaciones) == 15

def test_armar_tabla_de_posiciones_descendente():
    puntuaciones = [("Lucas", 3), ("María", 1), ("Juan", 7)]
    resultado_esperado = [("Juan", 7), ("Lucas", 3), ("María", 1)]
    assert armarTablaDePosicionesDescendente(puntuaciones) == resultado_esperado


def test_calcular_puntuaciones_con_listas_vacias():
    usuarioResultados = {}
    partidos = []
    puntuaciones = calcularPuntuaciones(usuarioResultados, partidos)
    
    assert puntuaciones == []
    
def test_armar_tabla_de_posiciones_con_empates():
    puntuaciones = [("Lucas", 5), ("María", 5), ("Juan", 7), ("Pedro", 3)]
    resultado_esperado = [("Juan", 7), ("Lucas", 5), ("María", 5), ("Pedro", 3)]
    
    assert armarTablaDePosicionesDescendente(puntuaciones) == resultado_esperado