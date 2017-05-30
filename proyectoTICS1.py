import serial #PySerial
import re #Regex
import os #Para limpiar consola
from getch import getch, pause #py-getch
def avg(A):
	return float(sum(A) / len(A))
#ser = serial.Serial('COM3', 9600)

#Definición de constantes
VOL_CODE = b'9997'
TEMP_CODE = b'9998'
FLUX_CODE = b'9996'

#Clase Principal
class Principal:
	def __init__(self):
		self.s = -1
		self.vol_areabase = 0
		self.vol_h = 0
	def set_serial(self,s): #Setea un serial
		self.s = s
	def calibrar_altura(self, hmax, hbase): #setea las alturas (base y max)
		self.vol_hmax = hmax
		self.vol_hbase = hbase
	def get_raw_height(self): #Retorna la medición directa de la altura
		a = []
		self.s.write(VOL_CODE)
		while True:
			#data = re.findall(r'\-*[0-9]*\.[0-9]*', str(self.s.readline()))
			data = float(str(self.s.readline())[2:-5])
			#print(data)
			if data == -1: #-1 indica que ha finalizado el envío de las muestras
				break
			a.append(data)
		return avg(a)
	def get_vol(self): #Retorna el porcentaje volumétrico actual del contenedor
		return ((self.vol_hbase - self.get_raw_height()) / (self.vol_hbase - self.vol_hmax)) * 100
	def get_temperature(self): #Retorna la temperatura actual en grados celcius del contenedor
		self.s.write(TEMP_CODE)
		data = float(str(self.s.readline())[2:-5])
		return data
	def imprimir_muestreo_actual(self):
		vol_data = pcp.get_vol()
		temp_data = pcp.get_temperature()
		os.system('cls')
		print("Porcentaje volumétrico: ")
		print(round(vol_data), end='')
		print('%')
		print("Temperatura: ")
		print(temp_data, end='')
		print('°C')

#Inicialización de Principal
pcp = Principal()
pcp.set_serial(serial.Serial('COM3', 9600))
#Calibración de porcentaje volumétrico
print("Vacie el recipiente y...")
pause("Presione cualquier tecla para realizar la medición.")
print("Midiendo...")
hbase = pcp.get_raw_height()
print(hbase)
print("Se ha tomado la medición del recipiente vacío.")
print("Llene el recipiente a su punto máximo y...")
pause("Presione cualquier tecla para realizar la medición.")
print("Midiendo...")
hmax = pcp.get_raw_height()
print(hmax)
print("Se ha tomado la medición del recipiente lleno.")
pcp.calibrar_altura(hmax, hbase)
print("Se ha calibrado la medición del porcentaje volumétrico.")

#Muestreo de porcentaje volumetrico

showingdata = 0

while True:
	pcp.imprimir_muestreo_actual()