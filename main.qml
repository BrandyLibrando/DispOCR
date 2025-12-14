import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Dialogs
import QtMultimedia
import QtQuick.Controls.Material

// import io.qt.textproperties 1.0

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
            x: 8
            y: 8
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
                            rightInset: 8

                            Pane {
                                id: subCameraField
                                x: 2
                                width: subCameraBorder.width * 5 / 8
                                height: subCameraField.width / 16 * 9
                                anchors.verticalCenter: parent.verticalCenter
                                anchors.verticalCenterOffset: -1

                                Column {
                                    id: configContainer
                                    x: subCameraField.width + 2
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
                                        Material.elevation: 1

                                        onClicked: {
                                            main.state = "editroidir"
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
                                        Material.elevation: 1

                                        onClicked: {
                                            main.state = "editroidir"
                                            folderDialog.open()
                                        }
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

                    ScrollBar.horizontal.height: 10
                    ScrollBar.horizontal.width: predictTextScrollView.width - (2 * ScrollBar.vertical.width + 4)
                    ScrollBar.horizontal.anchors.horizontalCenter: predictTextScrollView.horizontalCenter
                    ScrollBar.horizontal.bottomInset: 5
                    ScrollBar.horizontal.bottomPadding: 5

                    ScrollBar.vertical.height: 0.85 * predictTextScrollView.height
                    ScrollBar.vertical.width: 10
                    ScrollBar.vertical.anchors.verticalCenter: predictTextScrollView.verticalCenter
                    ScrollBar.vertical.rightInset: 5
                    ScrollBar.vertical.rightPadding: 5

                    TextArea {
                        id: predictTextArea
                        color: "#000000"
                        text: "PredictedPredictedPredictedPredictedPredicted\n\nHi there\n\nHi there\n\nHi there\n\nHi there\n\nHi there"
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
                            text: qsTr("Use text correction")
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
                        font.bold: true
                        font.pointSize: 9
                        leftPadding: 21
                        rightPadding: 21
                        highlighted: false
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


        FolderDialog {
            id: folderDialog
            title: "Select a Folder"
            onAccepted: {
                main.state = ""
                console.log("Selected folder:", folderDialog.selectedFolder)
            }
            onRejected: {
                main.state = ""
                console.log("Folder selection canceled")
            }
        }

        states: [
            State {
                id: stateInOp
                name: "inop"
                PropertyChanges { target: configRoi; enabled: false }
                PropertyChanges { target: configDir; enabled: false }
                PropertyChanges { target: operationStart; enabled: false }
                PropertyChanges { target: operationStop; enabled: true }
            },
            State {
                id: statePopRoiDir
                name: "editroidir"
                PropertyChanges { target: configRoi; enabled: false }
                PropertyChanges { target: configDir; enabled: false }
                PropertyChanges { target: operationStart; enabled: false }
                PropertyChanges { target: operationStop; enabled: false }
            }
        ]
    }
}
