import struct
import os

def guardar_partida(nombre_archivo, nivel, longitud, matriz):
    """
    Guarda el estado del juego en un archivo binario.
    
    Parámetros:
    - nombre_archivo: str, nombre del archivo donde se guardará (sin extensión .bin).
    - nivel: int, nivel actual del jugador.
    - longitud: int, tamaño de la matriz (debe coincidir con len(matriz)).
    - matriz: lista de listas, con valores 0 (libre), 1 (virus), 2 (barrera).
    """
    if len(matriz) != longitud or any(len(fila) != longitud for fila in matriz):
        raise ValueError("La matriz debe ser cuadrada y coincidir con la longitud indicada.")

    with open(nombre_archivo + ".bin", "wb") as f:
        # Guardar nivel y longitud (1 byte cada uno)
        f.write(struct.pack("B", nivel))      # 1 byte
        f.write(struct.pack("B", longitud))   # 1 byte

        # Guardar cada fila codificada en base 3 como entero
        for fila in matriz:
            base3_str = ''.join(str(celda) for celda in fila)
            base10 = int(base3_str, 3)
            num_bytes = (base10.bit_length() + 7) // 8 or 1
            f.write(base10.to_bytes(num_bytes, byteorder="big"))


def cargar_partida(nombre_archivo):
    """
    Carga una partida desde un archivo binario y devuelve un diccionario
    con 'nivel', 'longitud' y 'matriz'.

    Retorna:
    {
        'nivel': int,
        'longitud': int,
        'matriz': list[list[int]]
    }
    """
    nombre_bin = nombre_archivo + ".bin"

    if not os.path.exists(nombre_bin):
        raise FileNotFoundError(f"No se encontró el archivo: {nombre_bin}")

    with open(nombre_bin, "rb") as f:
        # Leer nivel y longitud (1 byte cada uno)
        nivel_byte = f.read(1)
        longitud_byte = f.read(1)


        nivel = struct.unpack("B", nivel_byte)[0]
        longitud = struct.unpack("B", longitud_byte)[0]

        matriz = []
        for _ in range(longitud):
            max_valor_base3 = int("2" * longitud, 3)
            max_bytes = (max_valor_base3.bit_length() + 7) // 8
            fila_bytes = f.read(max_bytes)

            

            valor_base10 = int.from_bytes(fila_bytes, byteorder="big")

            # Convertir a base 3
            base3_str = ""
            while valor_base10 > 0:
                base3_str = str(valor_base10 % 3) + base3_str
                valor_base10 //= 3

            base3_str = base3_str.zfill(longitud)
            fila = [int(c) for c in base3_str]
            matriz.append(fila)

        return {
            "nivel": nivel,
            "longitud": longitud,
            "matriz": matriz
        }
