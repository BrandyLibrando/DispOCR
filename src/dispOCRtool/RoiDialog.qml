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
    signal roiChanged(x1: int, y1: int, x2: int, y2: int)

    property Image viewfinder
    property int x1: Math.trunc( (roiPt1.x - roiVF.paintedX + roiPt1.width/2) / roiVF.paintedWidth * roiVF.imageWidth)
    property int x2: Math.trunc( (roiPt2.x - roiVF.paintedX + roiPt2.width/2) / roiVF.paintedWidth * roiVF.imageWidth)
    property int y1: Math.trunc( (roiPt1.y - roiVF.paintedY + roiPt1.height/2) / roiVF.paintedHeight * roiVF.imageHeight)
    property int y2: Math.trunc( (roiPt2.y - roiVF.paintedY + roiPt2.height/2) / roiVF.paintedHeight * roiVF.imageHeight)

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

                    x:  roiVF.paintedX
                    y:  roiVF.paintedY

                    DragHandler {
                        target: roiPt1
                        xAxis.minimum: roiVF.paintedX - (roiPt1.width / 2)
                        xAxis.maximum: roiPt2.x
                        yAxis.minimum: roiVF.paintedY - (roiPt1.width / 2)
                        yAxis.maximum: roiPt2.y
                    }
                }

                Rectangle {
                    id: roiPt2
                    width: 8
                    height: width
                    color: "#f00"
                    radius: width/2

                    x: roiVF.paintedX + roiVF.paintedWidth - (roiPt2.width / 2)
                    y: roiVF.paintedY + roiVF.paintedHeight - (roiPt2.height / 2)

                    DragHandler {
                        target: roiPt2
                        xAxis.minimum: roiPt1.x
                        xAxis.maximum: roiVF.paintedX + roiVF.paintedWidth - (roiPt2.width / 2)
                        yAxis.minimum: roiPt1.y
                        yAxis.maximum: roiVF.paintedY + roiVF.paintedHeight - (roiPt2.width / 2)
                    }
                }
            }
        }

        Row {
            height: root.height * 1/5
            anchors.horizontalCenter: parent.horizontalCenter
            spacing: 15

            Button {
                text: "Set new ROI"
                highlighted: true
                onClicked: {
                    roiVF.setRoi(root.x1, root.y1, root.x2, root.y2)
                    root.roiChanged(root.x1, root.y1, root.x2, root.y2)
                    root.hide()
                }
            }

            Button {
                text: "Cancel"
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

    function resetPoints() {
        roiVF.resetPoints();
    }

    onVisibleChanged: if (!root.visible) root.hidden()
}
