(function () {
    function ExcursionCategoryModel(form, data) {
        var self = this;

        self.url = {
            set_image: data.url.set_image,
            rmv_image: data.url.rmv_image,
            set_visible: data.url.set_visible
        };
        self.csrf = data.csrf;

        self.id = $(form).data('id');

        self.visible = ko.observable($(form).data('visible'));

        self.imageUrl = ko.observable($(form).data('image-url'));
        self.old_imageUrl = ko.observable(self.imageUrl());

        self.changed = ko.computed(function () {
            return self.old_imageUrl() != self.imageUrl()
        });

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

            formData.append("image", form.category_image_input.files[0]);
            formData.append("id", self.id);
            formData.append("csrfmiddlewaretoken", self.csrf);
            $.ajax({
                url: self.url.set_image,
                data: formData,
                type: "POST",
                contentType: false,
                processData: false
            }).done(function (r) {
                self.imageUrl(r);
                self.old_imageUrl(self.imageUrl());
            })
        };

        self.toggle = function () {
            $.get(self.url.set_visible, {
                id: self.id,
                visible: !self.visible()
            }).done(function (r) {
                self.visible(!self.visible());
                InterfaceAlerts.showSuccess();
            }).fail(InterfaceAlerts.showFail());
        };

        Init();
    }

    window.ExcursionCategoryModel = ExcursionCategoryModel;
})();


