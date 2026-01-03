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

            ImageViewfinder {
                id: roiVF

                overlayColor: viewfinder.overlayColor
                imageSource: viewfinder.source
                imageProvider: viewfinder.imageProvider
                imageWidth: viewfinder.imageWidth
                imageHeight: viewfinder.imageHeight

                Rectangle {
                    id: roioverlaynew
                    color: root.invertHexColor(viewfinder.overlayColor)
                    opacity: 0.4

                    x: Math.min(roiPt1.x + roiPt1.width/2, roiPt2.x + roiPt2.width/2)
                    y: Math.min(roiPt1.y + roiPt1.height/2, roiPt2.y + roiPt2.height/2)
                    width: Math.abs(roiPt1.x - roiPt2.x)
                    height: Math.abs(roiPt1.y - roiPt2.y)
                }

                Rectangle {
                    id: roiPt1
                    width: 8
                    height: width
                    color: "#f00"
                    radius: width/2

                    x:  roiVF.paintedX + (roiPt1.width / 2)
                    y:  roiVF.paintedY + (roiPt1.height / 2)

                    DragHandler {
                        target: roiPt1
                        xAxis.minimum: roiVF.paintedX - (roiPt1.width / 2)
                        xAxis.maximum: roiVF.paintedX + roiVF.paintedWidth - (roiPt1.width / 2)
                        yAxis.minimum: roiVF.paintedY - (roiPt1.width / 2)
                        yAxis.maximum: roiVF.paintedY + roiVF.paintedHeight - (roiPt1.width / 2)
                    }
                }

                Rectangle {
                    id: roiPt2
                    width: 8
                    height: width
                    color: "#f00"
                    radius: width/2

                    x:  roiVF.paintedX + roiVF.paintedWidth - (roiPt2.width / 2)
                    y:  roiVF.paintedY + roiVF.paintedHeight - (roiPt2.height / 2)

                    DragHandler {
                        target: roiPt2
                        xAxis.minimum: roiVF.paintedX - (roiPt2.width / 2)
                        xAxis.maximum: roiVF.paintedX + roiVF.paintedWidth - (roiPt2.width / 2)
                        yAxis.minimum: roiVF.paintedY - (roiPt2.width / 2)
                        yAxis.maximum: roiVF.paintedY + roiVF.paintedHeight - (roiPt2.width / 2)
                    }
                }
            }
        }

        Row {
            height: root.height * 1/5
            anchors.horizontalCenter: parent.horizontalCenter

            Button {
                text: "Close"
                onClicked: {
                    root.hidden()
                    root.hide()
                }
            }
        }
    }


    // Color inverter from hex string
    function invertHexColor(base: string): string {
        if (base.charAt(0) === '#') base = base.slice(1);
        const colors = [base.slice(0,2), base.slice(2,4), base.slice(4,6)];
        const invert_colors = colors.map( (color) => (255 - parseInt(color, 16)).toString(16).toLowerCase() );
        return "#" + invert_colors.join("")
    }

    onVisibleChanged: if (!root.visible) root.hidden()
}
