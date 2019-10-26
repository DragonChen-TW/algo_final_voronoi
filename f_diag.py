import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle('File Dialog')
        self.setGeometry(750, 150, 600, 600)
        self.show()

    def initUI(self):
        fileName, _ = QFileDialog.getOpenFileName(self)
        # fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    file_app = App()
    sys.exit(app.exec_())
