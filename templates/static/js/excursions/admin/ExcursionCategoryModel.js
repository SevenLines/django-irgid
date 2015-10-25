(function () {
    function ExcursionCategoryModel(form, data) {
        var self = this;
        self.model = data.model;
        self.url = {
            set_image: data.url.set_image,
            rmv_image: data.url.rmv_image,
            rmv_category: data.url.rmv_category,
            set_visible: data.url.set_visible,
            save_category: data.url.save_category
        };
        self.csrf = data.csrf;

        self.id = $(form).data('id');

        self.title = ko.observable($(form).data('title'));
        self.old_title = ko.observable($(form).data('title'));
        self.description = ko.observable($(form).data('description'));
        self.old_description = ko.observable($(form).data('description'));

        self.visible = ko.observable($(form).data('visible'));
        self.is_gallery = ko.observable($(form).data('is_gallery'));
        self.old_is_gallery = ko.observable(self.is_gallery());

        self.imageUrl = ko.observable($(form).data('image-url'));
        self.old_imageUrl = ko.observable(self.imageUrl());

        self.changed = ko.computed(function () {
            return self.old_imageUrl() != self.imageUrl() ||
                self.old_title() != self.title() ||
                self.old_is_gallery() != self.is_gallery() ||
                self.old_description() != self.description()
        });

        function Reset() {
            self.old_title(self.title());
            self.old_description(self.description());
            self.old_is_gallery(self.is_gallery());
            self.old_imageUrl(self.imageUrl());
        }

        function Init() {
            $(form.category_image_input).change(function () {
                input2base64f(this, function (e) {
                    self.imageUrl(e.target.result);
                });
            });
        }

        self.removeImage = function () {
            if (!self.old_imageUrl()) {
                self.imageUrl(null);
                return;
            }

            if (self.old_imageUrl() != self.imageUrl()) {
                self.imageUrl(self.old_imageUrl());
                return;
            }

            $.prompt("Удалить изображение?", {
                title: 'Подтвердите',
                buttons: {"Удалить": true, "Пока не надо": false},
                persistent: false,
                submit: function (e, confirmed) {
                    if (confirmed) {
                        $.get(self.url.rmv_image, {
                            id: self.id
                        }).done(function () {
                            self.old_imageUrl(null);
                            self.imageUrl(null);
                            InterfaceAlerts.showSuccess();
                        }).fail(InterfaceAlerts.showFail);
                    }
                }
            });
        };

        self.selectImage = function () {
            form.category_image_input.click();
        };

        self.save = function () {
            var formData = new FormData();

            if (form.category_image_input.files.length) {
                formData.append("image", form.category_image_input.files[0]);
            }
            formData.append("id", self.id);
            formData.append("title", self.title());
            formData.append("is_gallery", self.is_gallery());
            formData.append("description", self.description());
            formData.append("csrfmiddlewaretoken", self.csrf);

            $.ajax({
                url: self.url.save_category,
                data: formData,
                type: "POST",
                contentType: false,
                processData: false
            }).done(function (r) {
                Reset();
            })
        };

        var $edit_template = $("#edit-template");
        var $edit_template_content = $($edit_template.children()[0]);
        self.edit = function () {
            self.model.currentItem(self);
            $.prompt("Экскурсия", {
                title: 'Редактировать',
                persistent: false,
                submit: function (e, confirmed) {
                    if (confirmed) {

                    }
                },
                close: function () {
                    $edit_template_content.appendTo($edit_template);
                },
                loaded: function () {
                    var $msg = $(this).find(".jqimessage");
                    $msg.html("");
                    $edit_template_content.appendTo($msg);
                },
                promptspeed: 0
            });
        };

        self.remove = function () {
            $.prompt("Удалить категорию \"" + self.title() + "\"?", {
                title: 'Подтвердите',
                buttons: {"Удалить": true, "Пока не надо": false},
                persistent: false,
                submit: function (e, confirmed) {
                    if (confirmed) {
                        $.get(self.url.rmv_category, {
                            id: self.id
                        }).done(function () {
                            location.reload()
                        }).fail(InterfaceAlerts.showFail);
                    }
                }
            });
        };

        self.toggle = function () {
            $.get(self.url.set_visible, {
                id: self.id,
                visible: !self.visible()
            }).done(function (r) {
                self.visible(!self.visible());
                InterfaceAlerts.showSuccess();
            }).fail(InterfaceAlerts.showFail);
        };

        self.setAsGallery = function () {
            self.model.setAsGallery(self);
        };

        Init();
    }

    window.ExcursionCategoryModel = ExcursionCategoryModel;
})();


