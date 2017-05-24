import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QThread, pyqtSignal

class VentanaPrincipal(QWidget):
	def __init__(self):
		super().__init__()
		self.window_fast_init(300, 300, 640, 480, "PyQt")
		grid = QGridLayout()
		self.setLayout(grid)
		volumeLabel = self.add_labels_to_grid(grid, 0, 0, "Porcentaje volumétrico:", "%")
		tempLabel = self.add_labels_to_grid(grid, 0, 1, "Temperatura:", "°C")
		fluxLabel = self.add_labels_to_grid(grid, 1, 0, "Flujo actual:", "cm3 / s")
		self.show()
	def window_fast_init(self, x, y, width, height, name):
		self.setGeometry(x, y, width, height)
		self.setWindowTitle(name)
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
	sys.exit(app.exec_())