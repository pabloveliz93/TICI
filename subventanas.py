from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QThread, QTimer
from qtRangeSlider import QHSpinBoxRangeSlider
from time import time
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import auxlib


# Thread para conectar el software principal con nuestra interfaz gráfica
class Thread(QThread):
    def __init__(self):
        super().__init__()
        self.p = auxlib.Principal()
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
            curr = time()

            self.promediadorVolumen.append(self.p.vol)
            if len(self.promediadorVolumen) > 15 :
                self.promediadorVolumen.pop(0)
            promedio = 0
            for x in range(len(self.promediadorVolumen)) :
                promedio += self.promediadorVolumen[x]
            self.cola_volumen.append(promedio/len(self.promediadorVolumen))
            self.cola_volumen.pop(0)

            self.promediadorTemperatura.append(self.p.vol)
            if len(self.promediadorTemperatura) > 15:
                self.promediadorTemperatura.pop(0)
            promedio = 0
            for x in range(len(self.promediadorTemperatura)):
                promedio += self.promediadorTemperatura[x]
            self.cola_temperatura.append(promedio/len(self.promediadorTemperatura))
            self.cola_temperatura.pop(0)

            self.promediadorFlujo.append(self.p.vol)
            if len(self.promediadorFlujo) > 15:
                self.promediadorFlujo.pop(0)
            promedio = 0
            for x in range(len(self.promediadorFlujo)):
                promedio += self.promediadorFlujo[x]
            self.cola_volumen.append(promedio/len(self.promediadorVolumen))
            self.cola_volumen.pop(0)

            self.cola_tiempo.append(curr)
            self.cola_tiempo.pop(0)

# Subventana de parámetros
class SVParametros(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.addStretch(0)

        # lista dropdown de contenedores
        LDcont = QComboBox()
        nombrecont = QLabel("Tipo de contenedor:")
        layout.addWidget(nombrecont)
        layout.addStretch(1)
        layout.addWidget(LDcont)
        LDcont.addItem(None)
        LDcont.addItem("Cúbico/Cilíndrico")
        LDcont.activated[str].connect(self.LDpick)

        # Slider Temperatura
        SliderT = QHSpinBoxRangeSlider([-25, 125, 0.1], [0, 15])
        nombreT = QLabel("Rango de Temperatura:")
        layout.addWidget(nombreT)
        layout.addStretch(1)
        layout.addWidget(SliderT)
        SliderT.setEmitWhileMoving(False)
        SliderT.min_spin_box.valueChanged.connect(self.RITSBchange)
        SliderT.max_spin_box.valueChanged.connect(self.RSTSBchange)
        SliderT.range_slider.rangeChanged.connect(self.RTSchange)

        # Slider Porcentaje Volumen
        SliderV = QHSpinBoxRangeSlider([0, 100, 0.1], [5, 15])
        nombreV = QLabel("Rango de Volumen:")
        layout.addWidget(nombreV)
        layout.addStretch(1)
        layout.addWidget(SliderV)
        SliderV.setEmitWhileMoving(False)
        SliderV.min_spin_box.valueChanged.connect(self.RIVSBchange)
        SliderV.max_spin_box.valueChanged.connect(self.RSVSBchange)
        SliderV.range_slider.rangeChanged.connect(self.RVSchange)

        # Textboxes para base y altura del contenedor
        TextBoxBase = QLineEdit()
        nombrebase = QLabel("Área basal del contenedor:")
        layout.addWidget(nombrebase)
        layout.addStretch(1)
        rotuladorbase = QHBoxLayout()
        rotuladorbase.addStretch(1)
        rotuladorbase.addWidget(TextBoxBase)
        medidabase = QLabel("cm^2")
        rotuladorbase.addStretch(0)
        rotuladorbase.addWidget(medidabase)
        rotuladorbase.addStretch(1)
        layout.addLayout(rotuladorbase)
        TextBoxBase.textChanged[str].connect(self.TBBchanged)

        TextBoxAltura = QLineEdit()
        nombrealtura = QLabel("Altura del contenedor:")
        layout.addWidget(nombrealtura)
        layout.addStretch(1)
        rotuladoraltura = QHBoxLayout()
        rotuladoraltura.addStretch(1)
        rotuladoraltura.addWidget(TextBoxAltura)
        medidaaltura = QLabel("cm")
        rotuladoraltura.addStretch(0)
        rotuladoraltura.addWidget(medidaaltura)
        rotuladoraltura.addStretch(1)
        layout.addLayout(rotuladoraltura)
        TextBoxAltura.textChanged[str].connect(self.TBAchanged)

        # Checkbox y Textbox para el techo del contenedor
        self.CheckBoxTecho = QCheckBox('¿Es el techo del contenedor de área distinta a su base?')
        layout.addWidget(self.CheckBoxTecho)

        self.framelayout = QWidget()
        layoutframe = QVBoxLayout()
        rotuladorframe = QHBoxLayout()
        rotuladorframe.addStretch(1)

        nombretecho = QLabel("Área del techo del contenedor")
        layoutframe.addWidget(nombretecho)
        layoutframe.addStretch(0)

        TextBoxTecho = QLineEdit()
        rotuladorframe.addWidget(TextBoxTecho)
        rotuladorframe.addStretch(0)

        medidatecho = QLabel("cm^2")
        rotuladorframe.addWidget(medidatecho)
        rotuladorframe.addStretch(1)

        TextBoxTecho.textChanged[str].connect(self.TBTchanged)
        self.CheckBoxTecho.stateChanged.connect(self.CBTchanged)
        layoutframe.addLayout(rotuladorframe)
        self.framelayout.setLayout(layoutframe)
        layout.addWidget(self.framelayout)
        layout.addStretch(1)
        self.framelayout.hide()

        # Texto útil
        self.util = QLabel("")
        layout.addWidget(self.util)
        layout.addStretch(2)

        self.setLayout(layout)

    #Funciones de actualización. Seguro se pueden resumir pero no se ocupar connect asi que no me atrevo
    def LDpick(self, pick):
        global G_cont
        G_cont = pick
        self.util.setText("Tipo de contenedor actualizado a " + G_cont)

    def TBAchanged(self, valor):
        global G_altura
        G_altura = float(valor)
        self.util.setText("Altura actualizada a " + str(G_altura))

    def TBBchanged(self, valor):
        global G_base, G_techo
        G_base = float(valor)
        if self.CheckBoxTecho.isChecked() :
            G_techo = G_base
        self.util.setText("Área basal actualizada a " + str(G_base))

    def TBTchanged(self, valor):
        global G_techo
        G_techo = float(valor)
        self.util.setText("Área superior actualizada a " + str(G_techo))

    def CBTchanged(self, state):
        if state == Qt.Checked:
            self.framelayout.show()
        else:
            self.framelayout.hide()

    def RITSBchange(self, valor):
        global G_TI
        G_TI = valor
        self.util.setText("Rango inferior de temperatura actualizado a" + str(G_TI))

    def RSTSBchange(self, valor):
        global G_TS
        G_TS = valor
        self.util.setText("Rango superior de temperatura actualizado a" + str(G_TS))

    def RTSchange(self,valor_min,valor_max):
        global G_TI
        global G_TS
        G_TI = valor_min
        G_TS = valor_max
        self.util.setText("Rango de temperatura actualizado a " + str(G_TI) + " - "+ str(G_TS))

    def RIVSBchange(self, valor):
        global G_VI
        G_VI = valor
        self.util.setText("Rango inferior de volumen actualizado a" + str(G_VI))

    def RSVSBchange(self, valor):
        global G_VS
        G_VS = valor
        self.util.setText("Rango superior de volumen actualizado a" + str(G_VS))

    def RVSchange(self,valor_min,valor_max):
        global G_VI
        global G_VS
        G_VI = valor_min
        G_VS = valor_max
        self.util.setText("Rango de volumen actualizado a " + str(G_VI) + " - "+ str(G_VS))


# Subventana de interpretación
class SVInterpretacion(QWidget):
    def __init__(self):
        super().__init__()
        self.grafico_temperatura = QWidget()
        self.grafico_volumen = QWidget()
        self.grafico_flujo = QWidget()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.addStretch(1)

        label_volumen = QLabel("Gráfico de Volumen")
        layout.addWidget(label_volumen)
        layout.addStretch(0)
        self.lienzo_volumen = Lienzo(self.grafico_volumen)
        layout.addWidget(self.lienzo_volumen)
        layout.addStretch(1)

        label_temperatura = QLabel("Gráfico de Temperatura")
        layout.addWidget(label_temperatura)
        layout.addStretch(0)
        self.lienzo_temperatura = Lienzo(self.grafico_temperatura)
        layout.addWidget(self.lienzo_temperatura)
        layout.addStretch(1)

        label_flujo = QLabel("Gráfico de Flujo")
        layout.addWidget(label_flujo)
        layout.addStretch(0)
        self.lienzo_flujo = Lienzo(self.grafico_flujo)
        layout.addWidget(self.lienzo_flujo)
        layout.addStretch(1)

        self.setLayout(layout)


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class Lienzo(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.cola = [0]
        self.tiempo = [0]
        timer = QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

    def set_cola(self, thread):
        self.cola = thread

    def set_tiempo(self, thread):
        self.tiempo = thread

    def update_figure(self):
        self.axes.cla()
        self.axes.plot(self.tiempo, self.cola, 'r')
        self.draw()
