from PrincipalGrafica import *
from PrincipalThread import *

#Parámetros globales (¿será muy peligroso esto?)
G_cont = None  # Tipo de contenedor
G_PVI = "0"  # Rango inferior de porcentaje volumétrico
G_PVS = "0"  # Rango superior de porcentaje volumétrico
G_TI = "0"  # Rango inferior de temperatura
G_TS = "0"  # Rango superior de temperatura
G_base = 0  # Área basal
G_altura = 0  # Altura
G_techo = 0  # Área del techo

# No conseguido: marcado y desmarcado de botones
# Actualmente trabajando en: subventanas de display
# Pendientes: meter los cálculos y vínculos a Arduino, estilizar

#    def mostrar_svhistorial(self, pressed):

#    def mostrar_svalertas(self, pressed):


if __name__ == '__main__':
    app = QApplication(sys.argv)
    thr = Thread()
    ex = Ventana(thr)
    thr.set_main_window(ex)
    thr.set_vol_label(ex.Graf.volumeLabel)
    thr.set_temp_label(ex.Graf.tempLabel)
    thr.set_flux_label(ex.Graf.fluxLabel)
    thr.set_alert_signal(ex.Graf.alertSignal)
    # Supuestamente vincula la suma de datos del thread a la del grafico
    ex.Graf.svi.lienzo_temperatura.set_cola(thr.cola_temperatura)
    ex.Graf.svi.lienzo_volumen.set_cola(thr.cola_volumen)
    ex.Graf.svi.lienzo_flujo.set_cola(thr.cola_flujo)
    ex.Graf.svi.lienzo_temperatura.set_tiempo(thr.cola_tiempo)
    ex.Graf.svi.lienzo_volumen.set_tiempo(thr.cola_tiempo)
    ex.Graf.svi.lienzo_flujo.set_tiempo(thr.cola_tiempo)
    sys.exit(app.exec_())
