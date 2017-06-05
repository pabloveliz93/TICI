import serial #PySerial
from getch import getch, pause #py-getch
#from time import sleep
def avg(A):
	return float(sum(A) / len(A))
#ser = serial.Serial('COM3', 9600)

#Definición de constantes
VOL_CODE = b'9997'
TEMP_CODE = b'9998'
FLUX_CODE = b'9996'
VOL_SETUP_CODE = b'9999'

#Clase Principal
class Principal:
	def __init__(self):
		self.s = -1
		self.vol_hbase = 35.63
		self.vol_hmax = 10
		self.vol_queue = []
		self.current_vol = 0
		self.current_temp = 0
		self.current_flux = 0
	def set_serial(self,s): #Setea un serial
		self.s = s
	def calibrar_altura(self, hmax, hbase): #setea las alturas (base y max)
		self.vol_hmax = hmax
		self.vol_hbase = hbase
	def add_vol_data(self): #Retorna la medición directa de la altura
		if len(self.vol_queue) == 10:
			self.vol_queue.pop(0)
		self.s.write(VOL_CODE)
		data = float(str(self.s.readline())[2:-5])
		self.vol_queue.append(data)
	def get_vol(self): #Retorna el porcentaje volumétrico actual del contenedor
		return round(((self.vol_hbase - avg(self.vol_queue)) / (self.vol_hbase - self.vol_hmax)) * 100)
	def get_temp(self): #Retorna la temperatura actual en grados celcius del contenedor
		self.s.write(TEMP_CODE)
		data = float(str(self.s.readline())[2:-5])
		return data
	def get_flux(self): #Retorna el flujo en cm3/s
		self.s.write(FLUX_CODE)
		data = float(str(self.s.readline())[2:-5])
		return data

#Clase alertador
class Alertador:
	def __init__(self):
		self.upper_limit = 99999
		self.lower_limit = -99999
	def set_upper_limit(self, limit):
		self.upper_limit= limit
	def set_lower_limit(self, limit):
		self.lower_limit= limit
	def check_muestra(self, muestra):
		if muestra < self.lower_limit:
			return -1
		elif muestra > self.upper_limit:
			return 1
		return 0

#pcp = Principal()
#pcp.set_serial(serial.Serial('COM3', 9600))
#print("Ingrese dato a enviar")
#i = input()
#pcp.s.write(VOL_CODE)
#sleep(0.05)
#print(str(pcp.s.readline())[2:-5])