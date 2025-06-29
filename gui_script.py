from PyQt5 import QtWidgets, QtCore
from gui.dashboard_testuale_1 import DashboardTestuale1
from gui.dashboard_racing_1 import DashboardRacing1
from gui.dashboard_racing_2 import DashboardRacing2
from gui.dashboard_lancette_1 import DashboardLancette1
from gui.dashboard_jdm_1 import DashboardJDM1
from gui.dashboard_grafico_1 import DashboardGrafico1


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, m):
        super().__init__()
        self.m = m
        self.setWindowTitle("Mazda Dashboard")
        self.setFixedSize(900, 700)
        self.setStyleSheet("background-color: black;")

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QGridLayout(central)

        self.stacked = QtWidgets.QStackedWidget()
        layout.addWidget(self.stacked, 0, 0, 1, 3)

        # Aggiunta delle dashboard importate

        self.testo_1 = DashboardTestuale1(m)
        self.racing_1 = DashboardRacing1(m)
        self.racing_2 = DashboardRacing2(m)
        self.lancette_1 = DashboardLancette1(m)
        self.jdm_1 = DashboardJDM1(m)
        self.grafico_1 = DashboardGrafico1(m)

        self.stacked.addWidget(self.testo_1)
        self.stacked.addWidget(self.racing_1)
        self.stacked.addWidget(self.racing_2)
        self.stacked.addWidget(self.lancette_1)
        self.stacked.addWidget(self.jdm_1)
        self.stacked.addWidget(self.grafico_1)

        self.stacked.setCurrentWidget(self.racing_2)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_all)
        self.timer.start(500)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Right:
            i = (self.stacked.currentIndex() + 1) % self.stacked.count()
            self.stacked.setCurrentIndex(i)
        elif event.key() == QtCore.Qt.Key_Left:
            i = (self.stacked.currentIndex() - 1) % self.stacked.count()
            self.stacked.setCurrentIndex(i)

    def update_all(self):
        # Aggiorna sempre la dashboard grafica
        self.grafico_1.aggiorna()
        
        # Aggiorna anche la GUI attiva, se diversa da grafico_1
        current_widget = self.stacked.currentWidget()
        if current_widget is not self.grafico_1:
            current_widget.aggiorna()
