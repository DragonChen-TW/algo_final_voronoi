import sys, json
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt

class Canvas(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        pixmap = QtGui.QPixmap(600, 600)
        pixmap.fill(Qt.white)
        self.setPixmap(pixmap)

        self.last_x, self.last_y = None, None
        self.pen_color = QtGui.QColor('#000000')

        self.data = []

    def mousePressEvent(self, e):
        if len(self.data) < 3:
            painter = QtGui.QPainter(self.pixmap())
            p = painter.pen()
            p.setWidth(10)
            p.setColor(self.pen_color)
            painter.setPen(p)
            painter.drawPoint(e.x(), e.y())
            painter.end()
            self.update()

            self.data.append((e.x(), e.y()))

    # def mouseMoveEvent(self, e):
    #     if self.last_x is None: # First event.
    #         self.last_x = e.x()
    #         self.last_y = e.y()
    #         return # Ignore the first time.
    #
    #     painter = QtGui.QPainter(self.pixmap())
    #     p = painter.pen()
    #     p.setWidth(4)
    #     p.setColor(self.pen_color)
    #     painter.setPen(p)
    #     painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
    #     painter.end()
    #     self.update()
    #
    #     # Update the origin for next time.
    #     self.last_x = e.x()
    #     self.last_y = e.y()
    #
    # def mouseReleaseEvent(self, e):
    #     self.last_x = None
    #     self.last_y = None

class CanvasApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self._initUI()
        self.setGeometry(750, 150, 600, 600)

    def _initUI(self):
        self.canvas = Canvas()

        save = QtWidgets.QPushButton(self)
        save.setText('Save')
        save.clicked.connect(self.save)

        clear = QtWidgets.QPushButton(self)
        clear.setText('Cllear')
        clear.clicked.connect(self.clear)

        btns = QtWidgets.QHBoxLayout()
        btns.addWidget(save)
        btns.addWidget(clear)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.canvas, 1)
        layout.addLayout(btns)
        self.setLayout(layout)

    def save(self):
        self.canvas.pixmap().save('data/plot.png', 'png')
        with open('data/dots.json', 'w') as f:
            json.dump(self.canvas.data, f)

    def clear(self):
        self.canvas.pixmap().fill(Qt.white)
        self.canvas.update()
        self.canvas.data = []

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    canvas_app = CanvasApp()
    canvas_app.show()
    app.exec_()
