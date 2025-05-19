# -------------------------- 
# SECCIÓN 1: IMPORTS Y CONFIGURACIÓN
# --------------------------
import struct    # Para convertir números a bytes y viceversa
import os        # Para verificar tamaño de archivo
from tkinter import filedialog  # Para diálogos de archivo gráficos

# --------------------------
# SECCIÓN 2: GUARDAR PARTIDA
# --------------------------
def guardar_partida(nombre_archivo, matriz, nivel):
    """
    Función principal para guardar el estado del juego
    Parámetros:
    nombre_archivo: str - Ruta donde se guardará el archivo
    matriz: list - Matriz 2D del tablero (0,1,2)
    nivel: int - Nivel actual del jugador
    """
    tamaño_matriz = len(matriz)  # Obtener N de la matriz NxN
    
    with open(nombre_archivo, 'wb') as archivo:  # Abrir archivo en modo escritura binaria
        # 1. Escribir tamaño de matriz (2 bytes)
        # 'H' = formato para unsigned short (2 bytes)
        archivo.write(struct.pack('H', tamaño_matriz))  
        
        # 2. Escribir nivel (1 byte)
        # 'B' = formato para unsigned char (1 byte)
        archivo.write(struct.pack('B', nivel))  
        
        # 3. Escribir cada fila convertida a base 3
        for fila in matriz:
            # Convertir fila a número único en base 3
            numero_base3 = convertir_fila_a_numero(fila, tamaño_matriz)
            # Guardar como entero de 4 bytes sin signo ('I' = unsigned int)
            archivo.write(struct.pack('I', numero_base3))  

def convertir_fila_a_numero(fila, tamaño_matriz):
    """
    Convierte una fila de valores (0,1,2) en un número decimal 
    que representa la combinación en base 3
    Ejemplo: [0,1,2] → 0*3² + 1*3¹ + 2*3⁰ = 0 + 3 + 2 = 5
    """
    numero = 0
    for posicion, valor in enumerate(fila):
        # Calcular potencia correspondiente: desde 3^(N-1) hasta 3^0
        potencia = tamaño_matriz - posicion - 1
        # Sumar valor * 3^potencia
        numero += valor * (3 ** potencia)  
    return numero

# --------------------------
# SECCIÓN 3: CARGAR PARTIDA
# --------------------------
def cargar_partida(nombre_archivo):
    """Función principal para cargar una partida guardada"""
    with open(nombre_archivo, 'rb') as archivo:  # Abrir en modo lectura binaria
        # 1. Leer tamaño de matriz (primeros 2 bytes)
        # 'H' para desempaquetar unsigned short
        tamaño_matriz = struct.unpack('H', archivo.read(2))[0]  
        
        # 2. Leer nivel (siguiente byte)
        # 'B' para unsigned char
        nivel = struct.unpack('B', archivo.read(1))[0]  
        
        # 3. Verificar integridad del archivo
        # Tamaño esperado = 2 (tamaño) + 1 (nivel) + 4*N (filas)
        tamaño_esperado = 2 + 1 + 4 * tamaño_matriz
        # Comparar con tamaño real del archivo
        if os.path.getsize(nombre_archivo) != tamaño_esperado:  
            raise ValueError("Archivo dañado o incompatible")
        
        # 4. Reconstruir matriz
        matriz = []
        for _ in range(tamaño_matriz):  # Por cada fila esperada
            # Leer 4 bytes y convertirlos a entero ('I')
            numero = struct.unpack('I', archivo.read(4))[0]  
            # Convertir número a fila original
            fila = convertir_numero_a_fila(numero, tamaño_matriz)
            matriz.append(fila)
            
    return matriz, nivel

def convertir_numero_a_fila(numero, tamaño_matriz):
    """
    Reconstruye una fila a partir del número en base 3
    Ejemplo: 5 → [0,1,2] (5 = 0*3² + 1*3¹ + 2*3⁰)
    """
    fila = []
    for posicion in range(tamaño_matriz):  # Para cada celda en la fila
        # Calcular la potencia actual (de mayor a menor)
        potencia = tamaño_matriz - posicion - 1
        divisor = 3 ** potencia
        # Obtener el dígito correspondiente
        valor = numero // divisor  
        fila.append(valor)
        # Actualizar el número con el resto
        numero %= divisor  # Ej: 5 % 3² = 5 % 9 = 5 → siguiente iteración 5/3¹ = 1
    return fila

# --------------------------
# SECCIÓN 4: INTERFAZ GRÁFICA
# --------------------------
def guardar_desde_interfaz(matriz, nivel):
    """
    Muestra diálogo para seleccionar ubicación de guardado
    Parámetros iguales a guardar_partida
    """
    archivo = filedialog.asksaveasfilename(
        defaultextension=".vsc",  # Extensión predeterminada
        filetypes=[("Partidas Virus Spread", "*.vsc")]  # Filtro de archivos
    )
    if archivo:  # Si el usuario no canceló
        guardar_partida(archivo, matriz, nivel)

def cargar_desde_interfaz():
    """
    Muestra diálogo para seleccionar archivo a cargar
    Devuelve:
    - matriz: list - Matriz cargada
    - nivel: int - Nivel cargado
    Si se cancela, devuelve lista vacía y nivel 0
    """
    archivo = filedialog.askopenfilename(
        filetypes=[("Partidas Virus Spread", "*.vsc")]
    )
    if archivo:
        return cargar_partida(archivo)
    return [], 0  # Valores por defecto si se cancela

# --------------------------
# SECCIÓN 5: EJEMPLO DE USO
# --------------------------
if __name__ == "__main__":
    # Datos de prueba (matriz 3x3)
    matriz_prueba = [
        [0, 1, 0],  # Fila 1
        [2, 1, 0],  # Fila 2
        [0, 0, 1]   # Fila 3
    ]
    nivel_prueba = 2
    
    # Demostración de guardado
    guardar_partida("partida_prueba.vsc", matriz_prueba, nivel_prueba)
    
    # Demostración de carga
    matriz_cargada, nivel_cargado = cargar_partida("partida_prueba.vsc")
    
    # Verificación visual
    print(f"Nivel cargado: {nivel_cargado}")
    print("Matriz reconstruida:")
    for fila in matriz_cargada:
        print(fila)  # Debería coincidir con matriz_prueba