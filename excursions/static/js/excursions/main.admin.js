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
            console.log("ajax done");
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
        var btn  = $("#yandex-map-update-button");
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
                console.log("form saved, about to reload");
                location.reload();
            })
        })
    }

    Init();
    InitYandexMapControl();
    InitSaveAction();
    InitGallery();
};
