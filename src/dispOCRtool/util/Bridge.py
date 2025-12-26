from PySide6.QtCore import Slot, Signal, Property, QObject


## StringBridge() <= QObject
## - Bidirectional model for passing strings between QML and Python

class StringBridge(QObject):
    def __init__(self, data:str=None):
        QObject.__init__(self)
        self._data = data

    ## SIGNALS
    dataChanged = Signal()

    ## GETTER-SETTER
    def getData(self):
        return self._data
    def putData(self, value):
        if self._data != value:
            self._data = value
            self.dataChanged.emit()

    ## EXPOSED PROPERTIES
    data = Property(str, getData, putData, notify=dataChanged)

    ## EXPOSED SLOTS/METHODS
    @Slot(str)
    def setData(self, new_data):
        self.putData(new_data)

class ListBridge(QObject):
    def __init__(self, data:list=None):
        QObject.__init__(self)
        self._data = data

    ## SIGNALS
    dataChanged = Signal()

    ## GETTER-SETTER
    def getData(self):
        return self._data
    def putData(self, value):
        if self._data != value:
            self._data = value
            self.dataChanged.emit()

    ## EXPOSED PROPERTIES
    data = Property(list, getData, putData, notify=dataChanged)

    ## EXPOSED SLOTS/METHODS
    @Slot(str)
    def setData(self, new_data):
        self.putData(new_data)

    @Slot()
    def size(self):
        return self._data.__len__()
