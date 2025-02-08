import os

from PyQt5.QtWidgets import QGraphicsPixmapItem

from PyQt5 import QtCore, QtGui, QtWidgets
from gui.mainwindow import Ui_MainWindow
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import *

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

        #aggiungi scena e adattala alle dimensioni del graphicsView
        self.scene_page_1 = QtWidgets.QGraphicsScene()
        self.scene_page_1.setSceneRect(QRectF(0, 0, self.contenitore_lancette.width()-10, self.contenitore_lancette.height()-10))
        self.contenitore_lancette.setScene(self.scene_page_1)  # Associa la scena al pedaleacc_lancetta_2

    #impostare page 1

        # Aggiungi l'immagine alla scena
        pixmap_1 = QPixmap('lancetta.png')  # Sostituisci con il percorso della tua immagine

        # Ridimensiona il pimax_1 alla dimensione desiderata
        ridimensiona = pixmap_1.width()/100
        pixmap_1 = pixmap_1.scaled(pixmap_1.width()/ridimensiona, pixmap_1.height()/ridimensiona)

        self.velocita_lancetta = QGraphicsPixmapItem(pixmap_1)
        self.girimotore_lancetta = QGraphicsPixmapItem(pixmap_1)
        self.pedaleacc_lancetta = QGraphicsPixmapItem(pixmap_1)
        self.temperatura_lancetta = QGraphicsPixmapItem(pixmap_1)

        self.scene_page_1.addItem(self.velocita_lancetta)
        self.scene_page_1.addItem(self.girimotore_lancetta)
        self.scene_page_1.addItem(self.pedaleacc_lancetta)
        self.scene_page_1.addItem(self.temperatura_lancetta)

        x,y = pixmap_1.width() / 2, pixmap_1.height() / 2

        self.velocita_lancetta.setTransformOriginPoint(x,y)
        self.girimotore_lancetta.setTransformOriginPoint(x,y)
        self.pedaleacc_lancetta.setTransformOriginPoint(x,y)
        self.temperatura_lancetta.setTransformOriginPoint(x,y)

        x, spazio = 20, 58

        self.velocita_lancetta.setPos(x, spazio)
        self.girimotore_lancetta.setPos(x, spazio*3)
        self.pedaleacc_lancetta.setPos(x, spazio*5)
        self.temperatura_lancetta.setPos(x, spazio*7)

    #impostare page 2

        self.scene_page_2 = QtWidgets.QGraphicsScene()
        self.scene_page_2.setSceneRect(QRectF(0, 0, self.contenitore_page_2.width() - 10, self.contenitore_page_2.height() - 10))
        self.contenitore_page_2.setScene(self.scene_page_2)

        # Aggiungi l'immagine alla scena_2
        pixmap_2_s = QPixmap('sfondo_2')
        pixmap_2_l = QPixmap('lancetta_2')

        # Ridimensiona il pimax_1 alla dimensione desiderata
        ridimensiona_s = pixmap_2_s.width() / self.contenitore_page_2.width()
        ridimensiona_l = pixmap_2_l.width() / self.contenitore_page_2.width()

        pixmap_2_s = pixmap_2_s.scaled(pixmap_2_s.width() / ridimensiona_s, pixmap_2_s.height() / ridimensiona_s)
        pixmap_2_l = pixmap_2_l.scaled(pixmap_2_l.width() / ridimensiona_l, pixmap_2_l.height() / ridimensiona_l)

        self.giri_motore_2_s = QGraphicsPixmapItem(pixmap_2_s)
        self.giri_motore_2_l = QGraphicsPixmapItem(pixmap_2_l)

        self.giri_motore_2_l.setTransformOriginPoint(pixmap_2_l.width() / 2, pixmap_2_l.height() / 2)

        self.scene_page_2.addItem(self.giri_motore_2_s)
        self.scene_page_2.addItem(self.giri_motore_2_l)

        self.pedaleacc_bar.setOrientation(Qt.Vertical)


    # Timer per aggiornare le lancette e i testi
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(50)  # Aggiorna ogni mezzo secondo

    def switch_page(self):
        # Cambia pagina del QStackedWidget
        current_index = self.stackedWidget.currentIndex()

        if current_index == self.stackedWidget.count()-1:
            self.stackedWidget.setCurrentIndex(0)
        else:
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

            angle_girimotore = self.m.giri_motore / 9000 * 270
            self.giri_motore_2_l.setRotation(angle_girimotore)
        except:
            pass

        try:
            angle_pedaleacc = self.m.pedale_acceleratore / 100 * 180
            self.pedaleacc_lancetta.setRotation(angle_pedaleacc)
            self.pedaleacc_bar.setValue(self.m.pedale_acceleratore)

            self.update_progress_bar_color()

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
            self.velocita_text_2.setText(str(self.m.velocita))
            self.girimotore_text.setText(f"Giri Motore: {self.m.giri_motore} RPM")
            self.pedaleacc_text.setText(f"Pedale: {self.m.pedale_acceleratore} %")
            self.temperatura_text.setText(f"Temperatura: {self.m.temperatura_motore} °C")

        except:
            pass

    def update_progress_bar_color(self):
        value = self.pedaleacc_bar.value()

        if value <= 40:
            # Verde
            red = 0
            green = 255
        elif 41 <= value <= 50:
            # Da verde a giallo
            red = int(((value - 40) / 10) * 255)
            green = 255
        elif 51 <= value <= 70:
            # Giallo
            red = 255
            green = 255
        elif 71 <= value <= 80:
            # Da giallo a rosso
            red = 255
            green = int(255 - ((value - 70) / 10) * 255)
        else:
            # Rosso
            red = 255
            green = 0

        color = f"rgb({red}, {green}, 0)"

        # Aggiorna il foglio di stile della barra di progresso
        self.pedaleacc_bar.setStyleSheet(f"""
            QProgressBar::chunk {{
                background-color: {color};
            }}
        """)


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
