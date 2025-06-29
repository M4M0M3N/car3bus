from PyQt5 import QtWidgets, QtGui, QtCore
import math

class GaugeWidget(QtWidgets.QWidget):
    def __init__(self, label, unit, max_val, angle_span=180, steps=7):
        super().__init__()
        self.label = label
        self.unit = unit
        self.max_val = max_val
        self.angle_span = angle_span  # es. 180°, 230°
        self.steps = steps
        self.value = 0
        self.setMinimumSize(180, 180)

    def set_value(self, val):
        self.value = val
        self.update()

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        rect = self.rect()
        cx, cy = rect.center().x(), rect.center().y()

        # Sfondo del gauge
        gradient = QtGui.QRadialGradient(cx, cy, 90)
        gradient.setColorAt(0.0, QtGui.QColor("#222"))
        gradient.setColorAt(1.0, QtGui.QColor("#000"))
        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawEllipse(cx - 80, cy - 80, 160, 160)
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawEllipse(cx - 80, cy - 80, 160, 160)

        # Arco scala
        pen = QtGui.QPen(QtGui.QColor("#444"), 4)
        painter.setPen(pen)
        painter.drawArc(cx - 75, cy - 75, 150, 150,
                        180 * 16, -int(self.angle_span * 16))

        # Calcolo angolo della lancetta
        perc = min(self.value / self.max_val, 1.0)
        angle_deg = 180 + perc * self.angle_span
        angle_rad = math.radians(angle_deg)
        x2 = cx + 60 * math.cos(angle_rad)
        y2 = cy + 60 * math.sin(angle_rad)

        # Colore dinamico della lancetta
        if perc < 0.4:
            color = QtGui.QColor("green")
        elif perc < 0.7:
            color = QtGui.QColor("orange")
        else:
            color = QtGui.QColor("red")

        # 💡 Glow attorno alla lancetta
        pen_glow = QtGui.QPen(color)
        pen_glow.setWidth(10)
        pen_glow.setColor(QtGui.QColor(color.red(), color.green(), color.blue(), 60))
        painter.setPen(pen_glow)
        painter.drawLine(cx, cy, int(x2), int(y2))

        # 🧭 Lancetta nitida sopra
        painter.setPen(QtGui.QPen(color, 4))
        painter.drawLine(cx, cy, int(x2), int(y2))

        # Tacche e numeri
        for i in range(self.steps + 1):
            step_perc = i / self.steps
            val = int(self.max_val * step_perc)
            deg = 180 + step_perc * self.angle_span
            rad = math.radians(deg)

            # Tacca
            x1 = cx + 75 * math.cos(rad)
            y1 = cy + 75 * math.sin(rad)
            x2 = cx + 70 * math.cos(rad)
            y2 = cy + 70 * math.sin(rad)
            painter.setPen(QtGui.QPen(QtGui.QColor("#888"), 2))
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))

            # Numero
            xt = cx + 92 * math.cos(rad)
            yt = cy + 92 * math.sin(rad)
            painter.setFont(QtGui.QFont("Arial", 8))
            painter.setPen(QtGui.QColor("#aaa"))
            painter.drawText(int(xt - 10), int(yt + 5), f"{val}")

        # Etichetta e valore in basso
        text = f"{self.label}\n{int(self.value)} {self.unit}"
        painter.setFont(QtGui.QFont("DS-Digital", 18))
        painter.setPen(QtGui.QColor("white"))
        text_rect = QtCore.QRectF(rect)
        text_rect.moveTop(rect.center().y() + 5)
        painter.drawText(text_rect, QtCore.Qt.AlignHCenter, text)