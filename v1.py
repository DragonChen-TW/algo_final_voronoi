import sys, json
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
#
import helper

class Canvas(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()

        # Pixmap and Painter
        pixmap = QtGui.QPixmap(600, 600)
        pixmap.fill(Qt.white)
        self.setPixmap(pixmap)
        self.painter = QtGui.QPainter(self.pixmap())
        p = self.painter.pen()
        p.setWidth(7)
        p.setColor(Qt.black)
        self.painter.setPen(p)

        # data and variable
        self.mode = 1 # can only draw point
        self.max_points = 10
        self.data = []

        # self.draw_line(100, 200, 400.5, 600)

    def mousePressEvent(self, e):
        if self.mode == 1 and len(self.data) < self.max_points:
            self.draw_point(e.x(), e.y())
            self.data.append((e.x(), e.y()))

    def draw_line(self, x1, y1, x2, y2):
        if self.mode == 1:
            self.mode = 2
            p = self.painter.pen()
            p.setWidth(4)
            self.painter.setPen(p)

        self.painter.drawLine(x1, y1, x2, y2)
        self.update()

    def draw_point(self, x, y):
        self.painter.drawPoint(x, y)
        self.update()

    def draw_edge(self, x1, y1, x2, y2):
        self.painter.drawLine(x1, y1, x2, y2)

    def draw_edges(self, edges):
        p = self.painter.pen()
        p.setWidth(2)
        p.setColor(Qt.red)
        self.painter.setPen(p)
        for edge in edges:
            if len(edge) == 2:
                self.draw_edge(*edge[0], *edge[1])
            else:
                self.draw_edge(*edge)

        # back
        p.setWidth(10)
        p.setColor(Qt.black)
        self.painter.setPen(p)

        self.update()

class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self._initUI()
        self.setGeometry(750, 150, 600, 600)
        self.setWindowTitle('Algorithm final - Voronoi')

    def _initUI(self):
        self.canvas = Canvas()


        # btns
        load = QtWidgets.QPushButton()
        load.setText('Load')
        load.clicked.connect(self.load)
        load_result = QtWidgets.QPushButton()
        load_result.setText('Load Result')
        load_result.clicked.connect(self.load_result)

        run = QtWidgets.QPushButton()
        run.setText('Run')
        run.clicked.connect(self.run)
        save = QtWidgets.QPushButton()
        save.setText('Save')
        save.clicked.connect(self.save)
        clear = QtWidgets.QPushButton()
        clear.setText('Clear')
        clear.clicked.connect(self.clear)

        btns = QtWidgets.QHBoxLayout()
        btns.addWidget(load)
        btns.addWidget(load_result)
        btns.addWidget(run)
        btns.addWidget(save)
        btns.addWidget(clear)

        # VBox Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addLayout(btns)
        self.setLayout(layout)

    def load_result(self):
        self.clear()
        f_name = helper.select_file(self)
        p_data, e_data = helper.from_result(f_name)

        for p in p_data:
            self.canvas.draw_point(*p)
        # for e in e_data:
        #     self.canvas.draw_edge(*e)
        self.canvas.draw_edges(e_data)

    def load(self):
        f_name = helper.select_file(self)
        data = helper.from_text(f_name)
        print(len(data))

    def run(self):
        data = sorted(self.canvas.data, key=lambda x: (x[0], x[1]))
        edges = voronoi(data)

        print(len(edges), 'edges')
        print('edges', edges)

        self.canvas.draw_edges(edges)

    def save(self):
        self.canvas.pixmap().save('output/plot.png', 'png')
        with open('output/dots.json', 'w') as f:
            json.dump(self.canvas.data, f)

    def clear(self):
        self.canvas.pixmap().fill(Qt.white)
        self.canvas.update()
        self.canvas.data = []

def get_edge(p1, p2):
    # get ax + b
    print(p1, p2)
    calc_mid = lambda p1, p2: ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)
    calc_slope = lambda p1, p2: (p2[1] - p1[1]) / (p2[0] - p1[0])
    x, y = calc_mid(p1, p2)
    a = -1 / calc_slope(p1, p2)
    b = y - a * x

    # get points on edge
    edges = []
    t_flag = -b // a            # y = 0
    b_flag = (600 - b) // a     # y = 600
    l_flag = b                  # x = 0
    r_flag = 600 * a + b        # x = 600

    if 0 <= t_flag and t_flag <= 600:
        edges.append((t_flag, 0))
    if 0 < b_flag and b_flag < 600:
        edges.append((b_flag, 600))
    if 0 <= l_flag and l_flag <= 600:
        edges.append((0, l_flag))
    if 0 < r_flag and r_flag < 600:
        edges.append((600, r_flag))

    return edges

def voronoi(points):
    if len(points) == 1:
        return []

    l = len(points) // 2
    l_points = points[:l]
    r_points = points[l:]
    l_lines = voronoi(l_points)
    r_lines = voronoi(r_points)

    # merge
    edges = [get_edge(l_points[-1], r_points[0])]
    lines = l_lines + r_lines + edges

    return lines


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    canvas_app = App()
    canvas_app.show()
    app.exec_()
