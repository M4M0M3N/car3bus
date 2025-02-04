import os
from time import sleep

from PyQt5.QtWidgets import QGraphicsPixmapItem

from PyQt5 import QtCore, QtGui, QtWidgets
from gui.mainwindow import Ui_MainWindow
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import Qt

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, m):

        try:
            os.chdir("gui")
        except:
            pass

        super().__init__()
        self.setupUi(self)

        self.m = m

        # Disabilitare le barre di scorrimento
        #self.graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #self.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)


        self.pushButton.clicked.connect(self.switch_page)

        self.scene = QtWidgets.QGraphicsScene()
        self.contenitore_lancette.setScene(self.scene)  # Associa la scena al pedaleacc_lancetta_2

        # Aggiungi l'immagine alla scena
        pixmap = QPixmap('lancetta.png')  # Sostituisci con il percorso della tua immagine

        # Ridimensiona il pixmap alla dimensione desiderata
        pixmap = pixmap.scaled(100, 10)

        self.velocita_lancetta = QGraphicsPixmapItem(pixmap)
        self.girimotore_lancetta = QGraphicsPixmapItem(pixmap)
        self.pedaleacc_lancetta = QGraphicsPixmapItem(pixmap)
        self.temperatura_lancetta = QGraphicsPixmapItem(pixmap)

        self.scene.addItem(self.velocita_lancetta)
        self.scene.addItem(self.girimotore_lancetta)
        self.scene.addItem(self.pedaleacc_lancetta)
        self.scene.addItem(self.temperatura_lancetta)

        x,y = pixmap.width() / 2, pixmap.height() / 2

        self.velocita_lancetta.setTransformOriginPoint(x,y)
        self.girimotore_lancetta.setTransformOriginPoint(x,y)
        self.pedaleacc_lancetta.setTransformOriginPoint(x,y)
        self.temperatura_lancetta.setTransformOriginPoint(x,y)


        x, spazio = 0, 58

        self.velocita_lancetta.setPos(x, 0)
        self.girimotore_lancetta.setPos(x, 100)
        self.pedaleacc_lancetta.setPos(x, 150)
        self.temperatura_lancetta.setPos(x, 200)

        #self.item.setTransform(transform)



        # Timer per aggiornare le lancette e i testi
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(50)  # Aggiorna ogni mezzo secondo

    def switch_page(self):
        # Cambia pagina del QStackedWidget
        current_index = self.stackedWidget.currentIndex()

        if current_index == 1:
            current_index = -1

        self.stackedWidget.setCurrentIndex(current_index + 1)


    def update_ui(self):
        #self.m.info()

        try:
            angle_velocita = self.m.velocita / 210 * 180
            self.velocita_lancetta.setRotation(angle_velocita)
        except:
            pass

        try:
            angle_girimotore = self.m.giri_motore / 6000 * 180
            self.girimotore_lancetta.setRotation(angle_girimotore)
        except:
            pass

        try:
            angle_pedaleacc = self.m.pedale_acceleratore / 100 * 180
            self.pedaleacc_lancetta.setRotation(angle_pedaleacc)
        except:
            pass


        try:
            angle_temperatura = self.m.temperatura_motore / 110 * 180
            self.temperatura_lancetta.setRotation(angle_temperatura)
        except:
            pass

        try:
            # Aggiorna i testi con i valori attuali
            self.velocita_text.setText(f"Velocità: {self.m.velocita} km/h")
            self.girimotore_text.setText(f"Giri Motore: {self.m.giri_motore} RPM")
            self.pedaleacc_text.setText(f"Pedale: {self.m.pedale_acceleratore} %")
            self.temperatura_text.setText(f"Temperatura: {self.m.temperatura_motore} °C")

        except:
            pass

def run(m):
    import warnings

    warnings.filterwarnings("ignore", category=DeprecationWarning)

    app = QtWidgets.QApplication([])
    window = MainWindow(m)
    window.show()
    app.exec_()

if __name__ == "__main__":
    from macchina import macchina

    m = macchina()
    m.giri_motore = 10
    m.pedale_acceleratore = 20
    m.velocita = 30
    m.temperatura = 40
    run(m)
