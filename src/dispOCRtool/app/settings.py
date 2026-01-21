"""
settings.py
Creates persistent settings.
Used for the save directory and the setup settings
that are helpful when persistent (e.g., log frequency).
"""

from PySide6.QtCore import QObject, Slot, QSettings, QUrl, QStandardPaths


class AppSettings(QObject):
    def __init__(self, org_name="BrandyLibrando", app_name="DispOCR"):
        super().__init__()
        self._settings = QSettings(org_name, app_name)

    ## App Settings
    # General Settings
    @Slot(float)
    def setLogFrequency(self, value):
        self._settings.setValue("ui/general/logFrequency", value)
    @Slot(result=float)
    def getLogFrequency(self):
        return self._settings.value("ui/general/logFrequency", 1, type=float)

    @Slot(bool)
    def setEnableTextCorrection(self, value=True):
        self._settings.setValue("ui/general/textCorrect", value)
    @Slot(result=bool)
    def getEnableTextCorrection(self):
        return self._settings.value("ui/general/textCorrect", False, type=bool)


    # Control System Settings
    @Slot(bool)
    def setEnableController(self, value=True):
        self._settings.setValue("ui/control/enableController", value)
    @Slot(result=bool)
    def getEnableController(self):
        return self._settings.value("ui/control/enableController", False, type=bool)

    @Slot(str)
    def setControllerValue(self, value):
        self._settings.setValue("ui/control/controlValue", value)
    @Slot(result=str)
    def getControllerValue(self):
        return self._settings.value("ui/control/controlValue", "", type=str)


    # DepthAi Camera Settings
    # @Slot(bool)
    # def setEnableManualAll(self, value=True):
    #     self._settings.setValue("ui/dai/manualSettings", value)
    # @Slot(result=bool)
    # def getEnableManualAll(self):
    #     return self._settings.value("ui/dai/manualSettings", False, type=bool)

    @Slot(bool)
    def setEnableManualExposure(self, value=True):
        self._settings.setValue("ui/dai/manualExposure", value)
    @Slot(result=bool)
    def getEnableManualExposure(self):
        return self._settings.value("ui/dai/manualExposure", False, type=bool)

    @Slot(bool)
    def setEnableManualIso(self, value=True):
        self._settings.setValue("ui/dai/manualIso", value)
    @Slot(result=bool)
    def getEnableManualIso(self):
        return self._settings.value("ui/dai/manualIso", False, type=bool)

    @Slot(bool)
    def setEnableManualFocus(self, value=True):
        self._settings.setValue("ui/dai/manualFocus", value)
    @Slot(result=bool)
    def getEnableManualFocus(self):
        return self._settings.value("ui/dai/manualFocus", False, type=bool)


    @Slot(int)
    def setManualExposure(self, value):
        self._settings.setValue("ui/dai/values/manualExposure", value)
    @Slot(result=int)
    def getManualExposure(self):
        return self._settings.value("ui/dai/values/manualExposure", 16500, type=int)

    @Slot(int)
    def setManualIso(self, value):
        self._settings.setValue("ui/dai/values/manualIso", value)
    @Slot(result=int)
    def getManualIso(self):
        return self._settings.value("ui/dai/values/manualIso", 800, type=int)

    @Slot(int)
    def setManualFocus(self, value):
        self._settings.setValue("ui/dai/values/manualFocus", value)
    @Slot(result=int)
    def getManualFocus(self):
        return self._settings.value("ui/dai/values/manualFocus", 128, type=int)


    ## Log File Save Directory
    @Slot(QUrl)
    def setSaveDir(self, url):
        self._settings.setValue("paths/saveDir", url)

    @Slot(result=QUrl)
    def getSaveDir(self):
        return self._settings.value("paths/saveDir", QUrl.fromLocalFile(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.HomeLocation)), type=QUrl)
