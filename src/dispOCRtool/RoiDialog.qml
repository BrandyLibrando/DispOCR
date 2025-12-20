import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Material

Window {
    id: root
    width: 480; height: 400

    visible: false
    modality: Qt.ApplicationModal
    title: "Set Region of Interest"

    Material.theme: Material.Light
    Material.accent: Material.Cyan

    signal hidden

    Button {
        text: "Close"
        onClicked: {
            root.hidden()
            root.hide()
        }
    }

    onVisibleChanged: if (!root.visible) root.hidden()
}
