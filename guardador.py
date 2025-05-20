import struct
import os

def guardar_partida(nombre_archivo, matriz, nivel):
    """
    Guarda el estado del juego en un archivo binario.
    
    Parámetros:
    - nombre_archivo: str, nombre del archivo donde se guardará (sin extensión .bin).
    - matriz: lista de listas, con valores 0 (libre), 1 (virus), 2 (barrera).
    - nivel: int, nivel actual del jugador.
    """
    # Asegurarse de que la matriz es cuadrada
    n = len(matriz)
    if any(len(fila) != n for fila in matriz):
        raise ValueError("La matriz debe ser cuadrada (NxN)")

    with open(nombre_archivo + ".bin", "wb") as f:
        # Escribir las dimensiones de la matriz (2 bytes, unsigned short)
        f.write(struct.pack(">H", n))

        # Escribir el nivel actual (1 byte, unsigned char)
        f.write(struct.pack("B", nivel))

        # Codificar cada fila en base 3 y luego pasarla a hexadecimal
        for fila in matriz:
            base3_str = ''.join(str(celda) for celda in fila)  # Ej: "01201"
            base10 = int(base3_str, 3)  # Convertir base 3 a base 10
            num_bytes = (base10.bit_length() + 7) // 8 or 1  # Asegurar al menos 1 byte
            f.write(base10.to_bytes(num_bytes, byteorder="big"))

            

def cargar_partida(nombre_archivo):
    """
    Carga una partida desde un archivo binario y devuelve un diccionario
    con 'nivel' y 'matriz'.

    Retorna:
    {
        'nivel': int,
        'matriz': list[list[int]]
    }
    """
    nombre_bin = nombre_archivo + ".bin"

    if not os.path.exists(nombre_bin):
        raise FileNotFoundError(f"No se encontró el archivo: {nombre_bin}")

    with open(nombre_bin, "rb") as f:
        # Leer la dimensión de la matriz (2 bytes)
        n_bytes = f.read(2)
        if len(n_bytes) < 2:
            raise ValueError("Archivo corrupto o incompleto.")
        n = struct.unpack(">H", n_bytes)[0]

        # Leer el nivel (1 byte)
        nivel_byte = f.read(1)
        if len(nivel_byte) < 1:
            raise ValueError("Archivo corrupto: falta el nivel.")
        nivel = struct.unpack("B", nivel_byte)[0]

        matriz = []
        for _ in range(n):
            # Calculamos la cantidad máxima de bytes necesarios
            max_valor_base3 = int("2" * n, 3)
            max_bytes = (max_valor_base3.bit_length() + 7) // 8
            fila_bytes = f.read(max_bytes)

            if len(fila_bytes) == 0:
                raise ValueError("Archivo corrupto: faltan filas de la matriz.")

            valor_base10 = int.from_bytes(fila_bytes, byteorder="big")
            valor_base3 = ""
            while valor_base10 > 0:
                valor_base3 = str(valor_base10 % 3) + valor_base3
                valor_base10 //= 3

            valor_base3 = valor_base3.zfill(n)  # Rellenar con ceros si es necesario
            fila = [int(c) for c in valor_base3]
            matriz.append(fila)

        return {
            "nivel": nivel,
            "matriz": matriz
        }