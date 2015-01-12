window.ExcursionModel = function (data) {
    var self = this;
    self.excursion_id = data.id;
    self.csrf = data.csrf;

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

    function InitSaveAction() {
        $(".excursion-form").submit(function () {

            var title = $("#excursion-title").html();
            var description = $("#excursion-description").html();
            var short_description = $("#excursion-short-description").html();
            var price_list = $("#excursion-price-list")[0].value;

            var formData = new FormData();
            if (this.small_image.dataset.changed) {
                formData.append("small_image", this.small_image.files[0]);
            }

            var hasNewImageInGallery = false;
            $(this).find(".excursion-gallery .excursion-gallery-item input[type=file]").each(function () {
                formData.append("gallery[]", this.files[0]);
                hasNewImageInGallery = true;
            });

            formData.append("id", self.excursion_id);
            formData.append("csrfmiddlewaretoken", self.csrf);
            formData.append("title", title.trim());
            formData.append("description", description.trim());
            formData.append("short_description", short_description.trim());
            formData.append("price_list", price_list.trim());

            $.ajax({
                url: this.action,
                type: "POST",
                data: formData,
                processData: false,
                contentType: false
            }).done(function () {
                InterfaceAlerts.showSuccess();
                if (hasNewImageInGallery) {
                    location.reload();
                }
            }).fail(function () {
                InterfaceAlerts.showFail();
            });

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

    Init();
    InitSaveAction();
    InitGallery();
};
