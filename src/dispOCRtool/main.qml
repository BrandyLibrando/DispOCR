import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Dialogs
import QtMultimedia
import QtQuick.Controls.Material

// import io.qt.textproperties 1.0

Window {
    id: root
    width: 640; height: 480
    minimumWidth: 640; minimumHeight: 480
    maximumWidth: 640; maximumHeight: 480

    visible: true
    title: qsTr("DispOCR")

    Material.theme: Material.Light
    Material.accent: Material.Cyan
    property string disabledColor: "#9f9f9f"


    // Bridge {
    //     id: bridge
    // }

    Rectangle {
        id: main
        anchors.fill: parent

        property real heightRatio: main.height/480
        property real widthRatio: main.width/640

        Row {
            id: mainContainer
            x: 8; y: 8
            width: main.width - (mainContainer.x * 2)
            height: main.height - (mainContainer.y * 2)

            Flow {
                id: viewfinderContainer
                width: mainContainer.width * (43 / 68)
                height: mainContainer.height

                Column {
                    id: viewfinderSeparator
                    anchors.fill: parent
                    spacing: 8
                    rightPadding: 8
                    padding: 0

                    Row {
                        id: subCameraContainer
                        width: viewfinderContainer.width
                        height: predictTextScrollView.height
                        rightPadding: 0

                        Frame {
                            id: subCameraBorder
                            anchors.fill: parent
                            topInset: 5; rightInset: 8

                            Pane {
                                id: subCameraField
                                x: 2
                                width: subCameraBorder.width * 5 / 8
                                height: subCameraField.width / 16 * 9
                                background: Rectangle {
                                    color: "#000000"
                                }

                                anchors.verticalCenter: parent.verticalCenter
                                anchors.verticalCenterOffset: -1

                                Image {
                                    id: name

                                    anchors.fill: parent
                                    fillMode: Image.PreserveAspectFit

                                    source: "image://live/image"
                                    asynchronous: true
                                    cache: false

                                    function reload()
                                    {
                                        counter = !counter
                                        source = "image://live/image?id=" + counter
                                    }
                                }
                            }

                            Column {
                                id: configContainer
                                x: subCameraField.width + (subCameraBorder.width * 1/32)
                                width: subCameraBorder.width * 1/4
                                height: subCameraField.height
                                anchors.verticalCenter: parent.verticalCenter
                                topPadding: (configContainer.height - (configRoi.height + configDir.height)) / 2
                                spacing: 0

                                Button {
                                    id: configRoi
                                    width: configContainer.width
                                    height: operationStop.height
                                    text: qsTr("Set ROI")
                                    font.bold: true
                                    font.pointSize: 9
                                    Material.foreground: Material.accent
                                    Material.background: "#eeeeee"
                                    Material.elevation: 1

                                    onClicked: {
                                        main.state = "editroidir"
                                        roiwindow.show()
                                        console.log("pressed")
                                    }
                                }

                                Button {
                                    id: configDir
                                    width: configContainer.width
                                    height: operationStop.height
                                    text: qsTr("Set Dir")
                                    font.bold: true
                                    font.pointSize: 9
                                    Material.foreground: Material.accent
                                    Material.background: "#eeeeee"
                                    Material.elevation: 1

                                    onClicked: {
                                        main.state = "editroidir"
                                        folderDialog.open()
                                    }
                                }
                            }
                        }
                    }

                    Flow {
                        id: cameraContainer
                        width: viewfinderContainer.width
                        height: viewfinderContainer.height
                                - (subCameraContainer.height + viewfinderSeparator.spacing)
                        rightPadding: 8

                        Frame {
                            id: cameraBorder
                            anchors.fill: parent
                            rightInset: 8

                            Pane {
                                id: cameraField
                                width: cameraBorder.width * 9 / 10
                                height: cameraField.width / 16 * 9
                                anchors.centerIn: parent
                                anchors.horizontalCenterOffset: -4
                                rightInset: 0
                            }
                        }
                    }
                }
            }

            Column {
                id: menuContainer
                width: mainContainer.width - viewfinderContainer.width
                height: mainContainer.height
                spacing: 8

                ScrollView {
                    id: predictTextScrollView
                    width: menuContainer.width
                    height: menuContainer.height * (2 / 5) - menuContainer.spacing

                    ScrollBar.horizontal: ScrollBar {
                        policy: ScrollBar.AsNeeded
                        background: Rectangle {
                            implicitHeight: 5
                            implicitWidth: predictTextScrollView.width - 20
                            radius: 5
                            color: "#eeeeee"
                        }

                        contentItem: Rectangle {
                            implicitWidth: 5
                            radius: 5
                            color: Material.accent
                        }

                        Component.onCompleted: {
                            bottomInset = 5
                            bottomPadding = 5
                            anchors.bottom = predictTextScrollView.bottom
                            anchors.horizontalCenter = predictTextScrollView.horizontalCenter
                        }
                    }

                    ScrollBar.vertical: ScrollBar {
                        policy: ScrollBar.AsNeeded
                        background: Rectangle {
                            implicitHeight: 0.85 * predictTextScrollView.height
                            implicitWidth: 4
                            radius: 5
                            color: "#eeeeee"
                        }

                        contentItem: Rectangle {
                            implicitWidth: 4
                            radius: 5
                            color: Material.accent
                        }

                        Component.onCompleted: {
                            rightInset = 5
                            rightPadding = 5
                            anchors.right = predictTextScrollView.right
                            anchors.verticalCenter = predictTextScrollView.verticalCenter
                        }
                    }


                    TextArea {
                        id: predictTextArea
                        text: main.state
                        anchors.fill: parent
                        activeFocusOnTab: false
                        focus: false
                        bottomPadding: 15
                        clip: false
                        topInset: 4
                        rightPadding: 15
                        leftPadding: 12
                        font.pointSize: 9
                        topPadding: 19
                        cursorVisible: false
                        readOnly: true
                        placeholderText: qsTr("Text Area")
                    }
                }

                ScrollView {
                    id: settingsContainer
                    width: menuContainer.width
                    height: menuContainer.height * (1 / 2) - menuContainer.spacing

                    Frame {
                        id: settingsFrame
                        width: settingsContainer.width
                        height: settingsContainer.height
                        spacing: 0

                        CheckBox {
                            id: toggleCorrection
                            x: -9
                            y: -4
                            text: qsTr("Apply text correction upon saving")
                            display: AbstractButton.TextBesideIcon
                            leftPadding: 8
                            rightPadding: 8
                            padding: 8

                            height: 35
                            font.pointSize: 9
                        }

                        CheckBox {
                            id: toggleAutosave
                            x: -9
                            y: 28
                            text: qsTr("Enable auto-save")
                            height: 35
                            font.pointSize: 9
                        }

                        CheckBox {
                            id: toggleSsd
                            x: -9
                            y: 60
                            text: qsTr("Optimize for 7-segment font")
                            height: 35
                            font.pointSize: 9
                        }

                        SpinBox {
                            id: inputLogFrequency
                            x: 136
                            y: 101
                            width: 68
                            height: 28
                            font.pointSize: 8
                            from: 1
                            to: 30
                        }

                        Text {
                            id: inputLogFrequencyLabel1
                            x: 0
                            y: 99
                            text: qsTr("Logging frequency")
                            width: 119
                            height: 16
                            font.pixelSize: 12
                        }

                        Text {
                            id: inputLogFrequencyLabel2
                            x: 0
                            y: 113
                            text: qsTr("per sec. (max 30)")
                            width: 119
                            height: 16
                            font.pixelSize: 12
                        }

                        ComboBox {
                            id: inputDateFmt
                            x: 84
                            y: 141
                            editable: false
                            width: 120
                            height: 28
                            font.pointSize: 8
                        }

                        Text {
                            id: inputDateFmtLabel1
                            x: 0
                            y: 139
                            text: qsTr("Date")
                            width: 119
                            height: 16
                            font.pixelSize: 12
                        }

                        Text {
                            id: inputDateFmtLabel2
                            x: 0
                            y: 153
                            text: qsTr("format")
                            width: 119
                            height: 16
                            font.pixelSize: 12
                        }

                        CheckBox {
                            id: toggleDateMerge
                            x: -9
                            y: 174
                            text: qsTr("Merge date and time")
                            height: 35
                            font.pointSize: 9
                        }
                    }
                }

                Row {
                    id: operationContainer
                    width: menuContainer.width
                    height: menuContainer.height * (1 / 10)
                    rightPadding: 0
                    leftPadding: 0
                    spacing: 8

                    Button {
                        id: operationStart
                        width: operationContainer.width
                               - (operationStop.width + operationContainer.spacing)
                        height: operationContainer.height
                        text: qsTr("Start")
                        font.bold: true
                        font.pointSize: 9
                        rightPadding: 14
                        leftPadding: 14
                        highlighted: true
                        Material.elevation: 1

                        onClicked: {
                            // processes for start operation
                            main.state = "inop"
                        }
                    }

                    Button {
                        id: operationStop
                        height: operationContainer.height
                        text: qsTr("Stop + Save")
                        // text: folderDialog.selectedFolder.toString()
                        font.bold: true
                        font.pointSize: 9
                        leftPadding: 21
                        rightPadding: 21
                        highlighted: false
                        Material.foreground: Material.accent
                        Material.background: "#eeeeee"
                        Material.elevation: 1

                        enabled: false
                        onClicked: {
                            // finalize write CSV file
                            // processes
                            main.state = ""
                        }
                    }
                }
            }
        }


        ///////////////////////
        /// MISCELLANEOUS
        ///////////////////////

        Rectangle {
            id: subCameraContainerLabelBackground
            x: subCameraContainer.x + 19
            y: subCameraContainer.y + 4
            width: 93
            height: 12
            color: main.color

            Text {
                id: subCameraContainerLabelText
                x: 4
                y: 2
                color: "#959595"
                text: qsTr("Camera Viewfinder")
                font.pixelSize: 10
            }
        }

        Rectangle {
            id: cameraContainerLabelBackground
            x: cameraContainer.x + 19
            y: cameraContainer.y
            width: 137
            height: 12
            color: main.color

            Text {
                id: cameraContainerLabelText
                x: 4
                y: 2
                color: "#959595"
                text: qsTr("Region of Interest Viewfinder")
                font.pixelSize: 10
            }
        }

        Rectangle {
            id: settingsContainerLabelBackground
            x: viewfinderContainer.width + 19
            y: predictTextScrollView.height + 8
            width: 45
            height: 12
            color: main.color

            Text {
                id: settingsContainerLabelText
                x: 4
                y: 2
                color: "#959595"
                text: qsTr("Settings")
                font.pixelSize: 10
            }
        }


        //////////////////
        /// HANDLERS
        //////////////////

        // SAVE DIRECTORY HANDLER
        FolderDialog {
            id: folderDialog
            title: "Select a Folder"
            // property QUrl prevFolder: none
            onAccepted: {
                main.state = ""
                console.log("Selected folder:", folderDialog.selectedFolder)
            }
            onRejected: {
                main.state = ""
                console.log("Folder selection canceled")
            }
        }


        // ROI SELECTION HANDLER
        RoiDialog {
            id: roiwindow
            onHidden: main.state = ""
        }

        // CAMERA DEVICE HANDLERS
        MediaDevices {
            id: mediaDevices
        }

        CaptureSession {
            videoOutput: subCameraView
            camera: Camera {
                cameraDevice: mediaDevices.defaultVideoInput
            }
        }


        // WINDOW STATE MANAGEMENT
        states: [
            State {
                id: stateInOp
                name: "inop"
                PropertyChanges {
                    configRoi { enabled: false }
                    configDir { enabled: false }
                    operationStart { enabled: false }
                    operationStop { enabled: true }
                    settingsFrame { enabled: false }
                    inputLogFrequencyLabel1 { color: root.disabledColor }
                    inputLogFrequencyLabel2 { color: root.disabledColor }
                    inputDateFmtLabel1 { color: root.disabledColor }
                    inputDateFmtLabel2 { color: root.disabledColor }
                }
            },
            State {
                id: statePopRoiDir
                name: "editroidir"
                PropertyChanges {
                    configRoi { enabled: false }
                    configDir { enabled: false }
                    operationStart { enabled: false }
                    operationStop { enabled: false }
                    settingsFrame { enabled: false }
                    inputLogFrequencyLabel1 { color: root.disabledColor }
                    inputLogFrequencyLabel2 { color: root.disabledColor }
                    inputDateFmtLabel1 { color: root.disabledColor }
                    inputDateFmtLabel2 { color: root.disabledColor }
                }
            }
        ]
    }
}
