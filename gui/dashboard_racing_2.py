from PyQt5 import QtWidgets, QtGui, QtCore
import math

class BarraGiriGomito(QtWidgets.QWidget):
    def __init__(self, colore="#c084f5"):
        super().__init__()
        self.valore = 0.0  # Valore normalizzato 0.0 – 1.0
        self.setFixedSize(900, 350)  # Dimensione fissa della barra, puoi modificare a piacere
        self.colore = colore  # salva il colore come variabile

    def set_valore(self, val):
        self.valore = max(0.0, min(val, 1.0))
        self.update()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        max_rpm = 7000
        soglia = 0.3  # dove si trova lo spigolo nel valore normalizzato

        # Geometria barra
        base_x = int(w * 0.1)
        base_y = h - 40
        dx_inclinato = int(w * 0.18)
        dy_inclinato = int(h * 0.3)
        dx_orizzontale = int(w * 0.62)

        colore_barra = QtGui.QColor(self.colore)
        colore_testi = QtGui.QColor("#888")
        colore_contorno = QtGui.QColor("#fff")  # colore contorno bianco

        qp.fillRect(self.rect(), QtGui.QColor("#000"))
        qp.setBrush(colore_barra)
        qp.setPen(QtCore.Qt.NoPen)

        # --- Barra con spessore variabile (riempimento)
        if self.valore <= soglia: #solo barra obliqua
            perc = self.valore / soglia
            x1 = base_x + int(dx_inclinato * perc)
            y1 = base_y - int(dy_inclinato * perc)
            sp_start = int(10 + 20 * 0.0)
            sp_end = int(10 + 20 * perc)

            path = QtGui.QPainterPath()
            path.moveTo(base_x, base_y)
            path.lineTo(x1, y1)
            path.lineTo(x1, y1 - sp_end)
            path.lineTo(base_x, base_y - sp_start)
            path.closeSubpath()
            qp.drawPath(path)
        else:
            # Tratto inclinato pieno
            sp_start = int(10 + 20 * 0.0)
            sp_mid = int(10 + 20 * 1.0)
            path1 = QtGui.QPainterPath()
            path1.moveTo(base_x, base_y)
            path1.lineTo(base_x + dx_inclinato, base_y - dy_inclinato)
            path1.lineTo(base_x + dx_inclinato, base_y - dy_inclinato - sp_mid)
            path1.lineTo(base_x, base_y - sp_start)
            path1.closeSubpath()
            qp.drawPath(path1)

            # Tratto orizzontale con altezza che cresce col valore
            perc = (self.valore - soglia) / (1.0 - soglia)
            lunghezza = int(dx_orizzontale * perc)
            x_start = base_x + dx_inclinato
            y_start = base_y - dy_inclinato
            sp_inizio = sp_mid
            sp_fine = int(10 + 20 * perc)  # cresce da 10 a 30

            path2 = QtGui.QPainterPath()
            path2.moveTo(x_start, y_start)
            path2.lineTo(x_start + lunghezza, y_start)
            path2.lineTo(x_start + lunghezza, y_start - sp_fine)
            path2.lineTo(x_start, y_start - sp_inizio)
            path2.closeSubpath()
            qp.drawPath(path2)

        # --- Contorno sempre presente ---
        qp.setBrush(QtCore.Qt.NoBrush)
        qp.setPen(QtGui.QPen(colore_contorno, 2))

        # Contorno tratto inclinato + orizzontale
        sp_start = int(10 + 20 * 0.0)
        sp_mid = int(10 + 20 * 1.0)
        sp_fine = int(30 + 20)
        path_contorno = QtGui.QPainterPath()
        path_contorno.moveTo(base_x, base_y)
        path_contorno.lineTo(base_x + dx_inclinato, base_y - dy_inclinato)
        path_contorno.lineTo(base_x + dx_inclinato + dx_orizzontale, base_y - dy_inclinato)
        path_contorno.lineTo(base_x + dx_inclinato + dx_orizzontale, base_y - dy_inclinato - sp_fine)
        path_contorno.lineTo(base_x + dx_inclinato, base_y - dy_inclinato - sp_mid)
        path_contorno.lineTo(base_x + dx_inclinato, base_y - dy_inclinato - sp_mid)
        path_contorno.lineTo(base_x, base_y - sp_start)
        path_contorno.closeSubpath()
        qp.drawPath(path_contorno)

        # --- Scala graduata
        qp.setPen(colore_testi)
        qp.setFont(QtGui.QFont("Arial", 8))
        step = 500
        num_tacche = max_rpm // step

        for i in range(num_tacche + 1):
            t = i / num_tacche
            rpm = i * step
            if t <= soglia:
                perc = t / soglia
                x = base_x + int(dx_inclinato * perc)
                y = base_y - int(dy_inclinato * perc) + 18
            else:
                perc = (t - soglia) / (1.0 - soglia)
                x = base_x + dx_inclinato + int(dx_orizzontale * perc)
                y = base_y - dy_inclinato + 18

            qp.drawText(x - 10, y, f"{rpm}")

        qp.end()

class DashboardRacing2(QtWidgets.QWidget):
    def __init__(self, m):
        super().__init__()
        self.m = m
        self.colore = "#c084f5"
        self.setStyleSheet("background-color: black;")

        # --- Barra giri posizionata manualmente ---
        self.barra = BarraGiriGomito(colore=self.colore)
        self.barra.setParent(self)
        self.barra.move(-50, -130)  # posizione desiderata (x, y)

        # --- 3 display 7 segmenti per la velocità ---
        self.display_container = QtWidgets.QWidget(self)
        self.display_container.setFixedSize(210, 110)
        self.display_container.move(200, 120)  # posizione assoluta (x=120, y=240)
        container_layout = QtWidgets.QHBoxLayout(self.display_container)
        container_layout.setContentsMargins(0, 0, 0, 0)

        self.displays = []
        for _ in range(3):
            disp = QtWidgets.QLCDNumber()
            disp.setDigitCount(1)
            disp.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
            disp.setStyleSheet(f"color: {self.colore}; background: #111; border: none;")
            disp.setFixedSize(70, 110)
            container_layout.addWidget(disp)
            self.displays.append(disp)

    def aggiorna(self):
        giri = getattr(self.m, 'giri_motore', 0)
        self.barra.set_valore(min(giri / 7000.0, 1.0))

        # Aggiorna i 3 display 7 segmenti con la velocità
        vel = int(getattr(self.m, 'velocita', 0))
        vel_str = f"{vel:03d}"[-3:]  # sempre 3 cifre
        for i, disp in enumerate(self.displays):
            disp.display(int(vel_str[i]))
