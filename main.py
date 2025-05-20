from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,
    QGridLayout, QStackedWidget, QHBoxLayout, QSpacerItem, QSizePolicy, 
    QLineEdit, 
)
from PyQt6.QtCore import Qt
import time
import sys

class pantalla_juego(QWidget):
    def __init__(self, longitud, nivel=1, stack=None):
        super().__init__()
        self.setWindowTitle("Juego")
        self.matriz_botones = []
        self.turno_actual = "Jugador"
        self.stack = stack  # Para poder regresar al menú si se usa

        # --- Layout principal vertical ---
        layout_principal = QVBoxLayout()

        # Texto del nivel
        self.label_nivel = QLabel(f"🌟 Nivel: {nivel}")
        self.label_nivel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_nivel.setStyleSheet("font-size: 20px;")
        layout_principal.addWidget(self.label_nivel)

        # Texto del turno
        self.label_turno = QLabel(f"Turno: {self.turno_actual}")
        self.label_turno.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_turno.setStyleSheet("font-size: 18px;")
        layout_principal.addWidget(self.label_turno)

        # --- Tablero ---
        layout_tablero = QGridLayout()

        for y in range(longitud):
            fila = []
            for x in range(longitud):
                boton = QPushButton("🧱")
                boton.setFixedSize(50, 50)
                boton.setStyleSheet("font-size: 40px;")
                boton.clicked.connect(lambda _, px=x, py=y: self.saludar(px, py))
                layout_tablero.addWidget(boton, y, x)
                fila.append(boton)
            self.matriz_botones.append(fila)

        for col in range(longitud):
            layout_tablero.setColumnStretch(longitud, 1)

        contenedor_tablero = QWidget()
        contenedor_tablero.setLayout(layout_tablero)
        layout_principal.addWidget(contenedor_tablero, alignment=Qt.AlignmentFlag.AlignCenter)
        # --- Botón Salir ---
        boton_salir = QPushButton("Salir")
        boton_salir.setFixedSize(100, 40)
        boton_salir.setStyleSheet("font-size: 14px; border-radius: 8px;")
        boton_salir.clicked.connect(self.salir_del_juego)
        layout_principal.addWidget(boton_salir, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout_principal)

    def saludar(self, x, y):
        print(f"X:{x} Y:{y}")
        self.matriz_botones[y][x].setText("🦠")

        # Cambiar el turno
        self.turno_actual = "Virus" if self.turno_actual == "Jugador" else "Jugador"
        self.label_turno.setText(f"Turno: {self.turno_actual}")

    def salir_del_juego(self):
        if self.stack:
            self.stack.setCurrentIndex(0)  # Vuelve al menú principal
        else:
            self.close()  # Cierra la ventana si no hay stack


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
                self.label.setText("Introduce un número entre 1 y 20.")
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

