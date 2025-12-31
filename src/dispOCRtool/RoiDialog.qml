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

    property Image viewfinder

    Column {
        anchors.fill: parent

        Pane {
            height: root.height * 4/5
            width: root.width

            // Image {
            //     id: roiVF
            //     property int paintedX: (roiVF.width - roiVF.paintedWidth) / 2
            //     property int paintedY: (roiVF.height - roiVF.paintedHeight) / 2

            //     anchors.fill: parent
            //     fillMode: Image.PreserveAspectFit
            //     anchors.margins: 0

            //     cache: false
            //     source: root.viewfinder.source


            //     property int roi_x1: 0
            //     property int roi_y1: 0
            //     property int roi_x2: 320
            //     property int roi_y2: 240

            //     property int imageWidth: 640
            //     property int imageHeight: 480

            //     function resetPoints() {
            //         roi_x1 = 0
            //         roi_y1 = 0
            //         roi_x2 = cvCameraRenderer.getWidth()
            //         roi_y2 = cvCameraRenderer.getHeight()
            //         imageWidth = cvCameraRenderer.getWidth()
            //         imageHeight = cvCameraRenderer.getHeight()
            //     }

            //     Rectangle {
            //         id: roioverlay
            //         color: Material.accent
            //         opacity: 0.2

            //         x: roiVF.paintedX + (roiVF.roi_x1 / roiVF.imageWidth * roiVF.paintedWidth)
            //         y: roiVF.paintedY + (roiVF.roi_y1 / roiVF.imageHeight * roiVF.paintedHeight)
            //         width: roiVF.paintedWidth * (roiVF.roi_x2 - roiVF.roi_x1) / roiVF.imageWidth
            //         height: roiVF.paintedHeight * (roiVF.roi_y2 - roiVF.roi_y1) / roiVF.imageHeight
            //     }
            // }

            ImageViewfinder {
                id: roiVF

                imageSource: viewfinder.source
                imageProvider: viewfinder.imageProvider
            }
        }

        Row {
            height: root.height * 1/5

            Button {
                text: "Close"
                onClicked: {
                    root.hidden()
                    root.hide()
                }
            }
        }
    }




    onVisibleChanged: if (!root.visible) root.hidden()
}
