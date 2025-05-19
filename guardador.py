import pickle

def guardar_en_binario(int1, int2, lista, filename="data.bin"):
    datos = {
        'int1': int1,
        'int2': int2,
        'lista': lista
    }
    with open(filename, 'wb') as archivo:
        pickle.dump(datos, archivo)
    print("Datos guardados en binario.")

def cargar_desde_binario(filename="data.bin"):
    with open(filename, 'rb') as archivo:
        datos = pickle.load(archivo)
    print("Datos cargados desde el archivo:")
    return datos

# Ejemplo de uso:
if __name__ == "__main__":
    # Variables de entrada
    a = 42
    b = 1337
    lista = [1, 2, 3, 4, 5]

    # Guardar en archivo binario
    guardar_en_binario(a, b, lista)

    # Cargar del archivo binario
    datos_recuperados = cargar_desde_binario()
    print(datos_recuperados)
