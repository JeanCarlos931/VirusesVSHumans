import random as r
import time

def imprima_matriz(m:list)->None:
    for y in m:
        for x in y:
            print (x," ", end="")
        print("")

def crear_matriz(filas:int,columnas:int,elemento:any=None)->list:
    resultado:list=[]
    for _ in range (filas):
        nueva_fila=[]
        for _ in range (columnas):
            nueva_fila.append(elemento)
        resultado.append(nueva_fila)
    return (resultado)

