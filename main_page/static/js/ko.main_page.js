function MainPageItem(data) {
    var self = this;

    self.id = data.id;
    self.title = ko.observable(data.title);
    self.description = ko.observable(data.description);
    self.item_url = ko.observable(data.item_url);
    self.item_thumb_url = ko.observable(data.item_thumb_url);
    self.active = ko.observable(data.active);
}


function MainPageModel(data) {
    var self = this;

    self.reset_item = function () {
        return new MainPageItem({
            id: -1,
            title: '',
            description: '',
            item_url: '',
            item_thumb_url: '',
            active: false
        });
    };

    self.url = {
        items: data.url.items,                  // list of items
        item: data.url.item,                    // item with specific item_id
        activate_item: data.url.activate_item,  // activate currently selected item
        save_item: data.url.save_item,          // save item with specific item_id
        add_item: data.url.add_item,            // add new item
        remove_item: data.url.remove_item,      // remove item with id
        toggle_border: data.url.toggle_border,  // toggle main image border
        toggle_img_bootstrap_cols: data.url.toggle_img_bootstrap_cols,
        update_description: data.url.update_description,

        themes: data.url.themes,
        set_theme: data.url.set_theme
    };

    self.description = ko.observable("");
    self.show_border = ko.observable(data.show_border);

    self.selector = {
        view: data.selector.view
    };

    self.cols = $.map($(Array(14)), function (val, i) {
        return i - 1;
    });
    self.img_bootstrap_cols = ko.observable(data.img_bootstrap_cols);

    self.modalSave = new ModalConfirm({ modal_selector: "#modalSave" });
    self.modalDelete = new ModalConfirm({
        variable_name: "modalDelete",
        message: "Удалить?"
    });
    self.new_item = ko.observable(self.reset_item());

    self.csrf = data.csrf;
    function csrfize(data) {
        data.csrfmiddlewaretoken = self.csrf;
        return data;
    }

    self.items = ko.observableArray();
    self.current_item = ko.observable(self.reset_item());

    self.themes = ko.observableArray();
    self.current_theme = ko.observable();
    self.init_current_theme = ko.observable();

    self.img_bootstrap_cols.subscribe(function (value) {
        console.log(value);
        self.toggleImgBootstrapCols();
    });

    self.current_theme.subscribe(function (value) {
        if (self.current_theme() && self.init_current_theme() && self.current_theme().path != self.init_current_theme().path) {
            $.post(self.url.set_theme, csrfize({
                'css_path': value.path
            })).success(function () {
                InterfaceAlerts.showSuccess();
                self.init_current_theme(self.current_theme());
                location.reload();
            }).fail(function () {
                InterfaceAlerts.showFail();
            })
        }
    });

    self.style = ko.computed(function () {
        var s = self.show_border() ? 'glyphicon-eye-open' : 'glyphicon-eye-close';
        return s;
    }, self.show_border);

    // binding ckeditor with description content
    ko.bindingHandlers.ckeditor = {
        init: function (element) {
            var editor = $(element).ckeditor({
                extraPlugins: 'divarea,bootstrap-collapse,insertpre,div,image,' +
                'bootstrap-collapse,bootstrap-message,showblocks,justify,divarea,colordialog,colorbutton,liststyle,eqneditor'
            }).editor;
            self.description(editor.getData());
            editor.on('change', function (data) {
                self.description(editor.getData());
            });

            // create save button
            editor.addCommand("SaveCommand", {
                exec: function () {
                    self.update_description();
                }
            });
            editor.ui.addButton("Save", {
                command: "SaveCommand",
                label: "Save",
                icon: element.dataset.icon,
                toolbar: "editing"
            });
            // <<<
        },
        update: function (element) {
            var value = self.description();
            //console.log(value);
            if ($(element).val() !== value) {
                $(element).val(value);
            }
        }
    };
    // <<<
    self.loadThemes = function () {
        $.get(self.url.themes).success(function (response) {
            self.themes(response);
            self.themes().every(function (item) {
                if (item.current) {
                    self.init_current_theme(item);
                    return false;
                }
                return true;
            });
            if (self.init_current_theme()) {
                self.current_theme(self.init_current_theme());
            }
        });
    };

    self.loadItems = function (select_newest_item) {
        $.get(self.url.items, {}, function (data) {
            self.current_item(self.reset_item());
            self.items($.map(data, function (item) {
                return new MainPageItem(item);
            }));

            for (var i = 0; i < self.items().length; ++i) {
                if (select_newest_item) {
                    self.current_item(self.items()[i]);
                    break;
                }
                if (self.items()[i].active()) {
                    self.current_item(self.items()[i]);
                    break;
                }
            }
            self.update_view();
        })
    };

    self.activateItem = function (data) {
        self.current_item(data);

        $.post(self.url.activate_item, {
            item_id: data.id,
            csrfmiddlewaretoken: self.csrf
        }).success(function () {
            self.update_view();
            self.loadItems();
        })
    };

    self.update_view = function () {
        if (self.current_item === 'undefined')
            return;
        $.post(self.url.item, csrfize({
            item_id: self.current_item().id
        })).success(function (data) {
            $(self.selector.view).html(data.html);
        }).fail(function (data) {
            $(self.selector.view).html("");
        });
    };

    self.selectItem = function (data) {
        self.current_item(data);
        self.update_view()
    };

    self.saveItem = function () {
        $.post(self.url.save_item, csrfize({
            item_id: self.current_item().id,
            description: self.current_item().description(),
            title: self.current_item().title(),
            item_url: self.current_item().item_url
        })).success(function () {
            InterfaceAlerts.showSuccess();
            self.update_view();
        }).fail(function () {
            InterfaceAlerts.showFail();
        });
    };

    self.update_description = function () {
        console.log(self.description());
        $.post(self.url.update_description, csrfize({
            description: self.description()
        })).success(function() {
            InterfaceAlerts.showSuccess();
            self.update_view();
        }).fail(function () {
            InterfaceAlerts.showFail();
        })
    };

    self.removeItem = function (data) {
        self.modalDelete.show(function () {
            $.post(self.url.remove_item, csrfize({
                item_id: data.id
            })).success(function () {
                InterfaceAlerts.showSuccess();
                self.items.remove(data);
            }).fail(function () {
                InterfaceAlerts.showFail();
            })
        });
    };

    self.toggleBorder = function () {
        $.post(self.url.toggle_border, csrfize({
            show_border: self.show_border()
        })).done(function () {
            self.show_border(!self.show_border());
            self.update_view();
            InterfaceAlerts.showSuccess();
        }).fail(function () {
            InterfaceAlerts.showFail();
        });
    };

    self.toggleImgBootstrapCols = function () {
        $.post(self.url.toggle_img_bootstrap_cols, csrfize({
            img_bootstrap_cols: self.img_bootstrap_cols()
        })).done(function () {
            self.update_view();
            InterfaceAlerts.showSuccess();
        }).fail(function() {
            InterfaceAlerts.showFail();
        });
    }

    self.addItem = function (form) {
        var file_dialog = $(form).find("[name='file']").first();

        // unbind onchange event to avoid overbinding
        file_dialog.unbind("change");
        file_dialog.on("change", function () {
            // create preview of uploaded file
            var reader = new FileReader();
            reader.onload = function (e) {
                $("img#preview").attr('src', e.target.result)
            };
            reader.readAsDataURL(file_dialog[0].files[0]);

            // show modal form
            self.modalSave.message("Создать новый вид");
            self.modalSave.show(function () {
                var formData = new FormData(form);
                $.ajax({
                    url: self.url.add_item,
                    data: formData,
                    processData: false,
                    contentType: false,
                    type: 'POST',
                    success: function () {
                        self.loadItems(true);
                    }
                });
            });
        });

        // open file selection dialog
        file_dialog.click();
    };


    self.loadItems();
    self.loadThemes();
}

$(function () {

});
