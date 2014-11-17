CKEDITOR.dialog.add("mainPageMessageDialog", function (editor) {
    return {
        title: 'Bootstrap message',
        minWidth: 400,
        minHeight: 200,

        contents: [
            {
                id: 'tab-basic',
                label: 'Basic Settings',
                elements: [
                    {
                        type: 'textarea',
                        id: 'message',
                        label: 'Message',
                        validate: CKEDITOR.dialog.validate.notEmpty("Message field cannot be empty."),

                        setup: function (element) {
                            this.setValue(element.getHtml());
                        },
                        commit: function (element) {
                            element.setHtml(this.getValue());
                        }
                    },
                    {
                        type: 'select',
                        id: 'type',
                        label: 'Type',
                        default: '',
                        items: [
                            ['<none>', ''],
                            ['info', 'alert-info'],
                            ['success', 'alert-success'],
                            ['warning', 'alert-warning'],
                            ['danger', 'alert-danger']
                        ],
                        setup: function (element) {
                            var that = this;
                            if (this.items.every(function (item) {
                                    if (element.hasClass(item[1])) {
                                        that.setValue(item[1]);
                                        return false;
                                    }
                                    return true;
                                })) {
                                this.setValue("");
                            }
                        },
                        commit: function (element) {
                            this.items.every(function (item) {
                                element.removeClass(item[1]);
                                return true;
                            });
                            element.addClass(this.getValue());
                        }
                    }
                ]
            }
        ],

        onOk: function () {
            var dialog = this;
            if (dialog.insertMode) {
                var description = dialog.getValueOf('tab-basic', 'message');
                var cls = dialog.getValueOf('tab-basic', 'type');
                editor.insertHtml('<div class="main-page-message ' + cls + '">' + description + '</div>');
            } else {
                dialog.commitContent(dialog.element);
            }
        },

        onShow: function () {
            var selection = editor.getSelection();
            var element = selection.getStartElement();
            this.element = element;
            if ($(element.$).hasClass('main-page-message')) {
                this.insertMode = false;
                this.setupContent(element);
            } else {
                this.insertMode = true;
            }
        }
    };
});
