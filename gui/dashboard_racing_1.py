from PyQt5 import QtWidgets, QtGui, QtCore

class DashboardRacing1(QtWidgets.QWidget):
    def __init__(self, m):
        super().__init__()
        self.m = m
        self.setStyleSheet("background-color: black;")
        layout = QtWidgets.QGridLayout(self)

        self.speed_val = QtWidgets.QLabel("000 km/h")
        self.rpm_val = QtWidgets.QLabel("0000 RPM")
        self.temp_val = QtWidgets.QLabel("000 °C")
        self.acc_val = QtWidgets.QLabel("000 %")

        for lbl in [self.speed_val, self.rpm_val, self.temp_val, self.acc_val]:
            lbl.setFont(QtGui.QFont("DS-Digital", 28))
            lbl.setAlignment(QtCore.Qt.AlignCenter)
            lbl.setStyleSheet("color: white; background: transparent;")

        self.speed_bar = self.crea_barra("#00ff99", 250)
        self.rpm_bar = self.crea_barra("#ffff00", 9000)
        self.temp_bar = self.crea_barra("#ff5555", 120)
        self.acc_bar = self.crea_barra("#ffaa00", 100)

        layout.addLayout(self.stack(self.speed_val, self.speed_bar), 0, 0)
        layout.addLayout(self.stack(self.rpm_val, self.rpm_bar), 1, 0)
        layout.addLayout(self.stack(self.temp_val, self.temp_bar), 2, 0)
        layout.addLayout(self.stack(self.acc_val, self.acc_bar), 3, 0)

    def stack(self, label_widget, bar_widget):
        box = QtWidgets.QVBoxLayout()
        box.setSpacing(5)
        box.addWidget(label_widget)
        box.addWidget(bar_widget)
        return box

    def crea_barra(self, colore, max_val):
        bar = QtWidgets.QProgressBar()
        bar.setMaximum(max_val)
        bar.setTextVisible(False)
        bar.setFixedHeight(20)
        bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid #555;
                background-color: #111;
            }}
            QProgressBar::chunk {{
                background-color: {colore};
            }}
        """)
        return bar

    def aggiorna(self):
        v = int(self.m.velocita)
        rpm = int(self.m.giri_motore)
        t = int(self.m.temperatura_motore)
        acc = int(self.m.pedale_acceleratore)

        self.speed_val.setText(f"Velocità  {v:03} km/h")
        self.rpm_val.setText(f"Giri motore {rpm:04} RPM")
        self.temp_val.setText(f"Temperatura {t:03} °C")
        self.acc_val.setText(f"Gas Pedal  {acc:03} %")

        self.speed_bar.setValue(v)
        self.rpm_bar.setValue(rpm)
        self.temp_bar.setValue(t)
        self.acc_bar.setValue(acc)
