import QtMultimedia
import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Dialogs
import QtQuick.Layouts
// import QtQuick.VirtualKeyboard
import QtQuick.Controls.Material


ApplicationWindow {
    id: root
    width: 640; height: 480
    minimumWidth: 640; minimumHeight: 480
    maximumWidth: 640; maximumHeight: 480

    visible: true
    title: qsTr("DispOCR")

    Material.theme: Material.Light
    Material.accent: Material.Cyan
    property string disabledColor: "#9f9f9f"


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
                                padding: 2

                                background: Rectangle {
                                    color: "transparent"
                                }

                                anchors.verticalCenter: parent.verticalCenter
                                anchors.verticalCenterOffset: -1

                                Image {
                                    id: subCameraVF

                                    anchors.fill: parent
                                    fillMode: Image.PreserveAspectFit

                                    // asynchronous: true
                                    cache: false
                                    source: "image://MyImageProvider/img"
                                    property bool counter: false

                                    function reloadImage() {
                                        counter = !counter
                                        source = "image://MyImageProvider/img?id=" + counter
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
                                    font.bold: true
                                    font.pointSize: 9
                                    Material.foreground: Material.accent
                                    Material.background: "#eeeeee"
                                    Material.elevation: 1

                                    text: qsTr("Set ROI")

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
                                    font.bold: true
                                    font.pointSize: 9
                                    Material.foreground: Material.accent
                                    Material.background: "#eeeeee"
                                    Material.elevation: 1

                                    text: qsTr("Set Dir")

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

                                background: Rectangle {
                                    color: "#000000"
                                }
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
                            implicitWidth: predictTextScrollView.width - 20
                            implicitHeight: 5
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
                            implicitWidth: 4
                            implicitHeight: 0.85 * predictTextScrollView.height
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
                        anchors.fill: parent
                        topInset: 4
                        topPadding: 19
                        leftPadding: 12
                        rightPadding: 15
                        bottomPadding: 15

                        readOnly: true
                        activeFocusOnTab: false
                        focus: false
                        clip: false
                        font.pointSize: 10
                        cursorVisible: false

                        text: bridge.data
                        placeholderText: qsTr("Predicted Text")
                    }
                }

                TabBar {
                    id: settingsBar
                    x: 10; y: 4
                    width: implicitWidth; height: 12
                    spacing: 8

                    currentIndex: settingsContainer.currentIndex

                    Repeater {
                        model: [qsTr("General Settings"), qsTr("Control System Settings")]

                        TabButton {
                            id: settingsBarButton
                            width: implicitWidth
                            leftPadding: 5; rightPadding: 5
                            topPadding: 0; bottomPadding: 5

                            background: Rectangle {
                                height: 12
                                opacity: 1
                            }
                            contentItem: Text {
                                text: modelData

                                font.pointSize: 7
                                color: checked ? Material.accent : "#959595"
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter
                            }

                            onClicked: settingsContainer.setCurrentIndex(index)
                        }
                    }
                }

                Frame {
                    id: settingsFrame
                    width: settingsContainer.width
                    height: settingsContainer.height
                    clip: true

                    SwipeView {
                        id: settingsContainer
                        width: menuContainer.width
                        height: menuContainer.height * (1 / 2) - menuContainer.spacing - settingsBar.height

                        currentIndex: settingsBar.currentIndex

                        Item {
                            id: generalSettingsList

                            CheckBox {
                                id: toggleCorrection
                                x: -9; y: -10
                                height: 35
                                leftPadding: 8; rightPadding: 8
                                padding: 8
                                font.pointSize: 9
                                display: AbstractButton.TextBesideIcon

                                text: qsTr("Apply text correction upon saving")
                            }

                            Item {
                                id: groupInputLogFreq

                                Rectangle {
                                    id: inputLogFrequency
                                    x: inputCtrlCond.x + 20
                                    y: inputLogFrequencyLabel1.y + 2
                                    width: inputCtrlCond.width - 40
                                    height: inputCtrlCond.height
                                    border.width: 2
                                    border.color: inputFreqVal.focus ? Material.accent : "#959595"
                                    radius: 5
                                    clip: true

                                    TextInput{
                                        id: inputFreqVal
                                        width: parent.width
                                        leftPadding: 10; rightPadding: 10
                                        anchors.verticalCenter: parent.verticalCenter
                                        color: acceptableInput ? "#000" : "#E91E63"
                                        font.pixelSize: 12

                                        validator: DoubleValidator {
                                            notation: DoubleValidator.StandardNotation
                                            bottom: 0.1
                                        }
                                    }
                                }

                                Text {
                                    id: inputLogFrequencyLabel1
                                    x: 0; y: 28
                                    width: 119; height: 16
                                    font.pixelSize: 12
                                    text: qsTr("Log every:")
                                }

                                Text {
                                    id: inputLogFrequencyLabel2
                                    x: 0; y: 42
                                    width: 119; height: 16
                                    font.pixelSize: 12
                                    color: inputFreqVal.acceptableInput ? "#000" : "#E91E63"
                                    text: qsTr("(min: per 0.1 sec)")
                                }

                                Text {
                                    id: inputLogFrequencyLabel3
                                    x: inputLogFrequency.x + inputLogFrequency.width + 5
                                    anchors.verticalCenter: inputLogFrequency.verticalCenter
                                    width: 119; height: 16
                                    font.pixelSize: 12
                                    text: qsTr("sec.")
                                }
                            }
                        }

                        Item {
                            id: controlSettingsList

                            CheckBox {
                                id: toggleControlSystem
                                x: -9; y: -10
                                leftPadding: 8; rightPadding: 8
                                padding: 8
                                height: 35
                                font.pointSize: 9
                                display: AbstractButton.TextBesideIcon

                                checked: true
                                text: qsTr("Enable control system")
                            }

                            Item {
                                id: groupInputCtrlCondition

                                ComboBox {
                                    id: inputCtrlCond
                                    x: 84; y: 30
                                    width: 120; height: 28
                                    font.pointSize: 8

                                    enabled: toggleControlSystem.checked
                                    editable: false
                                    model: [qsTr("contains"), qsTr(">"), qsTr(">="), qsTr("<"), qsTr("<="), qsTr("equal to")]
                                }

                                Text {
                                    id: inputCtrlCondLabel1
                                    x: 0; y: 28
                                    width: 119; height: 16
                                    font.pixelSize: 12

                                    enabled: toggleControlSystem.checked
                                    text: qsTr("Control value")
                                }

                                Text {
                                    id: inputCtrlCondLabel2
                                    x: 0; y: 42
                                    width: 119; height: 16
                                    font.pixelSize: 12

                                    enabled: toggleControlSystem.checked
                                    text: qsTr("condition")
                                }
                            }

                            Item {
                                id: groupInputCtrlValue

                                Rectangle {
                                    id: inputCtrlValContainer
                                    x: inputCtrlCond.x + 10
                                    y: inputCtrlValLabel1.y + 2
                                    width: inputCtrlCond.width - 10
                                    height: inputCtrlCond.height
                                    border.width: 2
                                    border.color: inputCtrlVal.focus ? Material.accent : "#959595"
                                    radius: 5
                                    clip: true

                                    enabled: toggleControlSystem.checked

                                    TextInput{
                                        id: inputCtrlVal
                                        width: parent.width
                                        leftPadding: 10; rightPadding: 10
                                        anchors.verticalCenter: parent.verticalCenter
                                        color: acceptableInput ? "#000" : "#E91E63"
                                        font.pixelSize: 12

                                        enabled: toggleControlSystem.checked

                                        property var validNumber: DoubleValidator { notation: DoubleValidator.StandardNotation }
                                        property var validText: RegularExpressionValidator { regularExpression: /(.|\s)*\S(.|\s)*/ }
                                        validator: inputCtrlCond.currentValue === "contains" ? validText : validNumber
                                    }
                                }

                                Text {
                                    id: inputCtrlValLabel1
                                    x: 0; y: 66
                                    width: 119; height: 16
                                    font.pixelSize: 12

                                    text: qsTr("Value to check")
                                }

                                Text {
                                    id: inputCtrlValLabel2
                                    x: 0; y: 80
                                    width: 119; height: 16
                                    font.pixelSize: 12
                                    color: !toggleControlSystem.checked
                                           ? "#959595"
                                           : inputCtrlVal.acceptableInput
                                             ? Material.accent
                                             : "#E91E63"

                                    text: {
                                        if (!toggleControlSystem.checked) return qsTr("System disabled.")
                                        else if (inputCtrlVal.acceptableInput) return qsTr("Valid input.")
                                        else {
                                            if (inputCtrlCond.currentValue === "contains") return qsTr("Enter text.")
                                            else return qsTr("Enter numbers.")
                                        }
                                    }
                                }
                            }
                        }
                    }
                }

                Row {
                    id: operationContainer
                    width: menuContainer.width
                    height: menuContainer.height * (1 / 10)
                    rightPadding: 0; leftPadding: 0
                    spacing: 8

                    Button {
                        id: operationStart
                        width: operationContainer.width
                               - (operationStop.width + operationContainer.spacing)
                        height: operationContainer.height
                        font.bold: true
                        font.pointSize: 9
                        leftPadding: 14; rightPadding: 14
                        highlighted: true
                        Material.elevation: 1

                        text: qsTr("Start")

                        onClicked: {
                            // Check for invalid inputs
                            let allInputsValid = root.checkInputs(root.possibleInvalidInputs)
                            if (allInputsValid) {
                                main.state = "inop"
                            }
                            else {
                                let invalid = root.focusInvalidInput(root.possibleInvalidInputs)
                                console.log("", invalid)
                            }
                        }
                    }

                    Button {
                        id: operationStop
                        height: operationContainer.height
                        font.bold: true
                        font.pointSize: 9
                        leftPadding: 21; rightPadding: 21
                        highlighted: false
                        Material.foreground: Material.accent
                        Material.background: "#eeeeee"
                        Material.elevation: 1

                        enabled: false
                        text: qsTr("Stop + Save")
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
            width: 93; height: 12
            color: main.color

            Text {
                id: subCameraContainerLabelText
                x: 4; y: 2
                color: "#959595"
                font.pixelSize: 10
                text: qsTr("Camera Viewfinder")
            }
        }

        Rectangle {
            id: cameraContainerLabelBackground
            x: cameraContainer.x + 19; y: cameraContainer.y
            width: 137; height: 12
            color: main.color

            Text {
                id: cameraContainerLabelText
                x: 4; y: 2
                color: "#959595"
                font.pixelSize: 10
                text: qsTr("Region of Interest Viewfinder")
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
                bridge.updateData(folderDialog.selectedFolder)
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

        // VIRTUAL KEYBOARD
        // InputPanel {
        //     id: inputPanel
        //     y: Qt.inputMethod.visible ? parent.height - inputPanel.height : parent.height
        //     anchors.left: parent.left
        //     anchors.right: parent.right
        // }



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
                    settingsContainer { enabled: false; opacity: 0.3 }
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
                    settingsContainer { enabled: false; opacity: 0.3 }
                }
            }
        ]
    }

    // JAVASCRIPT HANDLERS
    property var possibleInvalidInputs: [
        {id: inputFreqVal, name: "Log frequency", pageIndex: 0},
        {id: inputCtrlVal, name: "Control value", pageIndex: 1},
    ]

    function checkInputs(inputList) {
        return inputList.every((field) => field.id.acceptableInput || !field.id.enabled)
    }

    function focusInvalidInput(inputList) {
        for (const field of inputList) {
            if (!field.id.acceptableInput && field.id.enabled) {
                settingsContainer.setCurrentIndex(field.pageIndex)
                field.id.forceActiveFocus();
                return field.name
            }
        }
        return ""
    }

    Connections{
        target: myImageProvider

        function onImageChanged(image) {
            console.log("emit")
            subCameraVF.reloadImage()
        }

    }

    Component.onCompleted: {
        myImageProvider.start()
    }

    onClosing: {
        myImageProvider.killThread()
    }
}
