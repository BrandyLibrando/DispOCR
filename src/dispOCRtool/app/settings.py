"""
settings.py
Creates persistent settings.
Used for
"""

from PySide6.QtCore import QObject, Slot, QSettings, QUrl, QStandardPaths


class AppSettings(QObject):
    def __init__(self, org_name="BrandyLibrando", app_name="DispOCR"):
        super().__init__()
        self._settings = QSettings(org_name, app_name)

    ## Checkboxes
    @Slot(bool)
    def setEnableController(self, value=True):
        self._settings.setValue("ui/rememberMe", value)

    @Slot(result=bool)
    def getEnableController(self):
        return self._settings.value("ui/rememberMe", False, type=bool)


    ## Log File Save Directory
    @Slot(QUrl)
    def setSaveDir(self, url):
        self._settings.setValue("paths/saveDir", url)

    @Slot(result=QUrl)
    def getSaveDir(self):
        return self._settings.value("paths/saveDir", QUrl.fromLocalFile(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.HomeLocation)), type=QUrl)
