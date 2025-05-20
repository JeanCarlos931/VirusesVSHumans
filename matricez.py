import random as r
import time

def imprima_matriz(m:list)->None:
    """_summary_

    Args:
        m (list): _description_
    """
    for y in m:
        for x in y:
            print (x," ", end="")
        print("")

def crear_matriz(filas:int,columnas:int,elemento:any=None)->list:
    """_summary_

    Args:
        filas (int): _description_
        columnas (int): _description_
        elemento (any, optional): _description_. Defaults to None.

    Returns:
        list: _description_
    """
    resultado:list=[]
    for _ in range (filas):
        nueva_fila=[]
        for _ in range (columnas):
            nueva_fila.append(elemento)
        resultado.append(nueva_fila)
    return (resultado)

