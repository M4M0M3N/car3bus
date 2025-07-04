from PyQt5 import QtWidgets, QtGui, QtCore
import os

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
            sp_fine = int(30 + 20 * perc)  # cresce da 30 a 50

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

        # --- Gestione cartelle video ---
        self.video_base_dir = os.path.join(os.getcwd(), "gui", "video")
        self.subfolders = [f for f in os.listdir(self.video_base_dir) if os.path.isdir(os.path.join(self.video_base_dir, f))]
        print(self.subfolders)  # Debug: stampa le cartelle trovate
        self.subfolders.sort()
        self.current_folder_idx = 0
        self.frames = []
        self.load_frames_from_current_folder()

    def load_frames_from_current_folder(self):
        if not self.subfolders:
            self.frames = []
            return
        folder = self.subfolders[self.current_folder_idx]
        folder_path = os.path.join(self.video_base_dir, folder)
        files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith('.png')])
        self.frames = []
        for fname in files:
            path = os.path.join(folder_path, fname)
            pix = QtGui.QPixmap(path)
            if os.path.exists(path) and not pix.isNull():
                self.frames.append(pix)
        # Aggiorna QLabel subito se esiste
        if hasattr(self, "label_video") and self.frames:
            self.label_video.setPixmap(self.frames[0])


    def cambia_cartella(self, direzione):
        # direzione: +1 (su), -1 (giu)
        if self.subfolders:
            self.current_folder_idx = (self.current_folder_idx + direzione) % len(self.subfolders)
            self.load_frames_from_current_folder()
        
    def aggiorna(self):
        giri = getattr(self.m, 'giri_motore', 0)
        self.barra.set_valore(min(giri / 7000.0, 1.0))

        # Aggiorna i 3 display 7 segmenti con la velocità
        vel = int(getattr(self.m, 'velocita', 0))
        vel_str = f"{vel:03d}"[-3:]  # sempre 3 cifre
        for i, disp in enumerate(self.displays):
            disp.display(int(vel_str[i]))

        # --- Mostra il frame video proporzionale ai giri motore ---
        if self.frames:
            idx = int((giri / 7000.0) * (len(self.frames) - 1))
            idx = max(0, min(idx, len(self.frames) - 1))
            # Se non hai già un QLabel per mostrare il frame, crealo una volta sola:
            if not hasattr(self, "label_video"):
                self.label_video = QtWidgets.QLabel(self)
                self.label_video.setGeometry(150, 300, 640, 360)
                self.label_video.show()
            self.label_video.setPixmap(self.frames[idx])
            # Mostra anche il nome della cartella corrente come overlay
            folder_name = self.subfolders[self.current_folder_idx] if self.subfolders else "-"
            self.label_video.setToolTip(f"Cartella: {folder_name}")
