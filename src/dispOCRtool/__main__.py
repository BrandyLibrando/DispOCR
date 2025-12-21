import sys
from pathlib import Path
import random, time
import numpy as np
import cv2

# import PySide6.QtMultimedia
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from PySide6.QtGui import QImage
from PySide6.QtCore import Slot, Signal, Property
from PySide6.QtCore import QObject, QTimer, QUrl, QThread, QPermission, QCameraPermission
from PySide6.QtQuick import QQuickImageProvider, QQuickView


class Bridge(QObject):
    ## INITIAL VALUES
    def __init__(self):
        QObject.__init__(self)
        self._data = "Hello from Python!"

    ## SIGNALS
    dataChanged = Signal()

    ## GETTER-SETTER
    def getData(self):
        return self._data
    def setData(self, value):
        if self._data != value:
            self._data = value
            self.dataChanged.emit()

    ## EXPOSED PROPERTIES
    data = Property(str, getData, setData, notify=dataChanged)

    ## EXPOSED SLOTS
    @Slot(str)
    def updateData(self, new_data):
        self.setData(new_data)


class NumpyImageProvider(QQuickImageProvider):
    def __init__(self):
        super().__init__(QQuickImageProvider.Image)
        self.image = None

    def set_array(self, array: np.ndarray):
        """Convert NumPy array to QImage and store it."""
        if array.ndim == 2:  # Grayscale
            h, w = array.shape
            qimg = QImage(array.data, w, h, w, QImage.Format_Grayscale8)
        elif array.ndim == 3 and array.shape[2] == 3:  # RGB
            h, w, _ = array.shape
            qimg = QImage(array.data, w, h, 3 * w, QImage.Format_RGB888)
        elif array.ndim == 3 and array.shape[2] == 4:  # RGBA
            h, w, _ = array.shape
            qimg = QImage(array.data, w, h, 4 * w, QImage.Format_RGBA8888)
        else:
            raise ValueError("Unsupported array shape for QImage conversion.")
        self.image = qimg.copy()  # Copy to avoid referencing freed memory

    def requestImage(self, id, size, requestedSize):
        return self.image if self.image else (QImage(), (0, 0))


class ThreadCamera(QThread):
    updateFrame = Signal(QImage)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)

    def run(self):
        self.cap = cv2.VideoCapture(0)
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                img = QImage("./images/network.png")
                self.updateFrame.emit(img)
            color_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = QImage(color_frame.data, color_frame.shape[1], color_frame.shape[0], QImage.Format_RGB888)
            self.updateFrame.emit(img)


class ImageProvider(QQuickImageProvider):
    imageChanged = Signal(QImage)

    def __init__(self):
        super(ImageProvider, self).__init__(QQuickImageProvider.Image)

        self.cam = ThreadCamera()
        self.cam.updateFrame.connect(self.update_image)
        self.image = None

    def requestImage(self, id, size, requestedSize):
        if self.image:
            img = self.image
        else:
            img = QImage(600, 500, QImage.Format_RGBA8888)
            img.fill("#4CAF50")

        return img


    @Slot()
    def update_image(self, img):
        self.imageChanged.emit(img)
        self.image = img

    @Slot()
    def start(self):
        print("Starting...")
        self.cam.start()

    @Slot()
    def killThread(self):
        print("Finishing...")
        try:
            self.cam.cap.release()
        except:
            pass


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    ## Create a sample NumPy RGB image
    # h, w = 10, 10
    # array = np.zeros((h, w, 3), dtype=np.uint8)
    # array[:, :] = [
    #     random.randint(0, 255),
    #     random.randint(0, 255),
    #     random.randint(0, 255)]

    ## # Create image provider and set array
    # provider = NumpyImageProvider()
    # provider.set_array(array)

    ##############################################
    ## PY-QML INTEG
    ##############################################
    bridge = Bridge()

    ## Expose Python object to QML
    # engine.rootContext().engine().addImageProvider("numpy", provider)
    myImageProvider = ImageProvider()

    engine.rootContext().setContextProperty("bridge", bridge)
    engine.rootContext().setContextProperty("myImageProvider", myImageProvider)

    engine.addImageProvider("MyImageProvider", myImageProvider)


    ##############################################
    ## LOADING OF QML FILE FOR APP
    ##############################################
    # qml_file = Path(__file__).resolve().parent / "tester.qml"
    qml_file = Path(__file__).resolve().parent / "main.qml"

    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
