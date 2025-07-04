from PyQt5 import QtWidgets, QtGui, QtCore

class DashboardTestuale1(QtWidgets.QWidget):
    def __init__(self, m):
        super().__init__()
        self.m = m
        layout = QtWidgets.QGridLayout(self)

        font_digital = QtGui.QFont("DS-Digital", 38)
        if "DS-Digital" not in QtGui.QFontDatabase().families():
            font_digital = QtGui.QFont("Courier", 38)

        self.vel_label = QtWidgets.QLabel("VEL: 000 km/h")
        self.giri_label = QtWidgets.QLabel("RPM: 0000")
        self.pedale_label = QtWidgets.QLabel("ACC: 00 %")
        self.temp_label = QtWidgets.QLabel("TEMP: 00 °C")

        for label, color in [
            (self.vel_label, "lime"),
            (self.giri_label, "cyan"),
            (self.pedale_label, "orange"),
            (self.temp_label, "red"),
        ]:
            label.setFont(font_digital)
            label.setStyleSheet(f"color: {color}; background-color: #111; border: 2px solid {color};")
            label.setAlignment(QtCore.Qt.AlignCenter)

        self.pedale_bar = QtWidgets.QProgressBar()
        self.pedale_bar.setOrientation(QtCore.Qt.Vertical)
        self.pedale_bar.setMinimum(0)
        self.pedale_bar.setMaximum(100)
        self.pedale_bar.setValue(0)
        self.pedale_bar.setFixedHeight(200)
        self.pedale_bar.setTextVisible(False)

        layout.addWidget(self.vel_label, 0, 0)
        layout.addWidget(self.giri_label, 1, 0)
        layout.addWidget(self.pedale_label, 2, 0)
        layout.addWidget(self.temp_label, 3, 0)
        layout.addWidget(self.pedale_bar, 0, 1, 4, 1)

    def aggiorna(self):
        v = int(self.m.velocita)
        rpm = int(self.m.giri_motore)
        acc = int(self.m.pedale_acceleratore)
        temp = int(self.m.temperatura_motore)

        self.vel_label.setText(f"VEL: {v:03} km/h")
        self.giri_label.setText(f"RPM: {rpm:04}")
        self.pedale_label.setText(f"ACC: {acc:02} %")
        self.temp_label.setText(f"TEMP: {temp:02} °C")

        color = "lime"
        if acc > 70:
            color = "red"
        elif acc > 40:
            color = "orange"

        self.pedale_bar.setValue(acc)
        self.pedale_bar.setStyleSheet(f"QProgressBar::chunk {{ background-color: {color}; }}")
