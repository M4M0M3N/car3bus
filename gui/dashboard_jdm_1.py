from PyQt5 import QtWidgets, QtGui, QtCore

class DashboardJDM1(QtWidgets.QWidget):
    def __init__(self, m):
        super().__init__()
        self.m = m

        self.setStyleSheet("""
            QWidget {
                background-color: black;
            }
        """)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 30, 40, 30)

        font_jdm = QtGui.QFont("DS-Digital", 28)
        color_labels = ["#00ffff", "#ff66ff", "#ffff00", "#ff4444"]

        self.labels = []
        self.bars = []
        self.valori = []
        self.flash_timers = {}
        self.flash_state = {}

        self.indicatori = [
            ("スピード", "km/h", 250),
            ("ターボ PSI", "PSI", 1.5),
            ("バッテリー", "V", 16),
            ("オイルプレッシャー", "bar", 5),
        ]

        for i, (jp_label, unit, max_val) in enumerate(self.indicatori):
            color = color_labels[i % len(color_labels)]

            titolo = QtWidgets.QLabel(jp_label)
            titolo.setFont(font_jdm)
            titolo.setStyleSheet(f"color: {color};")
            layout.addWidget(titolo)

            valore = QtWidgets.QLabel("--")
            valore.setFont(QtGui.QFont("DS-Digital", 24))
            valore.setStyleSheet("color: white; background: transparent;")
            valore.setAlignment(QtCore.Qt.AlignLeft)
            layout.addWidget(valore)
            self.valori.append((valore, unit))

            bar = QtWidgets.QProgressBar()
            bar.setMaximum(int(max_val * 100))
            bar.setMinimum(0)
            bar.setFixedHeight(20)
            bar.setTextVisible(False)
            bar.setStyleSheet(f"""
                QProgressBar {{
                    border: 1px solid #555;
                    background-color: #222;
                }}
                QProgressBar::chunk {{
                    background-color: {color};
                }}
            """)
            layout.addWidget(bar)
            self.bars.append((bar, max_val))

            self.flash_state[i] = False
            timer = QtCore.QTimer()
            timer.timeout.connect(lambda i=i: self.toggle_flash(i))
            timer.setInterval(200)
            self.flash_timers[i] = timer

    def toggle_flash(self, i):
        bar, _ = self.bars[i]
        current = self.flash_state[i]
        base_color = ["#00ffff", "#ff66ff", "#ffff00", "#ff4444"][i % 4]
        color = "#ffffff" if current else base_color
        bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid #555;
                background-color: #222;
            }}
            QProgressBar::chunk {{
                background-color: {color};
            }}
        """)
        self.flash_state[i] = not current

    def aggiorna(self):
        v = int(self.m.velocita)
        turbo = self.m.giri_motore / 9000.0 * 1.5
        volt = 12.0 + (self.m.pedale_acceleratore / 100.0) * 2.0
        pressure = 1.5 + (self.m.temperatura_motore / 120.0) * 3.0

        dati = [v, turbo, volt, pressure]
        for i, (val, (lbl, unit), (bar, max_val)) in enumerate(zip(dati, self.valori, self.bars)):
            percent = val * 100 / max_val if max_val else 0

            lbl.setText(f"{val:.2f} {unit}" if isinstance(val, float) else f"{val} {unit}")
            bar.setValue(int(val * 100))

            if percent >= 90:
                if not self.flash_timers[i].isActive():
                    self.flash_timers[i].start()
            else:
                self.flash_timers[i].stop()
                base_color = ["#00ffff", "#ff66ff", "#ffff00", "#ff4444"][i % 4]
                bar.setStyleSheet(f"""
                    QProgressBar {{
                        border: 1px solid #555;
                        background-color: #222;
                    }}
                    QProgressBar::chunk {{
                        background-color: {base_color};
                    }}
                """)
                self.flash_state[i] = False
