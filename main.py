import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QPainter, QImage, QColor
from PyQt5.QtCore import Qt

class MandelbrotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.zoom = 1.0
        self.center_x = -0.5
        self.center_y = 0
        self.max_iter = 100
        self.setMinimumSize(800, 600)

    def paintEvent(self, event):
        painter = QPainter(self)
        image = self.generate_mandelbrot()
        painter.drawImage(0, 0, image)

    def generate_mandelbrot(self):
        width = self.width()
        height = self.height()
        
        x = np.linspace(self.center_x - 2.0/self.zoom, 
                        self.center_x + 2.0/self.zoom, 
                        width)
        y = np.linspace(self.center_y - 1.5/self.zoom, 
                        self.center_y + 1.5/self.zoom, 
                        height)
        
        c = x[:, np.newaxis] + 1j * y[np.newaxis, :]
        z = np.zeros_like(c)
        divtime = self.max_iter + np.zeros(z.shape, dtype=int)

        for i in range(self.max_iter):
            z = z**2 + c
            diverge = z*np.conj(z) > 2**2
            div_now = diverge & (divtime == self.max_iter)
            divtime[div_now] = i
            z[diverge] = 2

        image = QImage(width, height, QImage.Format_RGB32)
        for x in range(width):
            for y in range(height):
                value = divtime[x, y]
                if value == self.max_iter:
                    color = QColor(0, 0, 0)
                else:
                    hue = (value % 256) / 255.0
                    color = QColor.fromHsvF(hue, 1.0, 1.0 if value < self.max_iter else 0)
                image.setPixelColor(x, y, color)
        
        return image

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.zoom *= 2.0
        elif event.button() == Qt.RightButton:
            self.zoom /= 2.0
            
        # Update center based on click position
        width = self.width()
        height = self.height()
        x_ratio = (event.x() - width/2) / (width/2)
        y_ratio = (event.y() - height/2) / (height/2)
        
        self.center_x += x_ratio / self.zoom
        self.center_y += y_ratio / self.zoom
        
        self.update()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mandelbrot Set Viewer")
        self.mandelbrot = MandelbrotWidget()
        self.setCentralWidget(self.mandelbrot)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
