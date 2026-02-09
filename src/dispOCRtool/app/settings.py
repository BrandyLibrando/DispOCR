"""
settings.py
Creates persistent settings.
Used for the save directory and the setup settings
that are helpful when persistent (e.g., log frequency).
"""

import os
from PySide6.QtCore import QObject, QSettings, QUrl, QStandardPaths
from PySide6.QtCore import Slot, Signal


class AppSettings(QObject):
    settingsUpdated = Signal()
    daiSettingsUpdated = Signal()

    def __init__(self, org_name="BrandyLibrando", app_name="DispOCR"):
        super().__init__()
        self._settings = QSettings(org_name, app_name)


    ## General Settings
    @Slot(float)
    def setLogFrequency(self, value):
        self._settings.setValue("ui/general/logFrequency", value)
        self.settingsUpdated.emit()
    @Slot(result=float)
    def getLogFrequency(self):
        return self._settings.value("ui/general/logFrequency", 1, type=float)

    @Slot(bool)
    def setEnableTextCorrection(self, value=True):
        self._settings.setValue("ui/general/textCorrect", value)
        self.settingsUpdated.emit()
    @Slot(result=bool)
    def getEnableTextCorrection(self):
        return self._settings.value("ui/general/textCorrect", False, type=bool)


    ## Control System Settings
    @Slot(bool)
    def setEnableController(self, value=True):
        self._settings.setValue("ui/control/enableController", value)
        self.settingsUpdated.emit()
    @Slot(result=bool)
    def getEnableController(self):
        return self._settings.value("ui/control/enableController", False, type=bool)

    @Slot(str)
    def setControllerValue(self, value):
        self._settings.setValue("ui/control/controlValue", value)
        self.settingsUpdated.emit()
    @Slot(result=str)
    def getControllerValue(self):
        return self._settings.value("ui/control/controlValue", "", type=str)

    @Slot(bool)
    def setEnableScriptAlt(self, value=True):
        self._settings.setValue("ui/control/enableFailScript", value)
        self.settingsUpdated.emit()
    @Slot(result=bool)
    def getEnableScriptAlt(self):
        return self._settings.value("ui/control/enableFailScript", False, type=bool)


    ## DepthAi Camera Settings
    @Slot(bool)
    def setEnableManualExposure(self, value=True):
        self._settings.setValue("ui/dai/manualExposure", value)
        self.settingsUpdated.emit()
        self.daiSettingsUpdated.emit()
    @Slot(result=bool)
    def getEnableManualExposure(self):
        return self._settings.value("ui/dai/manualExposure", False, type=bool)

    @Slot(bool)
    def setEnableManualFocus(self, value=True):
        self._settings.setValue("ui/dai/manualFocus", value)
        self.settingsUpdated.emit()
        self.daiSettingsUpdated.emit()
    @Slot(result=bool)
    def getEnableManualFocus(self):
        return self._settings.value("ui/dai/manualFocus", False, type=bool)

    @Slot(bool)
    def setEnableManualWhiteBalance(self, value=True):
        self._settings.setValue("ui/dai/manualWhiteBalance", value)
        self.settingsUpdated.emit()
        self.daiSettingsUpdated.emit()
    @Slot(result=bool)
    def getEnableManualWhiteBalance(self):
        return self._settings.value("ui/dai/manualWhiteBalance", False, type=bool)


    @Slot(int)
    def setManualExposure(self, value):
        self._settings.setValue("ui/dai/values/manualExposure", value)
        self.settingsUpdated.emit()
        self.daiSettingsUpdated.emit()
    @Slot(result=int)
    def getManualExposure(self):
        return self._settings.value("ui/dai/values/manualExposure", 16500, type=int)

    @Slot(int)
    def setManualIso(self, value):
        self._settings.setValue("ui/dai/values/manualIso", value)
        self.settingsUpdated.emit()
        self.daiSettingsUpdated.emit()
    @Slot(result=int)
    def getManualIso(self):
        return self._settings.value("ui/dai/values/manualIso", 800, type=int)

    @Slot(int)
    def setManualFocus(self, value):
        self._settings.setValue("ui/dai/values/manualFocus", value)
        self.settingsUpdated.emit()
        self.daiSettingsUpdated.emit()
    @Slot(result=int)
    def getManualFocus(self):
        return self._settings.value("ui/dai/values/manualFocus", 128, type=int)

    @Slot(int)
    def setManualWhiteBalance(self, value):
        self._settings.setValue("ui/dai/values/manualWhiteBalance", value)
        self.settingsUpdated.emit()
        self.daiSettingsUpdated.emit()
    @Slot(result=int)
    def getManualWhiteBalance(self):
        return self._settings.value("ui/dai/values/manualWhiteBalance", 7000, type=int)


    ## Directory Handlers
    @Slot(QUrl)
    def setSaveDir(self, url):
        self._settings.setValue("paths/saveDir", url)
        self.settingsUpdated.emit()
    @Slot()
    def verifySaveDir(self):
        saveDir = self.getSaveDir()
        if not os.path.exists(saveDir) or not os.path.isdir(saveDir):
            self._settings.setValue("paths/saveDir", QUrl.fromLocalFile(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.HomeLocation)))
            self.settingsUpdated.emit()
    @Slot(result=QUrl)
    def getSaveDir(self):
        return self._settings.value("paths/saveDir", QUrl.fromLocalFile(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.HomeLocation)), type=QUrl)
    
    @Slot(QUrl)
    def setScriptPath(self, url):
        self._settings.setValue("paths/scriptPath", url)
        self.settingsUpdated.emit()
    @Slot()
    def verifyScriptPath(self):
        scriptPath = self.getScriptPath()
        if not os.path.exists(scriptPath) or not os.path.isfile(scriptPath):
            self._settings.setValue("paths/scriptPath", QUrl.fromLocalFile(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.HomeLocation)))
            self.settingsUpdated.emit()
    @Slot(result=QUrl)
    def getScriptPath(self):
        return self._settings.value("paths/scriptPath", QUrl.fromLocalFile(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.HomeLocation)), type=QUrl)

    @Slot(QUrl)
    def setScriptPathAlt(self, url):
        self._settings.setValue("paths/scriptPathAlt", url)
        self.settingsUpdated.emit()
    @Slot()
    def verifyScriptPathAlt(self):
        scriptPath = self.getScriptPathAlt()
        if not os.path.exists(scriptPath) or not os.path.isfile(scriptPath):
            self._settings.setValue("paths/scriptPathAlt", QUrl.fromLocalFile(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.HomeLocation)))
            self.settingsUpdated.emit()
    @Slot(result=QUrl)
    def getScriptPathAlt(self):
        return self._settings.value("paths/scriptPathAlt", QUrl.fromLocalFile(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.HomeLocation)), type=QUrl)

    @Slot()
    def verifyPaths(self):
        self.verifySaveDir()
        self.verifyScriptPath()
        self.verifyScriptPathAlt()


AppConfigs = AppSettings()  # For singleton pattern
