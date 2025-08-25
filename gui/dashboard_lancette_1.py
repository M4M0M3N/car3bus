from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap
from gui.gauge_widget_1 import GaugeWidget
import os

class DashboardLancette1(QtWidgets.QWidget):
    def __init__(self, m):
        super().__init__()
        self.m = m
        layout = QtWidgets.QVBoxLayout(self)

        self.vel = GaugeWidget("Velocità", "km/h", 220, angle_span=180)
        self.rpm = GaugeWidget("RPM", "", 7000, angle_span=230)
        self.temp = GaugeWidget("Temp", "°C", 120, angle_span=180)
        self.acc = GaugeWidget("Gas", "%", 100, angle_span=180)

        grid = QtWidgets.QGridLayout()  # Crea un layout a griglia per posizionare i widget in righe e colonne
        grid.setVerticalSpacing(10)  # Imposta lo spazio verticale tra le righe della griglia (30 pixel)
        grid.setContentsMargins(30, 1, 30, 0)  # Imposta i margini (sinistra, sopra, destra, sotto) attorno alla griglia

        # RIMUOVI le dimensioni minime per evitare ridisegni costosi
        # grid.setRowMinimumHeight(0, 300)      # La riga 0 avrà almeno 300 pixel di altezza
        # grid.setRowMinimumHeight(1, 300)      # La riga 1 avrà almeno 300 pixel di altezza
        # grid.setColumnMinimumWidth(0, 200)    # La colonna 0 avrà almeno 200 pixel di larghezza
        # grid.setColumnMinimumWidth(1, 200)    # La colonna 1 avrà almeno 200 pixel di larghezza

        # Aggiunge i widget Gauge alle rispettive celle della griglia
        grid.addWidget(self.vel, 0, 0)   # Gauge velocità in riga 0, colonna 0
        grid.addWidget(self.rpm, 0, 1)   # Gauge RPM in riga 0, colonna 1
        grid.addWidget(self.temp, 1, 0)  # Gauge temperatura in riga 1, colonna 0
        grid.addWidget(self.acc, 1, 1)   # Gauge acceleratore in riga 1, colonna 1

        layout.addLayout(grid)

        # 👇 Spie aggiuntive: freccia e luce
        self.spie = QtWidgets.QHBoxLayout()
        self.spia_freccia = QtWidgets.QLabel(" ")
        self.spia_luce = QtWidgets.QLabel(" ")

        font = self.spia_freccia.font()
        font.setPointSize(24)
        self.spia_freccia.setFont(font)
        self.spia_luce.setFont(font)

        self.spie.addWidget(self.spia_freccia)
        self.spie.addWidget(self.spia_luce)
        layout.addLayout(self.spie)

    def toggle_freccia(self):
        freccia = self.m.freccia
        if freccia == "off":
            self.spia_freccia.setText("")
            return

        if self.lamp_visible:
            if freccia == "sx":
                self.spia_freccia.setText("⏪")
            elif freccia == "dx":
                self.spia_freccia.setText("⏩")
            elif freccia == "all":
                self.spia_freccia.setText("🔁")
        else:
            self.spia_freccia.setText("")
        self.lamp_visible = not self.lamp_visible

    def aggiorna(self):

        self.vel.set_value(int(self.m.velocita))
        self.rpm.set_value(int(self.m.giri_motore))
        self.temp.set_value(int(self.m.temperatura_motore))
        self.acc.set_value(int(self.m.pedale_acceleratore))

        # 🔆 Aggiorna stato luci
        if self.m.luci == 0:
            file = f"{os.getcwd()}/gui/img/luci_spente.png"

        elif self.m.luci == 1:
            file = f"{os.getcwd()}/gui/img/luci_aspente.png"
        
        elif self.m.luci == 2:
            file = f"{os.getcwd()}/gui/img/luci_abbaglianti.png"
        
        # Percorso assoluto rispetto a questo script
        abs_file = file
        if not os.path.isabs(file):
            abs_file = os.path.join(os.path.dirname(__file__), file)
        pixmap = QPixmap(abs_file)
        pixmap = pixmap.scaled(50,50, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.spia_luce.setPixmap(pixmap)
