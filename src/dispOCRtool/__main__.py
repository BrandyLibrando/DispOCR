import sys
from pathlib import Path
import random, time

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

## TODO: FOR QML-PY INTEG
# QML_IMPORT_NAME = "io.qt.textproperties"
# QML_IMPORT_MAJOR_VERSION = 1

# @QmlElement
# class Bridge(QObject):
#     @Slot(QImage)
#     def capture(self, preview):
#         # process placeholder
#         print(type(preview))

# def request_permissions(app):
#     """
#     Request camera and location permissions at runtime.
#     Works on platforms that require explicit user consent.
#     """
#     # Camera permission
#     camera_perm = QCameraPermission()
#     status = app.checkPermission(camera_perm)
#     if status != Qt.PermissionStatus:
#         print("Requesting camera permission...")
#         app.requestPermission(camera_perm, lambda perm: print(f"Camera permission: {perm.status}"))


# class Camera_video(QQuickImageProvider):
#     imageChange = Signal(bool)
#     def __init__(self):
#         # super().__init__(QQuickImageProvider)
#         super().__init__(QQmlImageProviderBase.ImageType.Pixmap)
#         # Thread in charge of updating the image
#         self.th = ThreadQ(self)
#         self._model = "yolov8n.pt"
#         # updateModel.connect(self.get_model)
#         self.th.updateFrame.connect(self.updateImage)
#         # self.th.finished.connect(self.setlast)
#         # self.nowstatus = self.saveState()

#         # inpath = r"C:\Users\10696\Desktop\CV\ZouJiu1\Pytorch_YOLOV3\log\val"
#         # self.imagelist = [os.path.join(inpath, i) for i in os.listdir(inpath)]
#         self.pixmap = self.th.zeros

#     def requestPixmap(self, id="image_elementll", size=QSize(0, 0),
#                       requestedSize=QSize(0, 0)):
#         # w, h = 640, 600
#         # # image = np.zeros((w, h, 3)) * 255
#         # image = cv2.imread(np.random.choice(self.imagelist, 1)[0])
#         # image = cv2.resize(image, (w, h))
#         # h, w, ch = image.shape
#         # image = QImage(image.data, w, h, ch * w, QImage.Format_RGB888)
#         # pixmap = QPixmap.fromImage(image)
#         return self.pixmap

#     @Slot(QImage)
#     def updateImage(self, image):
#         self.pixmap = image
#         self.imageChange.emit(True)

#     @Slot(str, result=None)
#     def get_model(self, model):
#         self.th.model = model.replace("file:///", "")

#     @Slot(str, result=None)
#     def get_video(self, video):
#         self.th.video = video.replace("file:///", "")

#     @Slot(str, result=None)
#     def get_type(self, type):
#         self.th.input = type

#     @Slot(bool)
#     def get_checked(self, ischecked):
#         self.th.checked = ischecked

#     @Slot()
#     def start(self):
#         self.th.start()
#         # self.showFullScreen()

#     @Slot()
#     def stop(self):
#         self.th.image_stop = True
#         self.kill_thread()





if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    ##############################################
    ## PY-QML INTEG
    ##############################################
    bridge = Bridge()

    # Expose Python object to QML
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
