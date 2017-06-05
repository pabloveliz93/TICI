import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSignal
from SVParametros import *
from SVInterpretacion import *
from SerialSetup import *
# La ventana principal de la interfaz gráfica
class Ventana(QMainWindow):
    def __init__(self, mainThread):
        super().__init__()
        self.mainThread = mainThread
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Interfaz de Análisis de Datos')

        self.Graf = Grafica(self.mainThread)
        self.setCentralWidget(self.Graf)

        self.statusBar()
        self.menu_bar_init()

        # Puedo jugar después a esto gdi
#        self.setAutoFillBackground(True)
#        a = self.palette()
#        a.setColor(self.backgroundRole(), QColor(255, 200, 170))
#        self.setPalette(a)

        self.setGeometry(300, 300, 300, 300)
        self.show()

    def menu_bar_init(self):
        exitAction = QAction(QIcon('exit24.png'), 'Salir', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Cierra la aplicación')
        exitAction.triggered.connect(self.close)
        serialSetup = QAction(QIcon('exit24.png'), 'Configurar conexión...', self)
        serialSetup.setShortcut('Ctrl+S')
        serialSetup.setStatusTip('Configura la conexión del dispositivo con este software.')
        serialSetup.triggered.connect(self.Graf.popup_serialsetup)
        menubar = self.menuBar()

        # definir menús
        menuArchivo = menubar.addMenu('&Archivo')
        menuArchivo.addAction(exitAction)
        menuArchivo.addAction(serialSetup)
        menuEdicion = menubar.addMenu('&Edición')
        menuGrafico = menubar.addMenu('&Gráfico')
        menuVentana = menubar.addMenu('&Ventana')
#        par = menubar.addMenu('&Parámetros')
#        lim = menubar.addMenu('&Límites')
        ayuda = menubar.addMenu('&Ayuda')

        # definir acciones
#        volshape = QAction(QIcon('exit.png'), '&Forma del contenedor...', self)
#        volshape.setStatusTip('Permite seleccionar la forma del contenedor que se está controlando.')
#        volcalib = QAction(QIcon('exit.png'), '&Calibrar volumen...', self)
#        volcalib.setStatusTip('Permite calibrar la toma de muestras de volumen.')
#        vollim = QAction(QIcon('exit.png'), '&Establecer limites de volumen...', self)
#        vollim.setStatusTip('Establece límites para alertar en tales situaciones.')
#        templim = QAction(QIcon('exit.png'), '&Establecer limites de temperatura...', self)
#        templim.setStatusTip('Establece límites para alertar en tales situaciones.')
        acercaDe = QAction(QIcon('exit.png'), '&Acerca de...', self)
        acercaDe.setStatusTip('Créditos.')

        # asignar acciones a menús.
#        par.addAction(volshape)
#        par.addAction(volcalib)
#        lim.addAction(vollim)
#        lim.addAction(templim)
        ayuda.addAction(acercaDe)


# Marco de la ventana principal
class Grafica(QWidget):
    alertSignal = pyqtSignal(str, str, QThread)
    def __init__(self, mainThread):
        super().__init__()
        self.mainThread = mainThread
        self.initUI()
        self.popup_serialsetup()

    def datos_rapidos(self):
        w = QWidget()
        grid = QGridLayout()
        w.setLayout(grid)
        self.volumeLabel = self.add_labels_to_grid(grid, 0, 0, "Porcentaje volumétrico:", "%")
        self.tempLabel = self.add_labels_to_grid(grid, 0, 1, "Temperatura:", "°C")
        self.fluxLabel = self.add_labels_to_grid(grid, 0, 2, "Flujo actual:", "cm3 / s")
        return w

    def add_labels_to_grid(self, grid, row, column, text, datatypetext):
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        textlabel = QLabel(text)
        textlabel.setFont(QFont("Arial", 8))
        hbox.addWidget(textlabel)
        temp = QLabel("0")
        temp.setFont(QFont("Arial", 8, QFont.Bold))
        hbox.addStretch(0)
        hbox.addWidget(temp)
        datatype = QLabel(datatypetext)
        datatype.setFont(QFont("Arial", 8, QFont.Bold))
        hbox.addStretch(0)
        hbox.addWidget(datatype)
        hbox.addStretch(1)
        grid.addLayout(hbox, row, column)
        return temp

    def initUI(self):
        self.alertSignal.connect(self.alert) #Conecta nuestra señal de alerta
        self.definido = False  # no se si sea apropiado ponerlo acá...

        # Cuadrícula general del Frame
        mprincipal = QVBoxLayout()
        mprincipal.addStretch(0)

        # Grid de datos rápidos
        datos = self.datos_rapidos()
        mprincipal.addWidget(datos)
        mprincipal.addStretch(0)

        # Corrida de botones de acción
        mbotones = QHBoxLayout()
        mbotones.addStretch(2)

        # Columna de botones de control de flujo
        mflujo = QVBoxLayout()  # m_nombre es el menu
        nflujo = ['Iniciar', 'Detener', 'Reiniciar']  # n_nombre son los nombres de los botones
        self.bflujo = []  # b_nombre arreglo de acceso a cada botón
        mflujo.addStretch(1)
        for flujo in nflujo:
            aux = QPushButton(flujo)    # Hacer el botón
            mflujo.addWidget(aux)       # Agregarlo a la cuadrícula
            self.bflujo.append(aux)          # Arreglo de acceso
            mflujo.addStretch(0)
        self.bflujo[0].clicked.connect(self.mainThread.resume)
        self.bflujo[1].clicked.connect(self.mainThread.pause)
        mflujo.addStretch(1)

        mbotones.addLayout(mflujo)
        mbotones.addStretch(2)
        nbotones = ['Fijar\nParámetros', 'Monitorear\nMediciones', 'Ver Historial\nde Mediciones', 'Panel de \nAlertas']
        self.bbotones = []
        for boton in nbotones:
            aux = QPushButton(boton)    # Hacer el botón
            mbotones.addWidget(aux)     # Agregarlo a la cuadrícula
            mbotones.addStretch(1)
            self.bbotones.append(aux)        # Arreglo de acceso
        mbotones.addStretch(1)

        for i in range(0,4) :
            self.bbotones[i].setCheckable(True)

        #Conectar el slot para mostrar SVPARAMETROS al botón
        self.bbotones[0].clicked.connect(self.mostrar_svparametros)
        self.bbotones[1].clicked.connect(self.mostrar_svinterpretacion)
#        bbotones[2].clicked.connect(self.mostrar_svhistorial)
#        bbotones[3].clicked.connect(self.mostrar_svalertas)

        mprincipal.addLayout(mbotones)
        mprincipal.addStretch(1)

        self.setLayout(mprincipal)

        #Crear subventanas
        self.sv = SVParametros(self.mainThread)
        self.svi = SVInterpretacion()
        self.ss = SSWidget()
        self.ss.connectbutton.clicked.connect(self.actualizar_puerto)
        self.ss.connectbutton.clicked.connect(self.all_buttons_enable)
        #¿Servirá?
        mprincipal.addWidget(self.sv)
        self.sv.hide()
        mprincipal.addWidget(self.svi)
        self.svi.hide()
    def actualizar_puerto(self):
        self.mainThread.set_port(self.ss.port)
        self.mainThread.serial_connect()
    def control_buttons_enable(self, enabled):
        for button in self.bflujo:
            button.setEnabled(enabled)
    def main_buttons_enable(self, enabled):
        for button in self.bbotones:
            button.setEnabled(enabled)
    def all_buttons_enable(self):
        if self.ss.port != "":
            for button in self.bflujo:
                button.setEnabled(True)
        for button in self.bbotones:
            button.setEnabled(True)
    #Slot para mostrar svparametros
    def mostrar_svparametros(self, pressed):
        if pressed:
            self.sv.show()
            if self.ss.port != "":
                self.control_buttons_enable(False)
            self.mainThread.pause()
        else:
            self.sv.hide()
            self.control_buttons_enable(True)

    def mostrar_svinterpretacion(self, pressed):
        if pressed:
            self.svi.show()
        else:
            self.svi.hide()
    def popup_serialsetup(self):
        self.control_buttons_enable(False)
        self.main_buttons_enable(False)
        self.mainThread.pause()
        self.ss.show()
    #Tengo que declarar el método de alerta aquí, porque no se puede en el thread
    def alert(self, wd_title, text, thread):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(text)
        msg.setWindowTitle(wd_title)
        msg.setStandardButtons(QMessageBox.Ok)
        #msg.buttonClicked.connect(thread.resume)
        msg.addButton(QPushButton("Ver gráfico..."), QMessageBox.AcceptRole)
        msg.exec_()