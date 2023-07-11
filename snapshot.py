import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QDesktopWidget
from PyQt5.QtGui import QPixmap, QPainter, QPen, QBrush, QColor, QGuiApplication
from PyQt5.QtCore import Qt, QPoint, QRect


class ScreenshotUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('截图工具')
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        
        self.setStyleSheet('''background-color:black; ''')
        self.setWindowOpacity(0.2)
        desktop_rect = QDesktopWidget().screenGeometry()
        self.setGeometry(desktop_rect)
        self.setCursor(Qt.CrossCursor)
        
        self.setMouseTracking(True)
        #self.setGeometry(QGuiApplication.primaryScreen().geometry())
        #self.label = QLabel(self)
        #self.label.setPixmap(QGuiApplication.primaryScreen().grabWindow(0))
        #self.label.show()
        self.start_pos = None
        self.end_pos = None
        self.drawing = False

        self.btn_ok = QPushButton('确认', self)
        self.btn_ok.clicked.connect(self.save)
        self.btn_ok.hide()

        self.btn_cancel = QPushButton('取消', self)
        self.btn_cancel.clicked.connect(self.close)
        self.btn_cancel.hide()

    def paintEvent(self, event):
        if self.drawing:
            qp = QPainter(self)
            qp.setPen(QPen(QColor(0, 255, 0, 255), 3, Qt.SolidLine))
            brush = QBrush(Qt.white)
            qp.setBrush(brush)
            qp.drawRect(self.rect())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = event.pos()
            self.end_pos = event.pos()
            self.update()
            self.drawing = True

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.end_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.end_pos = event.pos()
            
            x = min(self.start_pos.x(), self.end_pos.x())
            y = min(self.start_pos.y(), self.end_pos.y())
            w = abs(self.start_pos.x() - self.end_pos.x())
            h = abs(self.start_pos.y() - self.end_pos.y())
            rect = QRect(x, y, w, h)
            pixmap = QGuiApplication.primaryScreen().grabWindow(0).copy(rect)
            clipboard = QApplication.clipboard()
            clipboard.setPixmap(pixmap)
            self.close()
            

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def save(self):
        x = min(self.start_pos.x(), self.end_pos.x())
        y = min(self.start_pos.y(), self.end_pos.y())
        w = abs(self.start_pos.x() - self.end_pos.x())
        h = abs(self.start_pos.y() - self.end_pos.y())
        rect = QRect(x, y, w, h)
        pixmap = QGuiApplication.primaryScreen().grabWindow(0).copy(rect)
        clipboard = QApplication.clipboard()
        clipboard.setPixmap(pixmap)
        self.close()

    def rect(self):
        x = min(self.start_pos.x(), self.end_pos.x())
        y = min(self.start_pos.y(), self.end_pos.y())
        w = abs(self.start_pos.x() - self.end_pos.x())
        h = abs(self.start_pos.y() - self.end_pos.y())
        return QRect(x, y, w, h)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ScreenshotUI()
    ex.show()
    sys.exit(app.exec_())