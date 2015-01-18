window.ExcursionModel = function (data) {
    var self = this;
    self.excursion_id = data.id;
    self.csrf = data.csrf;

    self.$excursionForm = $(".excursion-form");

    function Init() {
        var editor_config = {
            enterMode: CKEDITOR.ENTER_BR,
            extraPlugins: 'sourcedialog,showblocks,justify,colordialog,colorbutton,liststyle'
        };

        CKEDITOR.disableAutoInline = true;
        CKEDITOR.inline('excursion-description', editor_config);


        $(".image-selector").on("change", function () {
            var that = this;
            if (that.files.length > 0) {
                var file = that.files[0];
                var fileReader = new FileReader();
                fileReader.onload = function (e) {
                    $(that).siblings("img")[0].src = e.target.result;
                };
                fileReader.readAsDataURL(file);
            }
            that.dataset['changed'] = 1;
        }).each(function (i, item) {
            var that = this;
            $(that).parent().find("img").click(function () {
                $(that).click();
            });
        });
    }

    self.Save = function (form, oncomplete) {
        var title = $("#excursion-title").html();
        var description = $("#excursion-description").html();
        var short_description = $("#excursion-short-description").html();
        var price_list = $("#excursion-price-list")[0].value;
        var yandex_map_script = $("#yandexmapscript-input")[0].value;

        var formData = new FormData();
        if (form.small_image.dataset.changed) {
            formData.append("small_image", form.small_image.files[0]);
        }

        var hasNewImageInGallery = false;
        $(form).find(".excursion-gallery .excursion-gallery-item input[type=file]").each(function () {
            formData.append("gallery[]", this.files[0]);
            hasNewImageInGallery = true;
        });

        formData.append("id", self.excursion_id);
        formData.append("csrfmiddlewaretoken", self.csrf);
        formData.append("title", title.trim());
        formData.append("description", description.trim());
        formData.append("short_description", short_description.trim());
        formData.append("yandex_map_script", yandex_map_script.trim());
        formData.append("price_list", price_list.trim());

        $.ajax({
            url: form.action,
            type: "POST",
            data: formData,
            processData: false,
            contentType: false
        }).done(function () {
            InterfaceAlerts.showSuccess();
            if (oncomplete)
                oncomplete();

            if (hasNewImageInGallery) {
                location.reload();
            }
        }).fail(function () {
            InterfaceAlerts.showFail();
        });
    };

    function InitSaveAction() {
        self.$excursionForm.submit(function () {
            self.Save(this);
            return false;
        });
    }

    function InitGallery() {
        var galleryItem = $(".excursion-gallery");

        // click on remove button
        galleryItem.on('click', ".remove", function () {
            var that = this;
            if (this.dataset.action) {
                $.prompt("Удалить изображение?", {
                    title: 'Подтвердите',
                    buttons: {"Удалить": true, "Пока не надо": false},
                    persistent: false,
                    submit: function (e, confirmed, m, f) {
                        if (confirmed) {
                            $.post(that.dataset.action, {
                                csrfmiddlewaretoken: self.csrf
                            }).done(function () {
                                $(that).parent().parent().remove();
                            }).fail(function () {
                                InterfaceAlerts.showFail();
                            })
                        }
                    },
                    overlayspeed: 'fast',
                    promptspeed: 0,
                    show: 'fadeIn'
                });
            } else {
                $(this).parent().parent().remove();
            }
        });


        var template = $("#gallery-item-template").html();
        var addItem = $("#add-image");
        addItem.click(function () {
            var item = $(template);
            var selector = item.find("input[type=file]");
            selector.one("change", function () {
                var file = this.files[0];
                var fileReader = new FileReader();
                fileReader.onload = function (e) {
                    item.find("img").attr("src", e.target.result)
                };
                fileReader.readAsDataURL(file);
                item.insertBefore(addItem.parent());
            });
            selector.click();
        });
    }

    function InitYandexMapControl() {
        var input = $("#yandexmapscript-input");
        var btn = $("#yandex-map-update-button");
        input.on("change", function () {
            var re = /\?sid=([\w-]+)?/g;
            var matches = re.exec(this.value);
            if (matches) {
                this.value = matches[1];
            }

            // убираем width и height теги
            //this.value = this.value.replace(/&(width|height)=(\d+)/g, "") ;
        });
        btn.on("click", function () {
            self.Save(self.$excursionForm[0], function () {
                location.reload();
            })
        })
    }

    Init();
    InitYandexMapControl();
    InitSaveAction();
    InitGallery();
};


function ExcursionCategoryModel(form, data) {
    var self = this;

    self.url = {
        set_image: data.url.set_image,
        rmv_image: data.url.rmv_image
    };
    self.csrf = data.csrf;

    self.id = $(form).data('id');

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

    Init();
}

function SaveCategoriesButtonModel(data) {
    var self = this;

    self.url = {
        set_order: data.url.set_order,
        set_image: data.url.set_image,
        rmv_image: data.url.rmv_image
    };
    self.csrf = data.csrf;

    self.items = ko.observableArray();

    self.init_order = ko.observable("");
    self.order = ko.observable("");

    self.visible = ko.computed(function () {
        for (var i = 0; i < self.items().length; ++i) {
            if (self.items()[i].changed()) {
                return true;
            }
        }
        return self.init_order() != self.order();
    });

    function get_order() {
        var _order = {};
        $("#categories-list .category-form").each(function (i, item) {
            _order[$(this).data('id')] = i;
        });
        return JSON.stringify(_order);
    }

    function Init() {
        $("#categories-list .category-element .category-form").each(function (i, item) {
            var model = new ExcursionCategoryModel(this, {
                url: {
                    set_image: self.url.set_image,
                    rmv_image: self.url.rmv_image
                },
                csrf: self.csrf
            });
            self.items.push(model);
            ko.applyBindings(model, this)
        });
        self.init_order(get_order());
        self.order(self.init_order());

        new Sortable(document.getElementById("categories-list"), {
            animation: 300,
            onUpdate: function () {
                self.order(get_order());
            }
        });
    }

    self.save = function () {
        $.post(self.url.set_order, {
            order: get_order(),
            csrfmiddlewaretoken: self.csrf
        }).done(function () {
            InterfaceAlerts.showSuccess();
            self.init_order(self.order());
        });

        ko.utils.arrayForEach(this.items(), function (i) {
            if (i.changed()) {
                i.save();
            }
        })
    };

    Init();
}

window.SaveCategoriesButtonModel = SaveCategoriesButtonModel;