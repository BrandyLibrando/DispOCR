import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Dialogs
import QtQuick.Layouts
// import QtMultimedia
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

        // Camera image properties
        property bool daiCameraSelected: inputCameraDevice.currentText.includes("[D")
        property real heightRatio: main.height/480
        property real widthRatio: main.width/640
        property var editedImage: null

        property int cameraWidth: 0
        property int cameraHeight: 0

        property string lastText: ""
        property real lastScore: 0.0

        property string saveDir: ""

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
                    spacing: 8
                    rightPadding: 8
                    padding: 0

                    Item {
                        id: subCameraContainer
                        width: viewfinderContainer.width
                        height: predictTextScrollView.height

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
                                    property string providerId: "image://CvRoiFeed/img"

                                    anchors.fill: parent
                                    fillMode: Image.PreserveAspectFit

                                    // asynchronous: true
                                    cache: false
                                    source: providerId
                                    property bool counter: false

                                    function reloadImage() {
                                        counter = !counter
                                        source = providerId + "?id=" + counter
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
                                    hoverEnabled: true
                                    ToolTip.delay: 250
                                    ToolTip.timeout: 5000
                                    ToolTip.visible: hovered
                                    ToolTip.text: qsTr("Current directory: %1").arg(main.saveDir)

                                    onClicked: {
                                        main.state = "editroidir"
                                        folderDialog.open()
                                    }
                                }

                                Text {
                                    id: labelFpsCam
                                    color: Material.accent
                                    font.pixelSize: 10
                                    text: qsTr("Starting cam...")
                                }

                                Text {
                                    id: labelFpsOcr
                                    color: Material.accent
                                    font.pixelSize: 10
                                    text: qsTr("Starting OCR...")
                                }
                            }
                        }
                    }

                    Item {
                        id: cameraContainer
                        width: viewfinderContainer.width
                        height: viewfinderContainer.height
                                - (subCameraContainer.height + viewfinderSeparator.spacing)

                        Frame {
                            id: cameraBorder
                            anchors.fill: parent
                            rightInset: 8

                            Pane {
                                id: cameraField
                                width: cameraBorder.width * 9 / 10
                                height: cameraField.width / 4.5 * 3
                                anchors.centerIn: parent
                                anchors.horizontalCenterOffset: -4
                                rightInset: 0
                                padding: 0

                                ImageViewfinder {
                                    id: cameraVF
                                    property string providerId: "image://CvCameraFeed/img"

                                    overlayColor: Material.accent
                                    imageProvider: cvCameraRenderer
                                    imageWidth: main.cameraWidth
                                    imageHeight: main.cameraHeight

                                    imageSource: providerId
                                    property bool counter: false

                                    function reloadImage() {
                                        counter = !counter
                                        imageSource = providerId + "?id=" + counter
                                    }
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
                        width: parent.width
                        height: parent.height
                        topInset: 4
                        topPadding: 19
                        leftPadding: 12
                        rightPadding: 15
                        bottomPadding: 15

                        readOnly: true
                        activeFocusOnTab: false
                        focus: false
                        clip: false
                        wrapMode: TextEdit.WordWrap
                        font.pointSize: 10
                        cursorVisible: false

                        placeholderText: qsTr("Predicted Text (%1%)").arg(main.lastScore)
                    }
                }

                TabBar {
                    id: settingsBar
                    x: 10; y: 4
                    width: implicitWidth; height: 12
                    spacing: 8

                    currentIndex: settingsContainer.currentIndex

                    Repeater {
                        model: [
                            { name: qsTr("General"), condition: true, tip: null },
                            { name: qsTr("Control System"), condition: true, tip: null },
                            { name: qsTr("DepthAI Camera"), condition: main.daiCameraSelected, tip: qsTr("Must select a DepthAI device first.") }
                        ]

                        TabButton {
                            id: settingsBarButton
                            width: implicitWidth
                            leftPadding: 5; rightPadding: 5
                            topPadding: 0; bottomPadding: 5
                            enabled: modelData.condition

                            background: Rectangle {
                                id: settingsBarBg
                                height: 12
                                opacity: 1
                            }
                            contentItem: Text {
                                id: settingsBarLabel
                                text: modelData.name

                                font.pointSize: 7
                                color: checked ? Material.accent : !modelData.condition ? "#E91E63" : "#959595"
                                opacity: modelData.condition ? 1 : 0.5
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter

                                MouseArea {
                                    anchors.fill: parent
                                    onClicked: if (modelData.condition) settingsContainer.setCurrentIndex(index); else return  // Prevent invalid menu from being clickable

                                    hoverEnabled: true
                                    ToolTip.delay: 250
                                    ToolTip.timeout: 5000
                                    ToolTip.visible: hovered && !modelData.condition  // Only show tooltip for invalid menus
                                    ToolTip.text: modelData.tip
                                }
                            }
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
                        interactive: false

                        Item {
                            id: generalSettingsList

                            Item {
                                id: groupInputCameraDevice

                                ComboBox {
                                    id: inputCameraDevice
                                    x: 0; y: inputCameraDeviceLabel1.y + 20
                                    width: settingsContainer.width - 30; height: 28
                                    font.pointSize: 8

                                    editable: false
                                    model: if (cameraList && cameraList.data.length) cameraList.data; else "No camera detected."

                                    Connections {
                                        function onCurrentIndexChanged() {
                                            if (inputCameraDevice.currentText && inputCameraDevice.currentIndex !== -1) {
                                                const daiIndex = Math.max(-1, inputCameraDevice.currentIndex - cvCamCount);
                                                cvCameraRenderer.change_camera(
                                                            inputCameraDevice.currentIndex,
                                                            inputCameraDevice.model[inputCameraDevice.currentIndex],
                                                            daiIndex,  // Check if camera is DAI based on CV2 cam count
                                                );
                                            }
                                        }
                                    }
                                }

                                Text {
                                    id: inputCameraDeviceLabel1
                                    x: 0; y: -2
                                    width: 119; height: 16
                                    font.pixelSize: 11

                                    text: qsTr("Choose input camera device")
                                }
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
                                        font.pixelSize: 11

                                        validator: DoubleValidator {
                                            notation: DoubleValidator.StandardNotation
                                            bottom: 0.1
                                        }

                                        onTextChanged: {
                                            if (inputFreqVal.acceptableInput) appSettings.setLogFrequency(inputFreqVal.text);
                                        }
                                    }
                                }

                                Text {
                                    id: inputLogFrequencyLabel1
                                    x: 0; y: 58
                                    width: 119; height: 16
                                    font.pixelSize: 11
                                    text: qsTr("Log every:")
                                }

                                Text {
                                    id: inputLogFrequencyLabel2
                                    x: 0; y: inputLogFrequencyLabel1.y + 14
                                    width: 119; height: 16
                                    font.pixelSize: 11
                                    color: inputFreqVal.acceptableInput ? "#000" : "#E91E63"
                                    text: qsTr("(min: per 0.1 sec)")
                                }

                                Text {
                                    id: inputLogFrequencyLabel3
                                    x: inputLogFrequency.x + inputLogFrequency.width + 5
                                    anchors.verticalCenter: inputLogFrequency.verticalCenter
                                    width: 119; height: 16
                                    font.pixelSize: 11
                                    text: qsTr("sec.")
                                }
                            }

                            CheckBox {
                                id: toggleCorrection
                                x: -9; y: 88
                                height: 35
                                leftPadding: 8; rightPadding: 8
                                padding: 8
                                font.pointSize: 8
                                display: AbstractButton.TextBesideIcon

                                text: qsTr("Apply LLM text correct upon save")
                                onCheckedChanged: appSettings.setEnableTextCorrection(checked);
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
                                font.pointSize: 8
                                display: AbstractButton.TextBesideIcon

                                text: qsTr("Enable control system")
                                onCheckedChanged: appSettings.setEnableController(checked);
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
                                    font.pixelSize: 11

                                    enabled: toggleControlSystem.checked
                                    text: qsTr("Control value")
                                }

                                Text {
                                    id: inputCtrlCondLabel2
                                    x: 0; y: 42
                                    width: 119; height: 16
                                    font.pixelSize: 11

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
                                        font.pixelSize: 11

                                        enabled: toggleControlSystem.checked
                                        opacity: enabled ? 1.0 : 0.3

                                        property var validNumber: DoubleValidator { notation: DoubleValidator.StandardNotation }
                                        property var validText: RegularExpressionValidator { regularExpression: /(.|\s)*\S(.|\s)*/ }
                                        validator: inputCtrlCond.currentValue === "contains" ? validText : validNumber
                                        onTextChanged: {
                                            if (inputCtrlVal.acceptableInput) appSettings.setControllerValue(inputCtrlVal.text);
                                        }
                                    }
                                }

                                Text {
                                    id: inputCtrlValLabel1
                                    x: 0; y: 66
                                    width: 119; height: 16
                                    font.pixelSize: 11

                                    text: qsTr("Value to check")
                                }

                                Text {
                                    id: inputCtrlValLabel2
                                    x: 0; y: inputCtrlValLabel1.y + 14
                                    width: 119; height: 16
                                    font.pixelSize: 11
                                    color: !toggleControlSystem.checked
                                           ? "#959595"
                                           : inputCtrlVal.acceptableInput
                                             ? Material.accent
                                             : "#E91E63"

                                    text: {
                                        if (!toggleControlSystem.checked) return qsTr("Disabled.")
                                        else if (inputCtrlVal.acceptableInput) return qsTr("Valid input.")
                                        else {
                                            if (inputCtrlCond.currentValue === "contains") return qsTr("Enter text.")
                                            else return qsTr("Enter numbers.")
                                        }
                                    }
                                }
                            }
                        }

                        Item {
                            id: depthaiSettingsList

                            Column {
                                id: groupDaiExposure
                                x: 0; y: 0
                                width: settingsContainer.width - 5
                                spacing: -10

                                Text {
                                    id: groupDaiExposureLabel
                                    height: 16
                                    font.pixelSize: 11

                                    text: qsTr("Manual exposure & ISO (%1, %2)").arg(daiExposure.value).arg(daiIso.value)
                                }

                                Row {
                                    x: -5
                                    width: parent.width - 5

                                CheckBox {
                                    id: toggleDaiExposure
                                        y: (parent.height / 2) - (height / 2)
                                        width: 25
                                    font.pointSize: 8
                                        display: AbstractButton.IconOnly

                                        ToolTip.delay: 250
                                        ToolTip.timeout: 5000
                                        ToolTip.visible: hovered
                                        ToolTip.text: qsTr("Enable manual exposure and ISO")

                                    onCheckedChanged: {
                                        appSettings.setEnableManualExposure(checked);
                                    }
                                }

                                    Column {
                                        id: groupDaiExposureSliders
                                        width: parent.width - toggleDaiExposure.width
                                        spacing: -20

                                Slider {
                                    id: daiExposure
                                    width: parent.width
                                    from: 1; to: 33000
                                    stepSize: 250
                                    touchDragThreshold: 4
                                    enabled: toggleDaiExposure.checked

                                    ToolTip {
                                        parent: daiExposure.handle
                                        visible: daiExposure.pressed
                                                text: qsTr("Exposure: %1").arg(daiExposure.value)
                                        background: Rectangle {
                                            radius: width / 2
                                            border.color: Material.accent; color: Material.accent
                                        }
                                    }

                                    onMoved: {
                                        appSettings.setManualExposure(value);
                                            }
                                        }

                                        Slider {
                                            id: daiIso
                                            width: parent.width
                                            from: 100; to: 1600
                                            stepSize: 50
                                            touchDragThreshold: 4
                                            enabled: toggleDaiExposure.checked

                                            ToolTip {
                                                parent: daiIso.handle
                                                visible: daiIso.pressed
                                                text: qsTr("ISO: %1").arg(daiIso.value)
                                                background: Rectangle {
                                                    radius: width / 2
                                                    border.color: Material.accent; color: Material.accent
                                                }
                                            }

                                            onMoved: {
                                                appSettings.setManualIso(value);
                                            }
                                        }
                                    }
                                }
                            }

                            Column {
                                id: groupDaiWB
                                x: 0; y: groupDaiExposure.y + groupDaiExposure.height + 3
                                width: settingsContainer.width - 5
                                spacing: -10

                                Text {
                                    id: groupDaiWBLabel
                                    height: 16
                                    font.pixelSize: 11

                                    text: qsTr("Manual white balance (%1K)").arg(daiWB.value)
                                }

                                Row {
                                    x: -5
                                    width: parent.width - 5

                                CheckBox {
                                        id: toggleDaiWB
                                        y: (parent.height / 2) - (height / 2)
                                        width: 25
                                    font.pointSize: 8
                                        display: AbstractButton.IconOnly

                                        ToolTip.delay: 250
                                        ToolTip.timeout: 5000
                                        ToolTip.visible: hovered
                                        ToolTip.text: qsTr("Enable manual white balance")

                                    onCheckedChanged: {
                                            appSettings.setEnableManualWhiteBalance(checked);
                                    }
                                }

                                    Column {
                                        id: groupDaiWBSliders
                                        width: parent.width - toggleDaiWB.width
                                        spacing: -20

                                Slider {
                                            id: daiWB
                                    width: parent.width
                                            from: 1000; to: 12000
                                            stepSize: 500
                                    touchDragThreshold: 4
                                            enabled: toggleDaiWB.checked

                                    ToolTip {
                                                parent: daiWB.handle
                                                visible: daiWB.pressed
                                                text: qsTr("White balance: %1K").arg(daiWB.value)
                                        background: Rectangle {
                                            radius: width / 2
                                            border.color: Material.accent; color: Material.accent
                                        }
                                    }

                                    onMoved: {
                                                appSettings.setManualWhiteBalance(value);
                                            }
                                        }
                                    }
                                }
                            }

                            Column {
                                id: groupDaiFocus
                                x: 0; y: groupDaiWB.y + groupDaiWB.height + 3
                                width: settingsContainer.width - 5
                                spacing: -10

                                Text {
                                    id: groupDaiFocusLabel
                                    height: 16
                                    font.pixelSize: 11

                                    text: qsTr("Manual focus (%1)").arg(daiFocus.value)
                                }

                                Row {
                                    x: -5
                                    width: parent.width - 5

                                CheckBox {
                                    id: toggleDaiFocus
                                        y: (parent.height / 2) - (height / 2)
                                        width: 25
                                    font.pointSize: 8
                                        display: AbstractButton.IconOnly

                                        ToolTip.delay: 250
                                        ToolTip.timeout: 5000
                                        ToolTip.visible: hovered
                                        ToolTip.text: qsTr("Enable manual focus")

                                    onCheckedChanged: {
                                        appSettings.setEnableManualFocus(checked);
                                    }
                                }

                                    Column {
                                        id: groupDaiFocusSliders
                                        width: parent.width - toggleDaiFocus.width
                                        spacing: -20

                                Slider {
                                    id: daiFocus

                                    width: parent.width
                                    from: 0; to: 255
                                    stepSize: 5
                                    touchDragThreshold: 4
                                    enabled: toggleDaiFocus.checked

                                    ToolTip {
                                        parent: daiFocus.handle
                                        visible: daiFocus.pressed
                                                text: qsTr("Focus: %1").arg(daiFocus.value)
                                        background: Rectangle {
                                            radius: width / 2
                                            border.color: Material.accent; color: Material.accent
                                        }
                                    }

                                    onMoved: {
                                        appSettings.setManualFocus(value);
                                            }
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
                        hoverEnabled: true
                        ToolTip.delay: 250
                        ToolTip.timeout: 5000
                        ToolTip.visible: hovered
                        ToolTip.text: qsTr("Start logging values into a .txt file.")

                        onClicked: {
                            // Check for invalid inputs
                            let allInputsValid = root.checkInputs(root.possibleInvalidInputs)
                            if (allInputsValid) {
                                main.state = "inop";
                                fileLogger.start( parseFloat(inputFreqVal.text) * 1000 );
                            }
                            else {
                                let invalid = root.focusInvalidInput(root.possibleInvalidInputs);
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
                        hoverEnabled: true
                        ToolTip.delay: 250
                        ToolTip.timeout: 5000
                        ToolTip.visible: hovered
                        ToolTip.text: qsTr("Stop log. Start correction if enabled.")

                        onClicked: {
                            // finalize write CSV file
                            // processes
                            fileLogger.stop(appSettings.getEnableTextCorrection());
                            main.state = "";
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
            width: 152; height: 12
            color: main.color

            Text {
                id: subCameraContainerLabelText
                x: 4; y: 3
                color: "#959595"
                font.pixelSize: 10
                text: qsTr("Region of Interest Viewfinder")
            }
        }

        Rectangle {
            id: cameraContainerLabelBackground
            x: cameraContainer.x + 19; y: cameraContainer.y
            width: 103; height: 12
            color: main.color

            Text {
                id: cameraContainerLabelText
                x: 4; y: 3
                color: "#959595"
                font.pixelSize: 10
                text: qsTr("Camera Viewfinder")
            }
        }


        //////////////////
        /// HANDLERS
        //////////////////

        // SAVE DIRECTORY HANDLER
        FolderDialog {
            id: folderDialog
            title: "Select a Folder"
            currentFolder: main.saveDir
            onAccepted: {
                main.state = "";
                appSettings.setSaveDir(folderDialog.selectedFolder);
                fileLogger.update_dir(folderDialog.selectedFolder);
                main.saveDir = appSettings.getSaveDir();
            }
            onRejected: {
                main.state = "";
                console.log("> Folder selection canceled.");
            }
        }

        // ROI SELECTION HANDLER
        RoiDialog {
            id: roiwindow
            viewfinder: cameraVF
            onHidden: main.state = ""
            onRoiChanged: (x1, y1, x2, y2) => {
                cvCameraRenderer.setRoi(x1, y1, x2, y2);
                cameraVF.setRoi(x1, y1, x2, y2);
            }
        }

        // DATA HANDLER FOR IMAGE PROVIDER CLASS
        Connections {
            target: cvCameraRenderer

            function onImageChanged(image, roi_image) {
                // main.editedImage = cvCameraRenderer.cropped_image

                subCameraVF.reloadImage();
                cameraVF.reloadImage();
                if (!roiwindow.hidden) roiwindow.viewfinder.reloadImage();

            }

            function onCameraOpened(cameraWidth, cameraHeight) {
                main.cameraWidth = cameraWidth;
                main.cameraHeight = cameraHeight;
                roiwindow.resetPoints();
                cameraVF.resetPoints();
            }

            function onPredictionChanged(predictText, predictScore) {
                fileLogger.update_data(predictText);
                predictTextArea.text = predictText;
                main.lastText = predictText;
                main.lastScore = (predictScore * 100).toFixed(2);
            }

            function onFpsCamChanged(fps) { labelFpsCam.text = qsTr("Camera: %1 FPS").arg(fps.toFixed(2)); }
            function onFpsOcrChanged(fps) { labelFpsOcr.text = qsTr("OCR: %1 FPS").arg(fps.toFixed(2)); }
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
                    settingsContainer { enabled: false; opacity: 0.3 }
                }
            },
            State {
                id: statePopulateRoiDir
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

    // Check validity of enabled inputs
    function checkInputs(inputList) {
        return inputList.every((field) => field.id.acceptableInput || !field.id.enabled)
    }

    // Switch focus to enabled invalid input
    function focusInvalidInput(inputList) {
        for (const field of inputList) {
            if (!field.id.acceptableInput && field.id.enabled) {
                settingsContainer.setCurrentIndex(field.pageIndex);
                field.id.forceActiveFocus();
                return field.name
            }
        }
        return ""
    }

    // Get MXID portion of DAI camera name
    function getLastWord(str) { return str.trim().split(" ").pop(); }


    Component.onCompleted: {
        if (cameraList.data.length) {
            cvCameraRenderer.start();
        }

        // Preload app settings with previous settings
        const cfg = appSettings;
        main.saveDir                = cfg.getSaveDir();
        inputFreqVal.text           = cfg.getLogFrequency();
        toggleCorrection.checked    = cfg.getEnableTextCorrection();

        toggleControlSystem.checked = cfg.getEnableController();
        inputCtrlVal.text           = cfg.getControllerValue();

        toggleDaiExposure.checked   = cfg.getEnableManualExposure();
        toggleDaiFocus.checked      = cfg.getEnableManualFocus();
        toggleDaiWB.checked         = cfg.getEnableManualWhiteBalance();
        daiExposure.value           = cfg.getManualExposure();
        daiIso.value                = cfg.getManualIso();
        daiFocus.value              = cfg.getManualFocus();
        daiWB.value                 = cfg.getManualWhiteBalance();
    }
}
