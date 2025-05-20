from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,
    QGridLayout, QStackedWidget, QHBoxLayout, QSpacerItem, QSizePolicy, 
    QLineEdit,
)
from PyQt6.QtCore import Qt, QTimer
from guardador import guardar_partida 
import time
import sys
from virus import agregar_virus, avanzar_virus


class pantalla_juego(QWidget):
    def __init__(self, longitud, nivel, stack):
        super().__init__()
        self.setWindowTitle("Juego")
        self.stack = stack
        self.turno = "jugador"
        self.longitud = longitud
        self.nivel = nivel
        self.matriz_datos = [[0 for _ in range(longitud)] for _ in range(longitud)]

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

    def turno_virus(self):
        avanzar_virus(self.matriz_datos)
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
                elif valor == 3:
                    self.matriz_botones[y][x].setText("🦠")

    def salir_del_juego(self):
        try:
            guardar_partida("ranura1", self.matriz_datos, self.nivel)
            print("Partida guardada correctamente.")
        except Exception as e:
            print(f"Error al guardar la partida: {e}")

        if self.stack:
            self.stack.setCurrentIndex(0)
        else:
            self.close()


class pantalla_inicio(QWidget):
    def __init__(self, stack):
        super().__init__()

        self.setFixedSize(800, 600)  # Tamaño fijo de la ventana

        # Título del juego
        self.label_titulo = QLabel("🧬 Virus Spread Game", self)
        self.label_titulo.setStyleSheet("font-size: 40px;")
        self.label_titulo.adjustSize()  # Ajusta el tamaño del QLabel al texto
        self.label_titulo.move((self.width() - self.label_titulo.width()) // 2, 50)  # Centrado horizontal, 150px vertical

        # Botón cuadrado "JUGAR"
        self.boton_jugar = QPushButton("JUGAR", self)
        self.boton_jugar.setFixedSize(200, 100)
        self.boton_jugar.setStyleSheet("""
            QPushButton {
                font-size: 30px;
                border: 2px solid black;
                border-radius: 10px;
            }
            QPushButton:hover {
                border: 2px solid blue;
            }
        """)
        self.boton_jugar.move((self.width() - 200) // 2, 300)  # Centrado horizontal, 300px vertical
        self.boton_jugar.clicked.connect(lambda: stack.setCurrentIndex(1))

class pantalla_saves(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        layout = QVBoxLayout()
        label_titulo = QLabel("Seleccione la Ranura de Guardado")
        label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_titulo.setStyleSheet("font-size: 24px;")

        # Botón para volver atrás
        boton_retroceder = QPushButton("Volver atrás")
        boton_retroceder.setFixedSize(100, 50)
        boton_retroceder.clicked.connect(lambda: self.stack.setCurrentIndex(0))
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

        # Ranuras
        boton_saves1 = QPushButton("RANURA 1")
        boton_saves1.setFixedSize(200, 60)
        boton_saves1.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        boton_saves1.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                border: 2px solid black;
                border-radius: 10px;
            }
            QPushButton:hover {
                border: 2px solid blue;
            }
        """)

        boton_saves2 = QPushButton("RANURA 2")
        boton_saves2.setFixedSize(200, 60)
        boton_saves2.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        boton_saves2.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                border: 2px solid black;
                border-radius: 10px;
            }
            QPushButton:hover {
                border: 2px solid blue;
            }
        """)

        boton_saves3 = QPushButton("RANURA 3")
        boton_saves3.setFixedSize(200, 60)
        boton_saves3.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        boton_saves3.setStyleSheet("""
            QPushButton {
                font-size: 16px; 
                border: 2px solid black;
                border-radius: 10px;
            }
            QPushButton:hover {
                border: 2px solid blue;
            }
        """)

        layout.addWidget(label_titulo, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(boton_saves1, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(boton_saves2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(boton_saves3, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(boton_retroceder, alignment=Qt.AlignmentFlag.AlignCenter)
      

        espaciador = QSpacerItem(30, 200, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addSpacerItem(espaciador)

        self.setLayout(layout)

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
        juego = pantalla_juego(longitud, nivel=1, stack=self.stack)
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

