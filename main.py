from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,
    QGridLayout, QStackedWidget, QHBoxLayout, QSpacerItem, QSizePolicy, 
    QLineEdit, 
)
from PyQt6.QtCore import Qt
import sys

class pantalla_juego(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Juego")
        self.matriz_botones = []
        layout = QGridLayout()
        for y in range(10):
            fila = []
            for x in range(15):
                boton = QPushButton("🧱")
                boton.setFixedSize(50, 50)
                boton.setStyleSheet("font-size: 40px;")
                boton.clicked.connect(lambda _, px=x, py=y: self.saludar(px, py))
                layout.addWidget(boton, y, x)
                fila.append(boton)
            self.matriz_botones.append(fila)
        self.setLayout(layout)

    def saludar(self, x, y):
        print(f"X:{x} Y:{y}")
        self.matriz_botones[y][x].setText("🦠")

class pantalla_inicio(QWidget):
    def __init__(self, stack):
        super().__init__()

        layout = QVBoxLayout()

        # Título del juego
        label_titulo = QLabel("🧬 Virus Spread Game")
        label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_titulo.setStyleSheet("font-size: 40px;")

        # Botón cuadrado
        boton_jugar = QPushButton("JUGAR")
        boton_jugar.setFixedSize(200, 100)  # Cuadrado
        boton_jugar.setStyleSheet("""
            QPushButton {
                font-size: 30px;
                border: 2px solid black;
                border-radius: 10px;
            }
            QPushButton:hover {
                border: 2px solid blue;
            }
        """)
        boton_jugar.clicked.connect(lambda: stack.setCurrentIndex(1))

        layout.addWidget(label_titulo, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(boton_jugar, alignment=Qt.AlignmentFlag.AlignCenter)

        # Espaciador para subir todo hacia arriba
        espaciador = QSpacerItem(20, 200, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addSpacerItem(espaciador)

        self.setLayout(layout)

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
        boton_retroceder.setFixedSize(100, 100)
        boton_retroceder.setStyleSheet("font-size: 16px; border-radius: 10px;")
        boton_retroceder.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        # Ranuras
        boton_saves1 = QPushButton("RANURA 1")
        boton_saves1.setFixedSize(100, 100)
        boton_saves1.setStyleSheet("font-size: 16px; border-radius: 10px;")
        boton_saves1.clicked.connect(lambda: self.stack.setCurrentIndex(2))

        boton_saves2 = QPushButton("RANURA 2")
        boton_saves2.setFixedSize(100, 100)
        boton_saves2.setStyleSheet("font-size: 16px; border-radius: 10px;")
        boton_saves2.clicked.connect(lambda: self.stack.setCurrentIndex(2))

        boton_saves3 = QPushButton("RANURA 3")
        boton_saves3.setFixedSize(100, 100)
        boton_saves3.setStyleSheet("font-size: 16px; border-radius: 10px;")
        boton_saves3.clicked.connect(lambda: self.stack.setCurrentIndex(2))

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

        layout = QVBoxLayout()
        label_titulo = QLabel("Seleccione el modo de juego")
        label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_titulo.setStyleSheet("font-size: 24px;")
 
        # Botón para volver atrás
        boton_retroceder = QPushButton("Volver atrás")
        boton_retroceder.setFixedSize(100, 200)
        boton_retroceder.setStyleSheet("font-size: 16px; border-radius: 10px;")
        boton_retroceder.clicked.connect(lambda: self.stack.setCurrentIndex(2))

        # Ranuras
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
        

        layout.addWidget(label_titulo, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(boton_modo1, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(boton_modo2, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(boton_retroceder, alignment=Qt.AlignmentFlag.AlignCenter)
      

        espaciador = QSpacerItem(30, 200, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addSpacerItem(espaciador)

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

        self.label = QLabel("Escribe la longitud:")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.caja_texto = QLineEdit()
        self.caja_texto.setPlaceholderText("Ejemplo: 8 ")  # Texto gris inicial
        self.caja_texto.setMaxLength(2)  # Límite de caracteres
        self.caja_texto.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.boton = QPushButton("Aceptar")
        self.boton.clicked.connect(self.mostrar_nombre)

        layout.addWidget(label_titulo, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(boton_retroceder, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        layout.addWidget(self.caja_texto)
        layout.addWidget(self.boton)
        espaciador = QSpacerItem(30, 200, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addSpacerItem(espaciador)
        self.setLayout(layout)

    def mostrar_nombre(self):
        nombre = self.caja_texto.text()
        self.label.setText(f"Hola, {nombre}!")  # Reemplaza el texto de la etiqueta

app = QApplication(sys.argv)
stack = QStackedWidget()

widget_inicio = pantalla_inicio(stack)
widget_ranuras = pantalla_saves(stack)
widget_modo = pantalla_modo(stack)
widget_longitud = pantalla_longitud(stack)
widget_juego = pantalla_juego()

stack.addWidget(widget_inicio)  # índice 0
stack.addWidget(widget_ranuras)  # índice 1
stack.addWidget(widget_modo)  # índice 2
stack.addWidget(widget_longitud)  # índice 3
stack.addWidget(widget_juego)  # índice 4

stack.setCurrentIndex(0)  # Pantalla inicial
stack.show()
sys.exit(app.exec())

