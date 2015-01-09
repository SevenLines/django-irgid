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

        $(".excursion-form").submit(function () {
            var title = $("#excursion-title").html();
            var description = $("#excursion-description").html();
            var short_description = $("#excursion-short-description").html();
            var price_list = $("#excursion-price-list")[0].value;

            var formData = new FormData();
            console.log(this.small_image.dataset.changed);
            if (this.small_image.dataset.changed) {
                formData.append("small_image", this.small_image.files[0]);
            }
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
            }).fail(function () {
                InterfaceAlerts.showFail();
            });

            return false;
        });
    }

    Init();
};

$(function () {
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

    var galleryItem = $(".excursion-gallery");
    galleryItem.on("click", ".add-image", function () {
        var currentItem = $(this).parent();
        var fileSelector = galleryItem.find(".add-image-selector");

        fileSelector.one("change", function () {
            var newItem = $('<div class="excursion-gallery-item"></div>');
            var newImage = $('<img />');
            newItem.append(newImage);
            newItem.insertBefore(currentItem);

            var file = this.files[0];
            var fileReader = new FileReader();
            fileReader.onload = function (e) {
                newImage.attr("src", e.target.result);
            };
            fileReader.readAsDataURL(file);

            $(this).removeClass("add-image-selector");
            $(this).appendTo(newItem);

            galleryItem.append('<input type="file" class="add-image-selector">');
        });
        fileSelector.click();
    });
});
