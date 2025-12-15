import QtQuick 2.0
import QtQuick.Controls 2.0
import QtQuick.Window 2.2
import QtMultimedia

Window {
    width: 640
    height: 480
    minimumWidth: 640
    minimumHeight: 480
    maximumWidth: 640
    maximumHeight: 480

    visible: true
    title: qsTr("DispOCR")

    Material.theme: Material.Light
    Material.primary: Material.BlueGrey
    Material.accent: Material.Indigo

    Item {
        width: 640
        height: 360

        MediaDevices {
            id: devices
        }

        CameraPermission {
            id: cameraPermission
        }

        CaptureSession {
            camera: Camera {
                id: camera
                cameraDevice: mediaDevices.defaultVideoInput
                focusMode: Camera.FocusModeAutoNear
                customFocusPoint: Qt.point(0.2, 0.2) // Focus near the top-left corner
            }
            videoOutput: videoOutput
        }

        VideoOutput {
            id: videoOutput
            anchors.fill: parent
        }
    }
}
