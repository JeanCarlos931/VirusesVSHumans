from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,
    QGridLayout, QStackedWidget, QHBoxLayout
)
from PyQt6.QtCore import Qt
import sys

class PantallaJuego(QWidget):
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

class PantallaInicio(QWidget):
    def __init__(self, stack):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("🧬 Virus Spread Game")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 24px;")
        boton = QPushButton("JUGAR")
        boton.clicked.connect(lambda: stack.setCurrentIndex(1))  # Cambiar a la siguiente pantalla
        layout.addWidget(label)
        layout.addWidget(boton)
        self.setLayout(layout)

app = QApplication(sys.argv)
stack = QStackedWidget()

pantalla_inicio = PantallaInicio(stack)
pantalla_juego = PantallaJuego()

stack.addWidget(pantalla_inicio)  # índice 0
stack.addWidget(pantalla_juego)  # índice 1

stack.setCurrentIndex(0)  # Pantalla inicial
stack.show()
sys.exit(app.exec())

