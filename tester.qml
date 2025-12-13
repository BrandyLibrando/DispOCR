import QtQuick
import QtQuick.Controls

ApplicationWindow {
    visible: true
    width: 400
    height: 300
    title: "Folder Selector Example"



    FolderSelectButton {
        id:  folderSelect
        text: "hi there"
    }
}
