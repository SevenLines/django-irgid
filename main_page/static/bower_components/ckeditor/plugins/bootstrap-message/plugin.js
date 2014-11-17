/**
 * Created by m on 06.10.14.
 */
CKEDITOR.plugins.add('bootstrap-message', {
    icons: "message",

    init: function (editor) {
        editor.addCommand("addMainPageMessage", new CKEDITOR.dialogCommand("mainPageMessageDialog"));
        CKEDITOR.dialog.add("mainPageMessageDialog", this.path + "dialogs/mainPageMessageDialog.js");
        editor.ui.addButton("btnAddMainPage", {
            label: 'Add bootstrap message',
            command: 'addMainPageMessage',
            toolbar: 'insert',
            icon : this.path + 'icons/message.png'
        });
        console.log("hi");
        if (editor.contextMenu) {
            editor.addMenuGroup("bootstrapMessageGroup");
            editor.addMenuItem("bootstrapMessageItem", {
                label: "Edit message",
                command: "addMainPageMessage",
                group: "bootstrapMessageGroup"
            });
            editor.contextMenu.addListener(function (element) {
                if ($(element.$).hasClass("main-page-message")) {
                    return {
                        bootstrapMessageItem: CKEDITOR.TRISTATE_OFF
                    };
                }
            })
        }
    }
});