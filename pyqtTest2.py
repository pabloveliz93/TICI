import sys
import auxlib
from time import sleep
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QThread, pyqtSignal

#Thread para conectar el software principal con nuestra interfaz gráfica
class Thread(QThread):
	def __init__(self):
		super().__init__()
		self.p = auxlib.Principal()
	def set_main_window(self, w):
		self.m = w
	def set_vol_label(self, label):
		self.vollabel = label
	def set_temp_label(self, label):
		self.templabel = label
	def set_flux_label(self, label):
		self.fluxlabel = label
	def run(self):
		while True:
			self.p.principal_loop()
			self.vollabel.setText(str(self.p.vol))
			self.templabel.setText(str(self.p.temp))
			self.fluxlabel.setText(str(self.p.flux))

#Clase de la ventana principal de la interfaz gráfica
class VentanaPrincipal(QWidget):
	def __init__(self):
		super().__init__()
		self.window_fast_init(300, 300, 640, 480, "PyQt")
		#self.menu_bar_init()
		grid = QGridLayout()
		self.setLayout(grid)
		self.volumeLabel = self.add_labels_to_grid(grid, 0, 0, "Porcentaje volumétrico:", "%")
		self.tempLabel = self.add_labels_to_grid(grid, 0, 1, "Temperatura:", "°C")
		self.fluxLabel = self.add_labels_to_grid(grid, 1, 0, "Flujo actual:", "cm3 / s")
		self.show()
	def window_fast_init(self, x, y, width, height, name):
		self.setGeometry(x, y, width, height)
		self.setWindowTitle(name)
	def menu_bar_init(self):
		#exitAction.setShortcut('Ctrl+Q')
		#exitAction.triggered.connect(qApp.quit)
		self.statusBar()
		menubar = self.menuBar()
		par = menubar.addMenu('&Parámetros')
		lim = menubar.addMenu('&Límites')
		ayuda = menubar.addMenu('&Ayuda')
		volshape = QAction(QIcon('exit.png'), '&Forma del contenedor...', self)
		volshape.setStatusTip('Permite seleccionar la forma del contenedor que se está controlando.')
		volcalib = QAction(QIcon('exit.png'), '&Calibrar volumen...', self)
		volcalib.setStatusTip('Permite calibrar la toma de muestras de volumen.')
		vollim = QAction(QIcon('exit.png'), '&Establecer limites de volumen...', self)
		vollim.setStatusTip('Establece límites para alertar en tales situaciones.')
		templim = QAction(QIcon('exit.png'), '&Establecer limites de temperatura...', self)
		templim.setStatusTip('Establece límites para alertar en tales situaciones.')
		acercaDe = QAction(QIcon('exit.png'), '&Acerca de...', self)
		par.addAction(volshape)
		par.addAction(volcalib)
		lim.addAction(vollim)
		lim.addAction(templim)
		ayuda.addAction(acercaDe)
	def add_labels_to_grid(self, grid, row, column, text, datatypetext):
		vbox = QVBoxLayout()
		textlabel = QLabel(text)
		textlabel.setFont(QFont( "Arial", 16))
		vbox.addWidget(textlabel)
		temp = QLabel("0")
		temp.setFont(QFont( "Arial", 48, QFont.Bold))
		hbox = QHBoxLayout()
		hbox.addStretch(0)
		hbox.addWidget(temp)
		datatype = QLabel(datatypetext)
		datatype.setFont(QFont( "Arial", 48, QFont.Bold))
		hbox.addWidget(datatype)
		vbox.addLayout(hbox)
		grid.addLayout(vbox, row, column)
		return temp

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = VentanaPrincipal()
	thr = Thread()
	thr.set_main_window(ex)
	thr.set_vol_label(ex.volumeLabel)
	thr.set_temp_label(ex.tempLabel)
	thr.set_flux_label(ex.fluxLabel)
	thr.start()
	sys.exit(app.exec_())