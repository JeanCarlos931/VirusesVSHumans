from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,
    QGridLayout, QStackedWidget, QHBoxLayout, QSpacerItem, QSizePolicy, 
    QLineEdit,
)
from PyQt6.QtCore import Qt, QTimer, QPoint
from guardador import guardar_partida, cargar_partida
import sys
from virus import agregar_virus, avanzar_virus, obtener_vecinos_validos
import random as r

class pantalla_juego(QWidget):
    def __init__(self, longitud, nivel, stack, nombre_guardado, modo_juego):
        super().__init__()
        self.setWindowTitle("Juego")
        self.stack = stack
        self.longitud = longitud
        self.nivel = nivel
        self.nombre_guardado = nombre_guardado
        self.modo_juego = modo_juego  # "single" o "multi"
        
        # Configuración inicial según modo de juego
        if self.modo_juego == "multi":
            self.turno = "jugador_muro"
            self.matriz_datos = [[0 for _ in range(longitud)] for _ in range(longitud)]
            # Posición inicial del virus en multijugador
            self.matriz_datos[0][0] = 3
            self.virus_activos = [(0, 0)]
        else:
            self.turno = "jugador"
            self.matriz_datos = [[0 for _ in range(longitud)] for _ in range(longitud)]
            agregar_virus(self.matriz_datos, nivel=nivel)
            self.virus_activos = [(f, c) for f in range(longitud) for c in range(longitud) if self.matriz_datos[f][c] == 3]

        self.matriz_botones = []

        # Crear layout general
        self.layout_general = QVBoxLayout()

        # Barra superior
        layout_superior = QHBoxLayout()
        
        self.label_modo = QLabel()
        self.actualizar_etiqueta_modo()
        self.label_modo.setStyleSheet("font-size: 18px; color: #2c3e50;")
        
        self.label_turno = QLabel()
        self.actualizar_etiqueta_turno()
        self.label_turno.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        self.boton_salir = QPushButton("Salir")
        self.boton_salir.setStyleSheet("background-color: #e74c3c; color: white; padding: 8px;")
        self.boton_salir.clicked.connect(self.salir_del_juego)
        
        layout_superior.addWidget(self.label_modo)
        layout_superior.addStretch()
        layout_superior.addWidget(self.label_turno)
        layout_superior.addStretch()
        layout_superior.addWidget(self.boton_salir)
        self.layout_general.addLayout(layout_superior)

        # Crear grilla
        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        for y in range(longitud):
            fila = []
            for x in range(longitud):
                boton = QPushButton(" ")
                boton.setFixedSize(50, 50)
                boton.setStyleSheet("""
                    QPushButton {
                        font-size: 24px;
                        background-color: #ecf0f1;
                        border: 2px solid #bdc3c7;
                        border-radius: 5px;
                    }
                    QPushButton:hover {
                        background-color: #d0d3d4;
                    }
                """)
                boton.clicked.connect(self.manejar_clic)
                self.grid.addWidget(boton, y, x)
                fila.append(boton)
            self.matriz_botones.append(fila)

        self.layout_general.addLayout(self.grid)
        self.setLayout(self.layout_general)
        self.actualizar_tablero()

    def actualizar_etiqueta_modo(self):
        if self.modo_juego == "multi":
            self.label_modo.setText("Modo: Multijugador")
        else:
            self.label_modo.setText(f"Nivel: {self.nivel}")

    def actualizar_etiqueta_turno(self):
        textos = {
            "jugador": "Turno: Jugador (Colocar muros)",
            "jugador_muro": "Turno: Jugador Muros",
            "jugador_virus": "Turno: Jugador Virus",
            "virus": "Turno: Virus",
            "fin": "Juego terminado"
        }
        self.label_turno.setText(textos.get(self.turno, ""))

    def manejar_clic(self):
        boton = self.sender()
        index = self.grid.indexOf(boton)
        posicion = self.grid.getItemPosition(index)
        y, x = posicion[0], posicion[1]
        
        if self.turno == "fin":
            return

        if self.modo_juego == "multi":
            if self.turno == "jugador_muro":
                self.colocar_muro(x, y)
            elif self.turno == "jugador_virus":
                self.colocar_virus(x, y)
        else:
            if self.turno == "jugador":
                self.colocar_muro(x, y)

    def colocar_muro(self, x, y):
        if self.matriz_datos[y][x] == 0:
            self.matriz_datos[y][x] = 2
            self.actualizar_tablero()
            
            if self.modo_juego == "multi":
                if not self.hay_movimientos_virus():
                    self.fin_juego("¡Jugador Muros Gana!")
                else:
                    self.turno = "jugador_virus"
            else:
                self.turno = "virus"
                QTimer.singleShot(500, self.turno_virus)
            
            self.actualizar_etiqueta_turno()

    def colocar_virus(self, x, y):
        if self.matriz_datos[y][x] == 0:
            # Verificar adyacencia a virus existente
            vecinos = obtener_vecinos_validos(self.matriz_datos, y, x, distancia=1)
            for (f, c) in vecinos:
                if self.matriz_datos[f][c] == 3:
                    self.matriz_datos[y][x] = 3
                    self.virus_activos.append((y, x))
                    self.actualizar_tablero()
                    
                    if not self.hay_movimientos_muro():
                        self.fin_juego("¡Jugador Virus Gana!")
                    else:
                        self.turno = "jugador_muro"
                    
                    self.actualizar_etiqueta_turno()
                    return

    def hay_movimientos_muro(self):
        return any(0 in fila for fila in self.matriz_datos)

    def hay_movimientos_virus(self):
        for (f, c) in self.virus_activos:
            if any(self.matriz_datos[nf][nc] == 0 for nf, nc in obtener_vecinos_validos(self.matriz_datos, f, c)):
                return True
        return False

    def actualizar_tablero(self):
        for y in range(self.longitud):
            for x in range(self.longitud):
                valor = self.matriz_datos[y][x]
                boton = self.matriz_botones[y][x]
                if valor == 0:
                    boton.setText(" ")
                    boton.setEnabled(True)
                elif valor == 2:
                    boton.setText("🧱")
                    boton.setEnabled(False)
                elif valor == 3:
                    boton.setText("🦠")
                    boton.setEnabled(False)
                
                # Resaltar celdas disponibles para virus en multijugador
                if self.modo_juego == "multi" and self.turno == "jugador_virus":
                    if self.matriz_datos[y][x] == 0:
                        vecinos = obtener_vecinos_validos(self.matriz_datos, y, x, distancia=1)
                        if any(self.matriz_datos[f][c] == 3 for (f, c) in vecinos):
                            boton.setStyleSheet("background-color: #f9e79f;")
                        else:
                            boton.setStyleSheet("background-color: #ecf0f1;")
                    else:
                        boton.setStyleSheet("background-color: #ecf0f1;")
                else:
                    boton.setStyleSheet("background-color: #ecf0f1;")

    def turno_virus(self):
        if self.modo_juego == "single":
            if self.nivel == 1:
                virus_expandido = self.avanzar_virus_normal()
            elif self.nivel == 2:
                virus_expandido = self.avanzar_virus_nivel2()
            else:
                virus_expandido = self.avanzar_virus_nivel3()
            
            if not virus_expandido:
                self.fin_juego("¡Jugador Gana!")
                return

            self.turno = "jugador"
            self.actualizar_etiqueta_turno()
            self.actualizar_tablero()

    def avanzar_virus_normal(self):
        virus_activados = self.virus_activos.copy()
        expandido = False
        
        for f, c in virus_activados:
            vecinos = obtener_vecinos_validos(self.matriz_datos, f, c)
            if vecinos:
                nf, nc = r.choice(vecinos)
                self.matriz_datos[nf][nc] = 3
                self.virus_activos.append((nf, nc))
                expandido = True
        
        return expandido

    def avanzar_virus_nivel2(self):
        virus_posibles = [pos for pos in self.virus_activos if obtener_vecinos_validos(self.matriz_datos, pos[0], pos[1])]
        if not virus_posibles:
            return False
        
        f, c = r.choice(virus_posibles)
        vecinos = obtener_vecinos_validos(self.matriz_datos, f, c)
        nf, nc = r.choice(vecinos)
        self.matriz_datos[nf][nc] = 3
        self.virus_activos.append((nf, nc))
        return True

    def fin_juego(self, mensaje):
        self.turno = "fin"
        self.label_turno.setText(mensaje)
        self.label_turno.setStyleSheet("color: #27ae60; font-size: 24px; font-weight: bold;")
        QTimer.singleShot(3000, self.volver_al_inicio)

    def volver_al_inicio(self):
        self.stack.setCurrentIndex(0)
        self.deleteLater()

    def salir_del_juego(self):
        if self.nombre_guardado:
            try:
                guardar_partida(self.nombre_guardado, {
                    'matriz': self.matriz_datos,
                    'nivel': self.nivel,
                    'modo': self.modo_juego
                })
            except Exception as e:
                print(f"Error guardando partida: {e}")
        self.stack.setCurrentIndex(1)

    # Métodos existentes para niveles single player
    def pasar_nivel2(self):
        self.nivel = 2
        self.label_modo.setText(f"Nivel: {self.nivel}")
        self.matriz_datos = [[0 for _ in range(self.longitud)] for _ in range(self.longitud)]
        agregar_virus(self.matriz_datos, cantidad=2, nivel=2)
        self.virus_activos = [(f, c) for f in range(self.longitud) for c in range(self.longitud) if self.matriz_datos[f][c] == 3]
        self.turno = "jugador"
        self.actualizar_etiqueta_turno()
        self.actualizar_tablero()

    def pasar_nivel3(self):
        self.nivel = 3
        self.label_modo.setText(f"Nivel: {self.nivel}")
        self.matriz_datos = [[0 for _ in range(self.longitud)] for _ in range(self.longitud)]
        agregar_virus(self.matriz_datos, cantidad=3, nivel=3)
        self.virus_activos = [(f, c) for f in range(self.longitud) for c in range(self.longitud) if self.matriz_datos[f][c] == 3]
        self.turno = "jugador"
        self.actualizar_etiqueta_turno()
        self.actualizar_tablero()

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
            except:
                pass

            label_ranura = QLabel(f"RANURA {i}")
            label_ranura.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label_ranura.setStyleSheet("font-size: 18px; font-weight: bold;")

            if datos:
                nivel = datos["nivel"]
                progreso = f"Nivel {nivel}"
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
        juego.actualizar_tablero()

        if self.stack.count() > 4:
            viejo = self.stack.widget(4)
            self.stack.removeWidget(viejo)
            viejo.deleteLater()

        self.stack.addWidget(juego)
        self.stack.setCurrentWidget(juego)

    def nueva_partida(self, ranura):
        # Obtener la instancia existente de pantalla_longitud
        pantalla_longitud_instance = self.stack.widget(3)
        # Configurar la ranura en esa instancia
        pantalla_longitud_instance.ranura = ranura
        # Cambiar a la pantalla de longitud
        self.stack.setCurrentIndex(2)

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt

class pantalla_modo(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.setFixedSize(800, 600)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Espaciador superior
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Título
        label_titulo = QLabel("Seleccione el modo de juego")
        label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_titulo.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(label_titulo)

        # Botones de modo
        boton_modo_single = QPushButton("Jugador VS CPU")
        boton_modo_multi = QPushButton("Jugador VS Jugador (Multijugador)")
        
        for boton in [boton_modo_single, boton_modo_multi]:
            boton.setFixedSize(300, 80)
            boton.setStyleSheet("""
                QPushButton {
                    font-size: 18px;
                    border: 2px solid #2c3e50;
                    border-radius: 10px;
                    padding: 10px;
                    background-color: #3498db;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            layout.addWidget(boton, alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addSpacing(20)

        # Configurar acciones
        boton_modo_single.clicked.connect(lambda: self.seleccionar_modo("single"))
        boton_modo_multi.clicked.connect(lambda: self.seleccionar_modo("multi"))

        # Espaciador inferior
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Botón volver
        boton_volver = QPushButton("Volver")
        boton_volver.setFixedSize(120, 40)
        boton_volver.setStyleSheet("font-size: 14px;")
        boton_volver.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        layout.addWidget(boton_volver, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def seleccionar_modo(self, modo):
        pantalla_longitud = self.stack.widget(3)
        pantalla_longitud.modo_juego = modo
        self.stack.setCurrentIndex(3)

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt

class pantalla_longitud(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.modo_juego = "single"  # Valor por defecto
        self.ranura = None

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Título
        label_titulo = QLabel("Configuración de partida")
        label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_titulo.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(label_titulo)

        # Instrucciones
        self.label_instruccion = QLabel("Longitud del tablero (4-20):")
        self.label_instruccion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_instruccion)

        # Campo de texto
        self.input_longitud = QLineEdit()
        self.input_longitud.setPlaceholderText("Ejemplo: 8")
        self.input_longitud.setMaxLength(2)
        self.input_longitud.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input_longitud.setStyleSheet("font-size: 16px; padding: 5px;")
        self.input_longitud.setFixedWidth(100)
        layout.addWidget(self.input_longitud, alignment=Qt.AlignmentFlag.AlignCenter)

        # Botón empezar
        boton_empezar = QPushButton("Comenzar partida")
        boton_empezar.setStyleSheet("font-size: 16px; padding: 8px;")
        boton_empezar.clicked.connect(self.iniciar_juego)
        layout.addWidget(boton_empezar, alignment=Qt.AlignmentFlag.AlignCenter)

        # Espaciador
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Botón volver
        boton_volver = QPushButton("Volver")
        boton_volver.setFixedSize(100, 40)
        boton_volver.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        layout.addWidget(boton_volver, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def iniciar_juego(self):
        try:
            longitud = int(self.input_longitud.text())
            if not 4 <= longitud <= 20:
                raise ValueError
        except ValueError:
            self.label_instruccion.setText("¡Longitud inválida! Debe ser entre 4 y 20")
            self.label_instruccion.setStyleSheet("color: red;")
            return

        # Limpiar partidas anteriores en la misma posición de stack
        while self.stack.count() > 4:
            old_widget = self.stack.widget(4)
            self.stack.removeWidget(old_widget)
            old_widget.deleteLater()

        nueva_partida = pantalla_juego(
            longitud=longitud,
            nivel=1,
            stack=self.stack,
            nombre_guardado=self.ranura,
            modo_juego=self.modo_juego
        )
        
        self.stack.addWidget(nueva_partida)
        self.stack.setCurrentIndex(4)

    

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

