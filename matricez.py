matriz=[[1,2,3],
        [4,5,6]]

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

def crear_matriz(filas:int,columnas:int,elemento:any=None)->list:
    return [[elemento for _ in range (columnas)] for _ in range (filas)]


def diagonal (m:list)->list:
    if len(m)==0 and len(m)!=len(m[0]):
        return []
    else:
        resultado=[]
        cont=0
        while cont<len(m):
            resultado.append(m[cont][cont])
            cont+=1
        return (resultado)

nueva_matriz=crear_matriz(10,10,0)

import random as r

def agregar_minas (m:list,porcentaje:int=10)->None:
    """
    Agrega minas a una matriz representada como una lista de listas.

    Las minas se representan con el número 9 y se colocan aleatoriamente
    en la matriz. El porcentaje de celdas que contendrán minas se especifica
    como un parámetro.

    Args:
        m (list): La matriz en la que se agregarán las minas. Debe ser una lista
                de listas donde cada sublista representa una fila.
        porcentaje (int, opcional): El porcentaje de celdas que contendrán minas.
                                    Por defecto es 10.

    Returns:
        None: Esta función modifica la matriz proporcionada directamente.
    """
    filas=len(m)
    columnas=len(m[0])
    cont=(porcentaje*(filas*columnas))//100
    while cont>0:
        nf=r.randint(0,filas-1)
        nc=r.randint(0,columnas-1)
        if m[nf][nc]==0:
            m[nf][nc]=9
            cont-=1
        else:
            pass

def es_mina (m:list,y:int,x:int)->bool:
    """
    Determina si una posición específica en una matriz corresponde a una mina.

    Args:
        m (list): Una matriz bidimensional representada como una lista de listas de enteros.
                    Se asume que el valor 9 representa una mina.
        y (int): La coordenada vertical (fila) de la posición a verificar.
        x (int): La coordenada horizontal (columna) de la posición a verificar.

    Returns:
        bool: Retorna True si la posición (y, x) está dentro de los límites de la matriz
                y contiene una mina (valor 9). Retorna False en caso contrario.
    """
    if x>=0 and x<len(m[0]) and y>=0 and y<len(m):
        if m[y][x]==9:
            return(True)
    else: 
        return False

def asignar_pistas(m:list):
    """
    Modifica una matriz representando un tablero de buscaminas para asignar pistas
    numéricas en las celdas que no contienen minas. Las pistas indican la cantidad
    de minas adyacentes a cada celda.

    Args:
        m (list): Una matriz bidimensional (lista de listas) donde cada celda contiene
                    un número entero. El valor 9 representa una mina, y cualquier otro
                    valor será reemplazado por el número de minas adyacentes.

    Notas:
        - La función asume que la matriz es rectangular (todas las filas tienen la misma longitud).
        - Las celdas en los bordes y esquinas se manejan correctamente, evitando accesos fuera
            de los límites de la matriz.
        - La función utiliza una función auxiliar `es_mina` (no incluida en este fragmento) para
            verificar si una celda específica contiene una mina.
    """
    for y in range (len(m)):
        for x in range (len(m[0])):
            if m[y][x]!=9: 
                vecinos=0
                if es_mina(m,y-1,x-1):
                    vecinos+=1
                if es_mina(m,y-1,x):
                    vecinos+=1
                if es_mina(m,y-1,x+1):
                    vecinos+=1
                if es_mina(m,y,x-1):
                    vecinos+=1
                if es_mina(m,y,x+1):
                    vecinos+=1
                if es_mina(m,y+1,x-1):
                    vecinos+=1
                if es_mina(m,y+1,x):
                    vecinos+=1
                if es_mina(m,y+1,x+1):
                    vecinos+=1
                m[y][x]=vecinos

agregar_minas(nueva_matriz,porcentaje=20)
asignar_pistas(nueva_matriz)

imprima_matriz(nueva_matriz)

