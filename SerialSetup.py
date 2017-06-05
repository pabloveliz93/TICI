import sys
import serial.tools.list_ports
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class SSWidget(QWidget):

	def __init__(self):
		super().__init__()
		self.initUI()
		self.port = ""
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
		self.connectbutton = QPushButton("Aceptar")
		self.connectbutton.clicked.connect(self.aceptar)
		layout2.addWidget(scanbutton)
		layout2.addWidget(self.connectbutton)
		layout.addLayout(layout2)
	def alert(self, wd_title, text):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Warning)
		msg.setText(text)
		msg.setWindowTitle(wd_title)
		msg.setStandardButtons(QMessageBox.Ok)
		#msg.buttonClicked.connect(thread.resume)
		msg.exec_()
	def aceptar(self):
		self.port = self.combobox.currentText()
		if self.port == "":
			self.alert("Puerto indefinido", "No se ha establecido ningún puerto para la conexión. \nEl proceso no podrá reanudarse hasta que se establezca una conexión exitosa.")
		else:
			self.port = self.port[:4]
		self.hide()
	def scan(self):
		ports = list(serial.tools.list_ports.comports())
		self.combobox.clear()
		if len(ports) > 0:
			for p in ports:
				self.combobox.addItem(str(p))

#Eliminar todo esto, es solo de prueba
#if __name__ == '__main__':
#	app = QApplication(sys.argv)
#	ex = SerialSetupWindow()
#	ex.show()
#	sys.exit(app.exec_())