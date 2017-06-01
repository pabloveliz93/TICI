import sys
import serial.tools.list_ports
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class SerialSetupWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()
	def initUI(self):
		layout = QVBoxLayout()
		self.combobox = QComboBox()
		self.scan()
		layout.addWidget(QLabel("Seleccione el dispositivo:"))
		layout.addWidget(self.combobox)
		self.setLayout(layout)
		self.setWindowTitle("Configuración de conexión")
		layout2 = QHBoxLayout()
		scanbutton = QPushButton("Escanear puertos")
		scanbutton.clicked.connect(self.scan)
		connectbutton = QPushButton("Conectar")
		layout2.addWidget(scanbutton)
		layout2.addWidget(connectbutton)
		layout.addLayout(layout2)
	def scan(self):
		ports = list(serial.tools.list_ports.comports())
		self.combobox.clear()
		if len(ports) > 0:
			for p in ports:
				self.combobox.addItem(str(p))

#Eliminar todo esto, es solo de prueba
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = SerialSetupWindow()
	ex.show()
	sys.exit(app.exec_())