"""
CroppedImageRenderer.py
Contains rudimentary QQuickImageProvider class,
used for displaying cropped version of image.
"""

from PySide6.QtGui import QImage
from PySide6.QtQuick import QQuickImageProvider


class CroppedImageProvider(QQuickImageProvider):
    def __init__(self):
        super(CroppedImageProvider, self).__init__(QQuickImageProvider.Image)
        self.name = "CroppedImageProvider"

        self.image = None


    def requestImage(self, id, size, requestedSize):
        if self.image:
            img = self.image
        else:
            img = QImage(640, 480, QImage.Format_RGBA8888)
            img.fill("#00BCD4")

        return img

    def setCroppedImage(self, img):
        self.image = img
