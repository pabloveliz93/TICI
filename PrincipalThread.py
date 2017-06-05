from proyectoTICS1 import *
from time import sleep, time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont, QColor
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from qtRangeSlider import QHSpinBoxRangeSlider
import matplotlib.pyplot as plt
from serial import SerialException
#import auxlib

# Thread para conectar el software principal con nuestra interfaz gráfica
class Thread(QThread):
    def __init__(self):
        super().__init__()
        self.p = Principal()
        self.port = ""
        self.vol = 0
        self.temp = 0
        self.flux = 0
        self.running = True
        self.promediadorVolumen = []
        self.promediadorTemperatura = []
        self.promediadorFlujo = []
        self.cola_volumen = []
        self.cola_temperatura = []
        self.cola_flujo = []
        self.cola_tiempo = []
        curr = time()
        for x in range(0, 600) :
            self.cola_temperatura.append(0)
            self.cola_flujo.append(0)
            self.cola_volumen.append(0)
            self.cola_tiempo.append(curr - 0.5 * (600 - x))

        self.vol_graf = plt.plot(self.cola_tiempo, self.cola_volumen)
        self.flux_graf = plt.plot(self.cola_tiempo, self.cola_flujo)
        self.temp_graf = plt.plot(self.cola_tiempo, self.cola_temperatura)
        self.run_init()

    def serial_connect(self):
        try:
            self.p.set_serial(serial.Serial(self.port, 9600))
            sleep(3)
        except SerialException:
            print("Error de conexión")
    def is_paused(self):
        return self.running == False
    def resume(self):
        self.running = True
        self.start()
    def pause(self):
        self.running = False
    def set_alert_signal(self, s):
        self.alertSignal = s
    def set_main_window(self, w):
        self.m = w

    def set_vol_label(self, label):
        self.vollabel = label

    def set_temp_label(self, label):
        self.templabel = label

    def set_flux_label(self, label):
        self.fluxlabel = label
    def update_labels(self):
        self.vollabel.setText(str(self.vol))
        self.templabel.setText(str(self.temp))
        self.fluxlabel.setText(str(self.flux))
    def run_init(self):
        self.vol_alertador = Alertador()
        self.temp_alertador = Alertador()
        sleep(3)
    def actualizar_cola_prom(self, data, prom, cola):
        prom.append(data)
        if len(prom) > 15:
            prom.pop(0)
        promedio = 0
        for x in range(len(prom)):
            promedio += prom[x]
        cola.append(promedio/len(prom))
        cola.pop(0)
    def actualizar_cola_tiempo(self,data):
        self.cola_tiempo.append(data)
        self.cola_tiempo.pop(0)
    def set_port(self, port):
        self.port = port
    def check_vol_limits(self):
        title = "Precaución: volumen crítico"
        checker = self.vol_alertador.check_muestra(self.vol)
        if checker != 0:
            if checker == 1:
                text = "El volumen ha superado el límite establecido.\nEl proceso se ha pausado para que el problema sea corregido.\nPuede reanudar el proceso cuando quiera desde la pantalla principal."
            elif checker == -1:
                text = "El volumen está por debajo del límite establecido.\nEl proceso se ha pausado para que el problema sea corregido.\nPuede reanudar el proceso cuando quiera desde la pantalla principal."
            self.pause()
            self.alertSignal.emit(title, text, self)
    def check_temp_limits(self):
        title = "Precaución: temperatura crítica"
        checker = self.temp_alertador.check_muestra(self.temp)
        if checker != 0:
            if checker == 1:
                text = "La temperatura ha superado el límite establecido.\nEl proceso se ha pausado para que el problema sea corregido.\nPuede reanudar el proceso cuando quiera desde la pantalla principal."
            elif checker == -1:
                text = "La temperatura está por debajo del límite establecido.\nEl proceso se ha pausado para que el problema sea corregido.\nPuede reanudar el proceso cuando quiera desde la pantalla principal."
            self.pause()
            self.alertSignal.emit(title, text, self)

    def run(self):
        while self.running == True:
            self.temp = self.p.get_temp()
            self.actualizar_cola_prom(self.temp, self.promediadorTemperatura, self.cola_temperatura)
            self.update_labels()
            sleep(1)
            for i in range(600):
                curr = time()
                self.p.add_vol_data()
                #print("vol data added")
                self.vol = self.p.get_vol()
                #print("vol updated")
                self.actualizar_cola_prom(self.vol, self.promediadorVolumen, self.cola_volumen)
                self.check_vol_limits()
                self.check_temp_limits()
                sleep(0.05)
                self.flux = self.p.get_flux()
                #print("flux added")
                self.actualizar_cola_prom(self.flux, self.promediadorFlujo, self.cola_flujo)
                sleep(0.05)
                self.update_labels()
                #print("labels updated")
                #print(self.running)
                self.actualizar_cola_tiempo(curr)
                if self.is_paused():
                    break