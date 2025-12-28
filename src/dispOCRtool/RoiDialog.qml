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
    property var imageProvider
    property alias image:  viewfinder

    signal hidden


    Image {
        id: viewfinder

        anchors.fill: parent
        anchors.margins: 15
        anchors.bottomMargin: 40
        fillMode: Image.PreserveAspectFit

        // asynchronous: true
        cache: false
        source: "image://CvCameraFeed/img"
        property bool counter: false

        function reloadImage() {
            console.log("lel")
            counter = !counter
            source = "image://CvCameraFeed/img?id=" + counter
        }


        property int x1
        property int x2
        property int y1
        property int y2
        Rectangle {

        }
    }

    Button {
        anchors.horizontalCenter: parent.horizontalCenter

        text: "Close"
        onClicked: {
            root.hidden()
            root.hide()
        }
    }

    onVisibleChanged: if (!root.visible) root.hidden()
}
