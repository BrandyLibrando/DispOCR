import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Controls.Material

Window {
    width: 640
    height: 480
    minimumWidth: 480
    minimumHeight: 360
    visible: true
    title: qsTr("DispOCR")

    Material.theme: Material.Light
    Material.accent: Material.Pink

    Rectangle {
        id: main
        anchors.fill: parent

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
                                        text: qsTr("Set ROI")
                                        highlighted: false
                                        flat: false
                                        font.bold: true
                                        font.pointSize: 9
                                    }

                                    Button {
                                        id: configDir
                                        width: configContainer.width
                                        text: qsTr("Set Dir")
                                        font.bold: true
                                        font.pointSize: 9
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
                    background: none.none

                    ScrollBar.horizontal.width: menuContainer.width - (ScrollBar.vertical.width + 4)

                    TextArea {
                        id: predictTextArea
                        color: "#000000"
                        text: "PredictedPredictedPredictedPredictedPredicted\n\nHi there\n\nHi there\n\nHi there\n\nHi there\n\nHi there"
                        anchors.fill: parent
                        activeFocusOnTab: false
                        focus: false
                        bottomPadding: 20
                        clip: false
                        topInset: 4
                        rightPadding: 20
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
                            height: 35
                            text: qsTr("Use text correction")
                            display: AbstractButton.TextBesideIcon
                            leftPadding: 8
                            padding: 8
                            rightPadding: 8
                            font.pointSize: 9
                        }

                        CheckBox {
                            id: toggleAutosave
                            x: -9
                            y: 28
                            height: 35
                            text: qsTr("Enable auto-save")
                            font.pointSize: 9
                        }

                        CheckBox {
                            id: toggleSsd
                            x: -9
                            y: 60
                            height: 35
                            text: qsTr("Optimize for 7-segment font")
                            autoExclusive: false
                            focusPolicy: Qt.StrongFocus
                            font.pointSize: 9
                        }

                        SpinBox {
                            id: inputLogFrequency
                            x: 136
                            y: 101
                            width: 68
                            height: 28
                            focusPolicy: Qt.StrongFocus
                            font.pointSize: 8
                            to: 30
                            from: 1
                        }

                        Text {
                            id: inputLogFrequencyLabel1
                            x: 0
                            y: 99
                            width: 119
                            height: 16
                            text: qsTr("Logging frequency")
                            font.pixelSize: 12
                        }

                        Text {
                            id: inputLogFrequencyLabel2
                            x: 0
                            y: 113
                            width: 119
                            height: 16
                            text: qsTr("per sec. (max 30)")
                            font.pixelSize: 12
                        }

                        CheckBox {
                            id: toggleDateMerge
                            x: -9
                            y: 174
                            height: 35
                            text: qsTr("Merge date and time")
                            font.pointSize: 9
                            focusPolicy: Qt.StrongFocus
                            autoExclusive: false
                        }

                        ComboBox {
                            id: inputDateFmt
                            x: 84
                            y: 141
                            width: 120
                            height: 28
                            editable: false
                            font.pointSize: 8
                        }

                        Text {
                            id: inputDateFmtLabel1
                            x: 0
                            y: 139
                            width: 119
                            height: 16
                            text: qsTr("Date")
                            font.pixelSize: 12
                        }

                        Text {
                            id: inputDateFmtLabel2
                            x: 0
                            y: 153
                            width: 119
                            height: 16
                            text: qsTr("format")
                            font.pixelSize: 12
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
                        highlighted: true
                        flat: false
                        rightPadding: 14
                        leftPadding: 14
                        font.pointSize: 9
                    }

                    Button {
                        id: operationStop
                        height: operationContainer.height
                        text: qsTr("Stop + Save")
                        highlighted: false
                        flat: false
                        font.bold: true
                        font.pointSize: 9
                        leftPadding: 21
                        rightPadding: 21
                    }
                }
            }
        }

        Rectangle {
            id: settingsContainerLabelBackground
            x: viewfinderContainer.width + 10
            y: predictTextScrollView.height + 8
            width: 49
            height: 12
            color: main.color

            Text {
                id: settingsContainerLabelText
                x: 4
                y: 0
                color: "#959595"
                text: qsTr("Settings")
                font.pixelSize: 12
            }
        }

        states: [
            State {
                id: stateNoOp
                name: "No Operation"
            },
            State {
                id: stateInOp
                name: "In Operation"
            },
            State {
                id: statePopRoi
                name: "Edit ROI"
            },
            State {
                id: statePopDir
                name: "Edit Directory"
            }
        ]
    }
}
