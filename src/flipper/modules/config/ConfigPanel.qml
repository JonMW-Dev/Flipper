import QtQuick
import QtQuick.Controls



Rectangle {
    id: configPanel

    height: 279
    width: 517

    clip: true
    color: palette.window

    Text {
        id: apiKeyLabel

        height: 15
        width: 49

        anchors.left: parent.left
        anchors.leftMargin: 10
        anchors.top: parent.top
        anchors.topMargin: 10

        color: palette.windowText
        font.family: "Inter"
        font.pixelSize: 12
        font.weight: Font.Normal
        horizontalAlignment: Text.AlignLeft
        text: qsTr("API_KEY")
        textFormat: Text.PlainText
        verticalAlignment: Text.AlignTop
    }
    TextField {
        id: apiKeyField


        anchors.left: parent.left
        anchors.right: parent.right
        anchors.leftMargin: 10
        anchors.rightMargin: 10
        anchors.top: parent.top
        anchors.topMargin: 35

        width: 497
        height: 34

        text: configModel.api_key // bind this text field to api_key
        onTextEdited: configModel.api_key = text //sets text in configModel
    }
    Text {
        id: urlLabel

        height: 15
        width: 25

        anchors.left: parent.left
        anchors.leftMargin: 10
        anchors.top: parent.top
        anchors.topMargin: 79

        color: palette.windowText
        font.family: "Inter"
        font.pixelSize: 12
        font.weight: Font.Normal
        horizontalAlignment: Text.AlignLeft
        text: qsTr("URL")
        textFormat: Text.PlainText
        verticalAlignment: Text.AlignTop
    }
    TextField {
        id: urlField

        height: 36
        width: 497

        anchors.left: parent.left
        anchors.right: parent.right
        anchors.leftMargin: 10
        anchors.rightMargin: 10
        anchors.top: parent.top
        anchors.topMargin: 104

        text: configModel.url
        onTextEdited: configModel.url = text
    }
    Text {
        id: modelLabel

        height: 15
        width: 37

        anchors.left: parent.left
        anchors.leftMargin: 10
        anchors.top: parent.top
        anchors.topMargin: 150

        color: palette.windowText
        font.family: "Inter"
        font.pixelSize: 12
        font.weight: Font.Normal
        horizontalAlignment: Text.AlignLeft
        text: qsTr("Model")
        textFormat: Text.PlainText
        verticalAlignment: Text.AlignTop
    }
    TextField {
        id: modelField

        height: 34
        width: 497

        anchors.left: parent.left
        anchors.right: parent.right
        anchors.leftMargin: 10
        anchors.rightMargin: 10
        anchors.top: parent.top
        anchors.topMargin: 175

        text: configModel.model
        onTextEdited: configModel.model = text
    }
    Text {
        id: localInfo

        height: 15
        width: 302

        anchors.left: parent.left
        anchors.leftMargin: 10
        anchors.top: parent.top
        anchors.topMargin: 219

        color: palette.windowText
        font.family: "Inter"
        font.pixelSize: 12
        font.weight: Font.Normal
        horizontalAlignment: Text.AlignLeft
        text: qsTr("Note: Local AI URL example: http://localhost:PORT/v1")
        textFormat: Text.PlainText
        verticalAlignment: Text.AlignTop
    }
    Rectangle {
        id: saveButton

        height: 25
        width: 497

        anchors.left: parent.left
        anchors.right: parent.right
        anchors.leftMargin: 10
        anchors.rightMargin: 10
        anchors.top: parent.top
        anchors.topMargin: 244

        color: "#00c417"
        radius: 4

        Text {
            id: saveButtonLabel

            anchors.fill: parent

            color: "#000000"
            font.family: "Inter"
            font.pixelSize: 12
            font.weight: Font.Normal
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: qsTr("Save Configuration")
            textFormat: Text.PlainText
        }

        MouseArea {
            anchors.fill: parent
            onClicked: configModel.save_config()
        }
    }
}