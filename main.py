from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,
    QGridLayout, QStackedWidget, QHBoxLayout, QSpacerItem, QSizePolicy, 
    QLineEdit,
)
from PyQt6.QtCore import Qt, QTimer
from guardador import guardar_partida, cargar_partida
import os
import sys
from virus import agregar_virus, avanzar_virus, obtener_vecinos_validos
import random as r

class pantalla_juego(QWidget):
    def __init__(self, longitud, nivel, stack, nombre_guardado):
        super().__init__()
        self.setWindowTitle("Juego")
        self.stack = stack
        self.turno = "jugador"
        self.longitud = longitud
        self.nivel = nivel
        self.nombre_guardado = nombre_guardado
        
        self.matriz_datos = [[0 for _ in range(longitud)] for _ in range(longitud)]
        self.virus_activos = []  # Para nivel 2: lista con posiciones de virus
        self.mover_virus_uno = False  # Flag para mover solo uno (nivel 2)
        

        self.actualizar_virus_activos()
        self.matriz_botones = []

        # Crear layout general
        self.layout_general = QVBoxLayout()

        # Texto nivel
        self.label_nivel = QLabel(f"Nivel {nivel}")
        self.label_nivel.setStyleSheet("font-size: 18px;")
        self.label_turno = QLabel("Turno: Jugador")
        self.label_turno.setStyleSheet("font-size: 18px;")

        self.boton_salir = QPushButton("Salir")
        self.boton_salir.clicked.connect(self.salir_del_juego)

        layout_superior = QHBoxLayout()
        layout_superior.addWidget(self.label_nivel)
        layout_superior.addWidget(self.label_turno)
        layout_superior.addWidget(self.boton_salir)
        self.layout_general.addLayout(layout_superior)

        # Crear grilla
        self.grid = QGridLayout()
        for y in range(longitud):
            fila = []
            for x in range(longitud):
                boton = QPushButton(" ")
                boton.setFixedSize(40, 40)
                boton.setStyleSheet("font-size: 24px;")
                boton.clicked.connect(lambda _, px=x, py=y: self.colocar_muro(px, py))
                self.grid.addWidget(boton, y, x)
                fila.append(boton)
            self.matriz_botones.append(fila)

        self.layout_general.addLayout(self.grid)
        self.setLayout(self.layout_general)

        # Agregar virus inicial
        agregar_virus(self.matriz_datos, nivel=nivel)
        self.actualizar_tablero()

    def colocar_muro(self, x, y):
        if self.turno == "jugador" and self.matriz_datos[y][x] == 0:
            self.matriz_datos[y][x] = 2
            self.turno = "virus"
            self.label_turno.setText("Turno: Virus")
            self.actualizar_tablero()
            QTimer.singleShot(500, self.turno_virus)

    def actualizar_virus_activos(self):
        # Actualiza la lista de posiciones donde hay virus (valor 2)
        self.virus_activos = [(f, c) for f in range(self.longitud) for c in range(self.longitud) if self.matriz_datos[f][c] == 2]

    def turno_virus(self):
        if self.nivel == 1:
            virus_expandido = self.avanzar_virus_y_detectar()
            if not virus_expandido:
                self.label_turno.setText("Jugador ganador!")
                self.turno = "fin"
                QTimer.singleShot(1000, self.pasar_nivel2)
                return

        elif self.nivel == 2:
            virus_expandido = self.avanzar_virus_nivel2()
            if not virus_expandido:
                self.label_turno.setText("Jugador ganador!")
                self.turno = "fin"
                QTimer.singleShot(1000, self.pasar_nivel3)
                return

        elif self.nivel == 3:
            # Nivel 3: ...
            if not self.virus_activos:
                self.label_turno.setText("Jugador ganador!")
                self.turno = "fin"
                QTimer.singleShot(1000, self.mostrar_pantalla_ganador)
                return
            virus_expandido = self.avanzar_virus_nivel2()
            if not virus_expandido:
                self.label_turno.setText("Jugador ganador!")
                self.turno = "fin"
                QTimer.singleShot(1000, self.mostrar_pantalla_ganador)
                return
        

        self.turno = "jugador"
        self.label_turno.setText("Turno: Jugador")
        self.actualizar_tablero()

    def actualizar_tablero(self):
        for y in range(self.longitud):
            for x in range(self.longitud):
                valor = self.matriz_datos[y][x]
                if valor == 0:
                    self.matriz_botones[y][x].setText(" ")
                elif valor == 2:
                    self.matriz_botones[y][x].setText("🧱")
                elif valor == 1:
                    self.matriz_botones[y][x].setText("🦠")
    
    def avanzar_virus_y_detectar(self):
        """
        Avanza el virus (igual que antes) pero devuelve True si avanzó, False si no pudo.
        """
        filas = len(self.matriz_datos)
        columnas = len(self.matriz_datos[0])
        virus_activados = [(f, c) for f in range(filas) for c in range(columnas) if self.matriz_datos[f][c] == 1]

        for f, c in virus_activados:
            vecinos = obtener_vecinos_validos(self.matriz_datos, f, c)
            if vecinos:
                nf, nc = r.choice(vecinos)
                self.matriz_datos[nf][nc] = 1
                self.actualizar_virus_activos()
                return True  # virus pudo expandirse
        return False  # no pudo expandirse ningún virus
    
    def avanzar_virus_nivel2(self):
        """
        En nivel 2 hay 2 virus, se mueve sólo uno por turno:
        selecciona aleatoriamente uno de los virus activos que pueda expandirse y lo mueve.
        """
        virus_posibles = []
        for (f, c) in self.virus_activos:
            vecinos = obtener_vecinos_validos(self.matriz_datos, f, c)
            if vecinos:
                virus_posibles.append((f, c))
    
        if not virus_posibles:
            return False  # ninguno puede expandirse
    
        # Seleccionamos uno al azar que puede avanzar
        f, c = r.choice(virus_posibles)
        vecinos = obtener_vecinos_validos(self.matriz_datos, f, c)
        nf, nc = r.choice(vecinos)
        self.matriz_datos[nf][nc] = 1  # CAMBIAR DE 2 A 3 AQUÍ
        self.actualizar_virus_activos()
        return True
    
    def pasar_nivel2(self):
        # Resetea matriz y prepara nivel 2 con 2 virus iniciales
        self.nivel = 2
        self.label_nivel.setText(f"Nivel {self.nivel}")
        self.matriz_datos = [[0 for _ in range(self.longitud)] for _ in range(self.longitud)]
        agregar_virus(self.matriz_datos, cantidad=2, nivel=2)
        self.actualizar_virus_activos()
        self.turno = "jugador"
        self.label_turno.setText("Turno: Jugador")
        self.actualizar_tablero()
    
    def pasar_nivel3(self):
        self.nivel = 3
        self.label_nivel.setText(f"Nivel {self.nivel}")
        self.matriz_datos = [[0 for _ in range(self.longitud)] for _ in range(self.longitud)]
        agregar_virus(self.matriz_datos, cantidad=2, nivel=3)  # Ajusta según virus que quieras poner en nivel 3
        self.actualizar_virus_activos()
        self.turno = "jugador"
        self.label_turno.setText("Turno: Jugador")
        self.actualizar_tablero()
    
    def salir_del_juego(self):
        try:
            matriz_actual = self.matriz_datos  # Ya tienes la matriz en self.matriz_datos
            nivel_actual = self.nivel           # Ya tienes el nivel en self.nivel
            longitud_actual = self.longitud

            guardar_partida(self.nombre_guardado, nivel_actual, longitud_actual, matriz_actual)
            print(f"Partida guardada en {self.nombre_guardado}.bin correctamente.")
        except Exception as e:
            print(f"Error al guardar la partida: {e}")

        # Volver a pantalla_saves (índice 1 asumiendo que ahí está)
        QApplication.quit()


    def mostrar_pantalla_ganador(self):
        ganador = pantallaGanador(self.stack)
        self.stack.addWidget(ganador)
        self.stack.setCurrentWidget(ganador)

class pantallaGanador(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.setWindowTitle("¡Ganador!")

        layout = QVBoxLayout()

        label = QLabel("Ganador del juego, gracias por jugar!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 24px; font-weight: bold;")

        boton_volver = QPushButton("Volver al inicio")
        boton_volver.setFixedSize(200, 50)
        boton_volver.clicked.connect(self.volver_inicio)

        layout.addWidget(label)
        layout.addWidget(boton_volver, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def volver_inicio(self):
        self.stack.setCurrentIndex(0)
        # Opcional: eliminar esta pantalla para liberar memoria si se vuelve a jugar
        self.stack.removeWidget(self)
        self.deleteLater()

class pantalla_inicio(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Título
        titulo = QLabel("🧬 Virus Spread Game")
        titulo.setStyleSheet("font-size: 40px; font-weight: bold;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Campo para nombre del guardado
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre de la partida...")
        self.input_nombre.setFixedWidth(300)

        # Botón nueva partida
        boton_nueva = QPushButton("Nueva Partida")
        boton_nueva.setFixedSize(200, 40)
        boton_nueva.clicked.connect(self.iniciar_nueva_partida)

        # Botón cargar
        boton_cargar = QPushButton("Cargar Partida")
        boton_cargar.setFixedSize(200, 40)
        boton_cargar.clicked.connect(self.cargar_partida_existente)

        # Añadir widgets al layout
        layout.addWidget(titulo)
        layout.addSpacing(30)
        layout.addWidget(self.input_nombre, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(20)
        layout.addWidget(boton_nueva, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(boton_cargar, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def iniciar_nueva_partida(self):
        nombre = self.input_nombre.text().strip()
        if not nombre:
            print("Debes ingresar un nombre para la partida.")
            return

        pantalla = pantalla_juego(longitud=6, nivel=1, stack=self.stack, nombre_guardado=nombre)
        self.stack.addWidget(pantalla)
        self.stack.setCurrentWidget(pantalla)

    def cargar_partida_existente(self):
        nombre = self.input_nombre.text().strip()
        if not nombre:
            print("Debes ingresar un nombre de partida guardada.")
            return
        try:
            matriz, nivel = cargar_partida(nombre)
            pantalla = pantalla_juego(longitud=len(matriz), nivel=nivel, stack=self.stack, nombre_guardado=nombre)
            pantalla.matriz_datos = matriz
            pantalla.actualizar_virus_activos()
            pantalla.actualizar_tablero()
            self.stack.addWidget(pantalla)
            self.stack.setCurrentWidget(pantalla)
        except FileNotFoundError:
            print(f"No se encontró una partida guardada con el nombre '{nombre}'.")


class pantalla_saves(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.actualizar_ranuras()
        

    def actualizar_ranuras(self):
        # Limpiar el layout por si ya fue cargado antes
        for i in reversed(range(self.layout.count())):
            item = self.layout.itemAt(i)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)

        label_titulo = QLabel("Seleccione la Ranura de Guardado")
        label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_titulo.setStyleSheet("font-size: 24px;")
        self.layout.addWidget(label_titulo)

        for i in range(1, 4):
            ranura = f"ranura{i}"
            grupo_ranura = QVBoxLayout()
            datos = None
            try:
                datos = cargar_partida(ranura)
                # Forzar la actualización de la UI
                QApplication.processEvents()  
            except Exception as e:
                print(f"Error cargando partida: {e}")  # Depuración

            label_ranura = QLabel(f"RANURA {i}")
            label_ranura.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label_ranura.setStyleSheet("font-size: 18px; font-weight: bold;")

            if datos:
                nivel = datos["nivel"]
                longitud = len(datos["matriz"])  # Nueva línea para obtener tamaño
                progreso = f"Nivel {nivel} - Tamaño: {longitud}x{longitud}"
            else:
                progreso = "Sin partida guardada"

            label_progreso = QLabel(progreso)
            label_progreso.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label_progreso.setStyleSheet("font-size: 16px;")

            grupo_ranura.addWidget(label_ranura)
            grupo_ranura.addWidget(label_progreso)

            if datos:
                btn_continuar = QPushButton("Continuar partida")
                btn_continuar.clicked.connect(lambda _, r=ranura, d=datos: self.continuar_partida(r, d))
                grupo_ranura.addWidget(btn_continuar)

            btn_nueva = QPushButton("Comenzar nueva partida")
            btn_nueva.clicked.connect(lambda _, r=ranura: self.nueva_partida(r))
            grupo_ranura.addWidget(btn_nueva)

            contenedor = QWidget()
            contenedor.setLayout(grupo_ranura)
            contenedor.setStyleSheet("border: 2px solid black; padding: 10px; margin: 10px;")
            self.layout.addWidget(contenedor)

        boton_retroceder = QPushButton("Volver atrás")
        boton_retroceder.setFixedSize(120, 50)
        boton_retroceder.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.layout.addWidget(boton_retroceder, alignment=Qt.AlignmentFlag.AlignCenter)
    
    def continuar_partida(self, ranura, datos):
        longitud = len(datos["matriz"])
        nivel = datos["nivel"]
        juego = pantalla_juego(longitud=longitud, nivel=nivel, stack=self.stack, nombre_guardado=ranura)
        juego.matriz_datos = datos["matriz"]
        juego.actualizar_virus_activos()
        juego.actualizar_tablero()
        

        if self.stack.count() > 4:
            viejo = self.stack.widget(4)
            self.stack.removeWidget(viejo)
            viejo.deleteLater()

        self.stack.addWidget(juego)
        self.stack.setCurrentWidget(juego)

    def nueva_partida(self, ranura):
        # Obtener la instancia existente de pantalla_longitud
        if os.path.exists(ranura+".bin"):
            os.remove(ranura+".bin")
            print(f"Archivo '{ranura+".bin"}' eliminado correctamente.")
        pantalla_longitud_instance = self.stack.widget(3)  # Índice correcto
        pantalla_longitud_instance.ranura = ranura
        self.stack.setCurrentIndex(2)  

class pantalla_modo(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.setFixedSize(800, 600)

        layout = QVBoxLayout()

        # Espaciador superior para centrar verticalmente
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
)

        # Título
        label_titulo = QLabel("Seleccione el modo de juego")
        label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_titulo.setStyleSheet("font-size: 24px;")
        layout.addWidget(label_titulo, alignment=Qt.AlignmentFlag.AlignCenter)

        # Botón modo 1
        boton_modo1 = QPushButton("Jugador VS CPU")
        boton_modo1.setFixedSize(200, 100)
        boton_modo1.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        boton_modo1.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                border: 2px solid black;
                border-radius: 10px;
            }
            QPushButton:hover {
                border: 2px solid blue;
            }
        """)
        layout.addWidget(boton_modo1, alignment=Qt.AlignmentFlag.AlignCenter)

        # Botón modo 2
        boton_modo2 = QPushButton("Jugador VS Jugador")
        boton_modo2.setFixedSize(200, 100)
        boton_modo2.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        boton_modo2.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                border: 2px solid black;
                border-radius: 10px;
            }
            QPushButton:hover {
                border: 2px solid blue;
            }
        """)
        layout.addWidget(boton_modo2, alignment=Qt.AlignmentFlag.AlignCenter)

        # Espaciador intermedio
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Botón volver abajo del todo
        boton_retroceder = QPushButton("Volver atrás")
        boton_retroceder.setFixedSize(120, 50)
        boton_retroceder.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        boton_retroceder.setStyleSheet("""
            QPushButton {
                font-size: 12px;
                border: 2px solid black;
                border-radius: 10px;
            }
            QPushButton:hover {
                border: 2px solid blue;
            }
        """)
        layout.addWidget(boton_retroceder, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

class pantalla_longitud(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.ranura = None
        layout = QVBoxLayout()
        label_titulo = QLabel("Seleccione la longitud del mapa")
        label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_titulo.setStyleSheet("font-size: 24px;")

        # Botón para volver atrás
        boton_retroceder = QPushButton("Volver atrás")
        boton_retroceder.setFixedSize(100, 100)
        boton_retroceder.setStyleSheet("font-size: 16px; border-radius: 10px;")
        boton_retroceder.clicked.connect(lambda: self.stack.setCurrentIndex(3))

        self.label = QLabel("Escribe la longitud del mapa:")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.caja_texto_longitud = QLineEdit()
        self.caja_texto_longitud.setPlaceholderText("Ejemplo: 8 ")  # Texto gris inicial
        self.caja_texto_longitud.setMaxLength(2)  # Límite de caracteres
        self.caja_texto_longitud.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.boton_empezar = QPushButton("Empezar")
        self.boton_empezar.clicked.connect(self.mostrar_nombre)

        layout.addWidget(label_titulo, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(boton_retroceder, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        layout.addWidget(self.caja_texto_longitud)
        layout.addWidget(self.boton_empezar)
        espaciador = QSpacerItem(30, 200, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addSpacerItem(espaciador)
        self.setLayout(layout)

    def mostrar_nombre(self):
        texto = self.caja_texto_longitud.text()
        try:
            longitud = int(texto)
            if longitud <= 3 or longitud > 20:
                self.label.setText("Introduce un número entre 4 y 20.")
                return
        except ValueError:
            self.label.setText("Por favor, escribe un número válido.")
            return

        # Elimina el widget anterior del juego si existe (evitar duplicados)
        if self.stack.count() > 4:
            widget_anterior = self.stack.widget(4)
            self.stack.removeWidget(widget_anterior)
            widget_anterior.deleteLater()

        # Crear nueva pantalla de juego con longitud personalizada
        juego = pantalla_juego(
            longitud=longitud, 
            nivel=1, 
            stack=self.stack, 
            nombre_guardado=self.ranura  # Usar la ranura almacenada
        )
        self.stack.addWidget(juego)
        self.stack.setCurrentWidget(juego)

    

app = QApplication(sys.argv)
stack = QStackedWidget()

widget_inicio = pantalla_inicio(stack)
widget_ranuras = pantalla_saves(stack)
widget_modo = pantalla_modo(stack)
widget_longitud = pantalla_longitud(stack)

stack.addWidget(widget_inicio)  # índice 0
stack.addWidget(widget_ranuras)  # índice 1
stack.addWidget(widget_modo)  # índice 2
stack.addWidget(widget_longitud)  # índice 3

stack.setCurrentIndex(0)  # Pantalla inicial
stack.show()
sys.exit(app.exec())

