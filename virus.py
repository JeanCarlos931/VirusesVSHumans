import random as r
import time

def agregar_virus(m: list, cantidad: int = 1, nivel: int= 1) -> None:
    """
    Agrega 'cantidad' de virus (representados con el número 9)
    en posiciones aleatorias de una matriz (lista de listas).

    Args:
        m (list): La matriz a modificar.
        cantidad (int): Número de virus a colocar. Por defecto 10.

    Returns:
        None: La matriz es modificada directamente.
    """
    filas = len(m)
    columnas = len(m[0])
    total_disponibles = [(f, c) for f in range(filas) for c in range(columnas) if m[f][c] == 0]

    if nivel == 1:
        cantidad = 1
    elif nivel == 2:
        cantidad +=1
    elif nivel == 3:
        cantidad += 2
    else:
        raise ValueError ("El nivel máximo es 3")

    if cantidad > len(total_disponibles):
        cantidad = len(total_disponibles)  # evita pasarse

    posiciones = r.sample(total_disponibles, cantidad)

    for f, c in posiciones:
        m[f][c] = 1
        
        pass

def obtener_vecinos_validos(m, f, c):
    filas = len(m)
    columnas = len(m[0])
    vecinos = [(f-1, c), (f+1, c), (f, c-1), (f, c+1)]
    return [(nf, nc) for nf, nc in vecinos if 0 <= nf < filas and 0 <= nc < columnas and m[nf][nc] == 0]

def avanzar_virus(matriz):
    filas = len(matriz)
    columnas = len(matriz[0])
    virus_activados = [(f, c) for f in range(filas) for c in range(columnas) if matriz[f][c] == 3]
    
    for f, c in virus_activados:
        vecinos = obtener_vecinos_validos(matriz, f, c)
        if vecinos:
            nf, nc = r.choice(vecinos)
            matriz[nf][nc] = 3
            break

