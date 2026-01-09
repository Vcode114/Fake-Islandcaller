import sys
import os
import subprocess
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget
from PyQt5.QtGui import QIcon, QPixmap, QImage, QColor
from PyQt5.QtCore import Qt, QSize

class CameraButton(QWidget):
    def __init__(self, icon_path: str = "Icon.png", size: int = 96):
        super().__init__()
        self.icon_path = Path(icon_path)
        self.size = size

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        btn = QPushButton('', self)
        class DraggableButton(QPushButton):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self._drag_offset = None
                self._press_global = None
                self._moved = False

            def mousePressEvent(self, e):
                if e.button() == Qt.LeftButton and self.parentWidget() is not None:
                    self._press_global = e.globalPos()
                    self._drag_offset = e.globalPos() - self.parentWidget().frameGeometry().topLeft()
                    self._moved = False
                super().mousePressEvent(e)

            def mouseMoveEvent(self, e):
                if self._press_global is not None and (e.buttons() & Qt.LeftButton) and self.parentWidget() is not None:
                    # if moved beyond system drag threshold, treat as drag and move window
                    if (e.globalPos() - self._press_global).manhattanLength() >= QApplication.startDragDistance():
                        self._moved = True
                        self.parentWidget().move(e.globalPos() - self._drag_offset)
                else:
                    super().mouseMoveEvent(e)

            def mouseReleaseEvent(self, e):
                if self._moved:
                    self._drag_offset = None
                    self._press_global = None
                    self._moved = False
                    return
                self._drag_offset = None
                self._press_global = None
                self._moved = False
                super().mouseReleaseEvent(e)

        btn = DraggableButton('', self)
        pix = QPixmap(str(self.icon_path)) if self.icon_path.exists() else QPixmap()
        if not pix.isNull():
            img = pix.toImage().convertToFormat(QImage.Format_ARGB32)
            w = img.width()
            h = img.height()
            for yy in range(h):
                for xx in range(w):
                    col = QColor(img.pixel(xx, yy))
                    if col.alpha() == 255 and col.red() >= 250 and col.green() >= 250 and col.blue() >= 250:
                        col.setAlpha(0)
                        img.setPixelColor(xx, yy, col)
            pix = QPixmap.fromImage(img)
            icon = QIcon(pix)
            btn.setIcon(icon)
            btn.setIconSize(QSize(self.size, self.size))
        btn.setFlat(True)
        btn.setStyleSheet("QPushButton{border: none; background: transparent;}")
        btn.clicked.connect(self.launch_camera)
        btn.resize(self.size, self.size)

        self.resize(self.size, self.size)
        screen = QApplication.primaryScreen().availableGeometry()
        x = screen.right() - self.size - 12
        y = screen.bottom() - self.size - 60
        self.move(x, y)

    def launch_camera(self):
        try:
            subprocess.run('start microsoft.windows.camera:', shell=True, check=False)
        except Exception:
            os.system('start microsoft.windows.camera:')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    here = Path(__file__).parent
    icon_file = here / 'Icon.png'
    w = CameraButton(icon_path=str(icon_file), size=96)
    w.show()
    sys.exit(app.exec_())
