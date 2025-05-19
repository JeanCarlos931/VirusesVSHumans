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
        cantidad =+1
    elif nivel == 3:
        cantidad += 2
    else:
        raise ValueError ("El nivel máximo es 3")

    if cantidad > len(total_disponibles):
        cantidad = len(total_disponibles)  # evita pasarse

    posiciones = r.sample(total_disponibles, cantidad)

    for f, c in posiciones:
        m[f][c] = 9
        
        pass

def movimientos(m: list) -> list:
    filas = len(m)
    columnas = len(m[0])
    vida_virus = any(0 in fila for fila in m)
    turno = 1

    while vida_virus:
        print(f"Turno {turno}:")
        for fila in m:
            print(" ".join(str(celda) for celda in fila))
        print()
        time.sleep(0.5)

        # 1. Buscar todos los virus activos
        virus_activados = [(f, c) for f in range(filas) for c in range(columnas) if m[f][c] == 3]

        # 2. Seleccionar UN virus al azar
        if not virus_activados:
            break  # no hay más virus
        f, c = r.choice(virus_activados)

        # 3. Ver sus vecinos
        vecinos = [
            (f-1, c), (f+1, c), (f, c-1), (f, c+1)
        ]
        vecinos_validos = [
            (nf, nc) for nf, nc in vecinos
            if 0 <= nf < filas and 0 <= nc < columnas and m[nf][nc] == 0
        ]

        # 4. Si tiene a dónde ir, infecta una casilla
        if vecinos_validos:
            nuevo_f, nuevo_c = r.choice(vecinos_validos)
            m[nuevo_f][nuevo_c] = 3
            turno += 1
        else:
            # si ese virus no tiene a dónde ir, terminamos si ningún virus puede moverse
            puede_moverse = False
            for f, c in virus_activados:
                vecinos = [
                    (f-1, c), (f+1, c), (f, c-1), (f, c+1)
                ]
                if any(0 <= nf < filas and 0 <= nc < columnas and m[nf][nc] == 0 for nf, nc in vecinos):
                    puede_moverse = True
                    break
            if not puede_moverse:
                vida_virus = False

    # Mostrar último turno
    print(f"Turno {turno} (final):")
    for fila in m:
        print(" ".join(str(celda) for celda in fila))
    print()

    return m

"""asignar_pistas(nueva_matriz)
imprima_matriz(nueva_matriz)"""



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