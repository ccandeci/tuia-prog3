"""
Módulo de estrategias para el juego del Tateti

Este módulo contiene las estrategias para elegir la acción a realizar.
Los alumnos deben implementar la estrategia minimax.

Por defecto, se incluye una estrategia aleatoria como ejemplo base.
"""

import random
from typing import List, Tuple
from tateti import Tateti, JUGADOR_MAX, JUGADOR_MIN

def estrategia_aleatoria(tateti: Tateti, estado: List[List[str]]) -> Tuple[int, int]:
    """
    Estrategia aleatoria: elige una acción al azar entre las disponibles.
  
    Args:
        tateti: Instancia de la clase Tateti
        estado: Estado actual del tablero
        
    Returns:
        Tuple[int, int]: Acción elegida (fila, columna)

    Raises:
        ValueError: Si no hay acciones disponibles
    """
    acciones_disponibles = tateti.acciones(estado)
    if not acciones_disponibles:
        raise ValueError("No hay acciones disponibles")
    
    return random.choice(acciones_disponibles)

def estrategia_minimax(tateti: Tateti, estado: List[List[str]]) -> Tuple[int, int]:
    """
    Estrategia minimax: elige la mejor acción usando el algoritmo minimax.

    La utilidad siempre se mide desde la perspectiva de JUGADOR_MAX
    (1.0 si gana MAX, 0.0 si gana MIN, 0.5 si hay empate). Si le toca mover
    a MAX se elige la acción de mayor valor; si le toca a MIN, la de menor valor.
    Args:
        tateti: Instancia de la clase Tateti
        estado: Estado actual del tablero
    Returns:
        Tuple[int, int]: Acción elegida (fila, columna)
    Raises:
        ValueError: Si no hay acciones disponibles
    """
    # Primero me fijo qué casillas están libres para poder jugar
    acciones_disponibles = tateti.acciones(estado)

    # Si no queda ninguna casilla libre, tiro error
    if not acciones_disponibles:
        raise ValueError("No hay acciones disponibles")

    def valor_max(est: List[List[str]]) -> float:
        """Valor de un estado en el que mueve MAX: el mejor valor para MAX."""

        # si el juego ya terminó, no sigo explorando y devuelvo cómo le fue a MAX
        # (1 si ganó, 0 si perdió, 0.5 si empató) -> caso base
        if tateti.test_terminal(est):
            return tateti.utilidad(est, JUGADOR_MAX)

        # empiezo en -infinito para que cualquier valor que encuentre sea mejor
        v = float("-inf")

        # pruebo todas las jugadas que puede hacer MAX
        for a in tateti.acciones(est):
            # después de que juega MAX le toca a MIN, por eso llamo a valor_min
            # me quedo con el valor más grande porque MAX quiere maximizar
            v = max(v, valor_min(tateti.resultado(est, a)))
        return v

    def valor_min(est: List[List[str]]) -> float:
        """Valor de un estado en el que mueve MIN: el mejor valor para MIN."""
        # mismo caso base de arriba. Uso JUGADOR_MAX también acá porque
        # la utilidad siempre la mido desde el punto de vista de MAX
        if tateti.test_terminal(est):
            return tateti.utilidad(est, JUGADOR_MAX)

        # acá empiezo en +infinito porque ahora busco el valor más chico
        v = float("inf")

        # pruebo todas las jugadas que puede hacer MIN
        for a in tateti.acciones(est):
            # después de que juega MIN le toca a MAX, por eso llamo a valor_max
            # me quedo con el valor más chico porque MIN quiere minimizar
            v = min(v, valor_max(tateti.resultado(est, a)))
        return v

    # el que mueve ahora determina si se maximiza o se minimiza
    # contamos fichas con tateti.jugador y veo si le toca a MAX
    es_turno_max = tateti.jugador(estado) == JUGADOR_MAX

    # guardamos  la mejor jugada que encuentro
    mejor_accion = None
    # el valor inicial depende de quién juega: si es MAX arranco en -inf
    # y si es MIN arranco en +inf, así la primera jugada ya lo mejora
    mejor_valor = float("-inf") if es_turno_max else float("inf")

    # recorremos todas las jugadas posibles del tablero actual
    for accion in acciones_disponibles:
        # armamos el tablero que quedaría si hago esta jugada
        sucesor = tateti.resultado(estado, accion)

        if es_turno_max:
            # si juego como MAX, después mueve MIN, así que uso valor_min
            valor = valor_min(sucesor)
            # si esta jugada es mejor que la que tenía, me la guardo
            if valor > mejor_valor:
                mejor_valor, mejor_accion = valor, accion
        else:
            # si juego como MIN, después mueve MAX, así que uso valor_max
            valor = valor_max(sucesor)
            # como MIN quiere el valor más chico, guardo la jugada si es menor
            if valor < mejor_valor:
                mejor_valor, mejor_accion = valor, accion

    # devuelvemos la mejor jugada que encontré (fila, columna)
    return mejor_accion