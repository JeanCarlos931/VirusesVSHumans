import struct

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