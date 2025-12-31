"""
NumpyQImageRenderer.py
Class for rendering numpy matrices (representing
image files) to QImages that can be passed to
image providers for display.
"""

import numpy as np
from PySide6.QtGui import QImage
from PySide6.QtQuick import QQuickImageProvider


## NumpyImageProvider
## - For rendering images stored as numpy arrays in QML as QImages

## Sample use to display blue image from numpy array to QML
# /main.py
#   h, w = 10, 10
#   array = np.zeros((h, w, 3), dtype=np.uint8)
#   array[:, :] = [ 0, 188, 212 ]
#   provider = NumpyImageProvider()
#   provider.set_array(array)
#   ...
#   engine.rootContext().engine().addImageProvider("numpy", provider)
#
# /main.qml
#   Image {
#       id: blueImage
#       anchors.fill: parent
#       fillMode: Image.PreserveAspectFit
#       cache: false
#
#       source: "image://numpy/test"
#   }


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
