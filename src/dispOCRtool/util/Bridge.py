"""
Bridge.py
Contains class for bidirectional models.
Intended for lists but a list can be used as a wrapper for a single object (bad practice though).
"""

from PySide6.QtCore import Slot, Signal, Property, QObject


class ListBridge(QObject):
    def __init__(self, data:list=None):
        QObject.__init__(self)
        self._data = data

    ## Internal use
    def putData(self, value):
        if self._data != value:
            self._data = value
            self.dataChanged.emit(self._data)


    ## EXPOSED SLOTS/METHODS
    @Slot(list)
    def setData(self, new_data):
        self.putData(new_data)

    @Slot(result=list)
    def getData(self):
        return self._data

    @Slot(int)
    def size(self):
        return self._data.__len__()

    ## SIGNALS
    dataChanged = Signal(list)

    ## EXPOSED PROPERTIES
    data = Property(list, getData, putData, notify=dataChanged)

