import QtQuick
import QtQuick.Controls

Image {
    id: root

    // Computed properties
    property int paintedX: (root.width - root.paintedWidth) / 2
    property int paintedY: (root.height - root.paintedHeight) / 2

    // Filled properties
    property int roi_x1: 0
    property int roi_y1: 0
    property int roi_x2: imageWidth
    property int roi_y2: imageHeight

    property int imageWidth: imageProvider.getWidth()
    property int imageHeight: imageProvider.getHeight()
    property var imageSource  // QQuickImageProvider url
    property var imageProvider  // Image provider instance, instantiated in PY file

    property var overlayColor: "#ffff00"


    anchors.fill: parent
    fillMode: Image.PreserveAspectFit
    anchors.margins: 0

    cache: false
    source: imageSource


    function resetPoints() {
        roi_x1 = 0
        roi_y1 = 0
        imageWidth = imageProvider.getWidth()
        imageHeight = imageProvider.getHeight()
        roi_x2 = root.imageWidth
        roi_y2 = root.imageHeight
    }

    Rectangle {
        id: roioverlay
        color: overlayColor
        opacity: 0.2

        x: root.paintedX + (root.roi_x1 / root.imageWidth * root.paintedWidth)
        y: root.paintedY + (root.roi_y1 / root.imageHeight * root.paintedHeight)
        width: root.paintedWidth * (root.roi_x2 - root.roi_x1) / root.imageWidth
        height: root.paintedHeight * (root.roi_y2 - root.roi_y1) / root.imageHeight
    }

    MouseArea {
        anchors.fill: parent
        onClicked: console.log("", [root.paintedX, root.imageHeight, root.imageWidth, root.imageProvider.getWidth()])
    }
}
