import sys
from pathlib import Path
import random, time
import numpy as np

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


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Create a sample NumPy RGB image
    h, w = 10, 10
    array = np.zeros((h, w, 3), dtype=np.uint8)
    array[:, :] = [255, 0, 0]  # Red image

    # Create image provider and set array
    provider = NumpyImageProvider()
    provider.set_array(array)

    ##############################################
    ## PY-QML INTEG
    ##############################################
    bridge = Bridge()

    # Expose Python object to QML
    engine.rootContext().engine().addImageProvider("numpy", provider)
    engine.rootContext().setContextProperty("bridge", bridge)


    ##############################################
    ## LOADING OF QML FILE FOR APP
    ##############################################
    # qml_file = Path(__file__).resolve().parent / "tester.qml"
    qml_file = Path(__file__).resolve().parent / "main.qml"

    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
