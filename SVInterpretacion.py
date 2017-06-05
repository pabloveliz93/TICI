from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QThread, QTimer
from qtRangeSlider import QHSpinBoxRangeSlider
from time import time
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
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