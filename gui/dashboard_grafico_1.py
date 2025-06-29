from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

class DashboardGrafico1(QtWidgets.QWidget):
    def __init__(self, m):
        super().__init__()
        self.m = m
        layout = QtWidgets.QVBoxLayout(self)

        # Crea una figura matplotlib con 4 sottografi
        self.fig, self.axes = plt.subplots(4, 1, figsize=(8, 10), sharex=True)
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        # Dati iniziali vuoti
        self.time = []
        self.temp = []
        self.vel = []
        self.rpm = []
        self.acc = []

        # Salva il tempo di avvio in secondi
        self.start_time = QtCore.QTime.currentTime().msecsSinceStartOfDay() / 1000.0


    def aggiorna(self):
        # Calcola i minuti trascorsi dall'accensione
        now = QtCore.QTime.currentTime().msecsSinceStartOfDay() / 1000.0
        t = (now - self.start_time) / 60.0  # minuti trascorsi
        self.time.append(t)
        self.temp.append(self.m.temperatura_motore)
        self.vel.append(self.m.velocita)
        self.rpm.append(self.m.giri_motore)
        self.acc.append(self.m.pedale_acceleratore)

        # Mantieni solo gli ultimi 240 punti, 2 minuti se timer ogni 0.5 min
        self.time = self.time[-240:]
        self.temp = self.temp[-240:]
        self.vel = self.vel[-240:]
        self.rpm = self.rpm[-240:]
        self.acc = self.acc[-240:]

        # Pulisci e ridisegna i grafici con sfondo nero e testi chiari
        labels = ["Temperatura (°C)", "Velocità (km/h)", "Giri motore (RPM)", "Pedale Gas (%)"]
        dati = [self.temp, self.vel, self.rpm, self.acc]
        ylims = [None, None, None, (0, 100)]  # limiti verticali per ogni grafico
        for ax, y, label, ylim in zip(self.axes, dati, labels, ylims):
            ax.clear()
            ax.plot(self.time, y, color="cyan")
            ax.set_ylabel(label, color="white")
            ax.grid(True, color="gray")
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            ax.set_facecolor("black")
            if ylim is not None:
                ax.set_ylim(*ylim)  # imposta i limiti verticali
            ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%d'))  # <-- senza decimali
        self.axes[-1].set_xlabel("Minuti dall'accensione", color="white")
        self.axes[-1].xaxis.set_major_formatter(mticker.FormatStrFormatter('%d'))  # <-- senza decimali anche sull'asse X
        self.fig.patch.set_facecolor('black')
        self.fig.tight_layout()
        self.canvas.draw()
