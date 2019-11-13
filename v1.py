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

        self.data = []

    def _initUI(self):
        self.canvas = Canvas()


        # btns
        load = QtWidgets.QPushButton()
        load.setText('Load')
        load.clicked.connect(self.load)
        load_result = QtWidgets.QPushButton()
        load_result.setText('Load Result')
        load_result.clicked.connect(self.load_result)
        data_input = QtWidgets.QLineEdit(self)
        data_input.setFixedWidth(80)
        data_input.textChanged.connect(self.data_input_change)
        self.data_input = data_input
        previous_data = QtWidgets.QPushButton()
        previous_data.setText('Next Data')
        previous_data.clicked.connect(self.previous_data)
        next_data = QtWidgets.QPushButton()
        next_data.setText('Next Data')
        next_data.clicked.connect(self.next_data)

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
        btns.addWidget(data_input)
        btns.addWidget(previous_data)
        btns.addWidget(next_data)

        btns2 = QtWidgets.QHBoxLayout()
        btns2.addWidget(run)
        btns2.addWidget(save)
        btns2.addWidget(clear)

        # VBox Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addLayout(btns)
        layout.addLayout(btns2)
        self.setLayout(layout)

    def data_input_change(self):
        text = self.data_input.text()
        if text:
            data_i = int(text)
            if data_i >= 0 and data_i < len(self.data):
                self.data_i = data_i
                self.draw_data()

    def previous_data(self):
        if self.data_i > 1:
            self.data_i -= 1
            self.data_input.setText(str(self.data_i))
            self.draw_data()

    def next_data(self):
        if self.data_i < len(self.data) - 1:
            self.data_i += 1
            self.data_input.setText(str(self.data_i))
            self.draw_data()

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
        self.data = data
        self.data_i = 0
        self.data_input.setText(str(self.data_i))

        self.draw_data()

    def draw_data(self):
        print(self.data[self.data_i])
        self.clear()
        for p in self.data[self.data_i][1:]:
            self.canvas.draw_point(*p)
            self.canvas.data.append(p)
        self.run()

    def run(self):
        data = sorted(self.canvas.data, key=lambda x: (x[0], x[1]))
        self.canvas.data = data
        edges = self.voronoi_temp(data)

        # print(len(edges), 'edges')
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

    def voronoi(self, points):
        if len(points) == 1:
            return []

        l = len(points) // 2
        l_points = points[:l]
        r_points = points[l:]
        l_lines = self.voronoi(l_points)
        r_lines = self.voronoi(r_points)

        # merge
        edges = [get_edge(l_points[-1], r_points[0])]
        lines = l_lines + r_lines + edges

        return lines

    def voronoi_temp(self, points):
        del_i = -1
        for i, p1 in enumerate(points):
            for j, p2 in enumerate(points):
                if i == j:
                    continue
                if p1 == p2:
                    del_i = i
        if del_i != -1:
            points.pop(del_i)

        if len(points) == 1:
            return []
        elif len(points) == 2:
            return [get_edge(points[0], points[1])]
        elif len(points) == 3:
            funcs = [
                get_func(points[0], points[1]),
                get_func(points[1], points[2]),
                get_func(points[0], points[2])
            ]

            edge_lens = [f[3] for f in funcs]
            lens = sorted(edge_lens)
            ctr = lens[0] ** 2 + lens[1] ** 2 > lens[2] ** 2
            # true is sharp, false is right/obtuse

            # calc mid
            if funcs[0][0] == funcs[1][0]: # 平行
                edges = [get_edge(points[0], points[1]), get_edge(points[1], points[2])]
            else:
                mid_x = (funcs[1][1] - funcs[0][1]) / (funcs[0][0] - funcs[1][0])
                mid_y = mid_x * funcs[0][0] + funcs[0][1]
                mid = (mid_x, mid_y)

                calc_len = lambda p1, p2: ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2) ** 0.5
                directions = ['out', 'out', 'out']
                if not ctr: # if not sharp
                    longest = max([f[3] for f in funcs])
                    longest_i = [f[3] for f in funcs].index(longest)
                    directions[longest_i] = 'in'
                print(directions)

                dots = [points[2], points[0], points[1]]
                edges = [get_edge_temp(f[0], f[1], mid, f[2], dots[i], directions[i]) for i, f in enumerate(funcs)]

            return edges
        else:
            # Not implemented
            return []

def get_func(p1, p2):
    calc_mid = lambda p1, p2: ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)
    calc_slope = lambda p1, p2: (p2[1] - p1[1]) / (p2[0] - p1[0])
    x, y = calc_mid(p1, p2)
    l_mid = (x, y)
    if p1[0] == p2[0]:
        a = 0
        b = y - a * x
    elif p1[1] == p2[1]:
        a = 1340
        b = (p1[0] + p2[0]) / 2
    else:
        a = -1 / calc_slope(p1, p2)
        b = y - a * x

    calc_len = lambda p1, p2: ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2) ** 0.5
    edge_len = calc_len(p1, p2)

    print(p1, p2)
    print('funcs', a, b)

    return a, b, l_mid, edge_len

def get_edge(p1, p2, a=None, b=None):
    # get ax + b
    print(p1, p2)
    res = get_func(p1, p2)
    a = res[0]
    b = res[1]
    print('ab', a, b)

    # get points on edge
    edges = []
    if a == 1340:
        t_flag = b
        b_flag = b
    elif a != 0:
        t_flag = -b // a            # y = 0
        b_flag = (600 - b) // a     # y = 600
    else:
        t_flag = -1
        b_flag = -1
    l_flag = b                  # x = 0
    r_flag = 600 * a + b        # x = 600

    if len(edges) < 2 and 0 <= t_flag and t_flag <= 600:
        edges.append((t_flag, 0))
    if len(edges) < 2 and 0 < b_flag and b_flag < 600:
        edges.append((b_flag, 600))
    if len(edges) < 2 and 0 <= l_flag and l_flag <= 600:
        edges.append((0, l_flag))
    if len(edges) < 2 and 0 < r_flag and r_flag < 600:
        edges.append((600, r_flag))

    return edges

def get_edge_temp(a, b, mid, l_mid, dot, direction):
    edges = []
    if a == 1340:
        t_flag = b
        b_flag = b
    elif a != 0:
        t_flag = -b // a            # y = 0
        b_flag = (600 - b) // a     # y = 600
    else:
        t_flag = -1
        b_flag = -1
    l_flag = b                  # x = 0
    r_flag = 600 * a + b        # x = 600

    print('flags', t_flag, b_flag, l_flag, r_flag)

    if 0 <= t_flag and t_flag <= 600:
        edges.append((t_flag, 0))
    if 0 <= b_flag and b_flag <= 600:
        edges.append((b_flag, 600))
    if len(edges) < 2 and 0 < l_flag and l_flag < 600:
        edges.append((0, l_flag))
    if len(edges) < 2 and 0 < r_flag and r_flag < 600:
        edges.append((600, r_flag))

    print(edges)

    calc_len = lambda p1, p2: ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2) ** 0.5
    if calc_len(edges[0], l_mid) == calc_len(edges[0], mid): # 直角
        print('直')
        print(a, b, dot)
        if calc_len(edges[0], dot) > calc_len(edges[0], mid):
            out_i = 0
            in_i = 1
        else:
            out_i = 1
            in_i = 0
    elif calc_len(edges[0], l_mid) > calc_len(edges[0], mid):
        out_i = 0
        in_i = 1
    else:
        out_i = 1
        in_i = 0

    if direction == 'out':
        edges[out_i] = mid
    else:
        edges[in_i] = mid

    return edges

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    canvas_app = App()
    canvas_app.show()
    app.exec_()
