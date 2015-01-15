function TextPageModel(save_url, upload_image, remove_image, id) {

    var editor = CKEDITOR.inline("page-content", {
        enterMode: CKEDITOR.ENTER_BR,
        extraPlugins: 'sourcedialog,showblocks,justify,colordialog,colorbutton,liststyle',
        //removePlugins: 'image',
        extraAllowedContent: 'img[data-id]'
    });

    var images_to_delete = [];
    editor.addCommand("save", { // create named command
        exec: function (edt) {

            // save text
            function save_text() {
                $.post(save_url, {
                    text: edt.getData(),
                    csrfmiddlewaretoken: $.cookie('csrftoken'),
                    id: id
                }).done(function () {
                    InterfaceAlerts.showSuccess();
                }).fail(function () {
                    InterfaceAlerts.showFail();
                });
            }

            var inputs = $("#images-form input[type=file]");
            var ajaxesLeft = inputs.length + images_to_delete.length;
            // first save images and rewrite it src attributes
            inputs.each(function () {
                var that = this;
                setTimeout(function () {
                    var num = $(that).data("num");

                    if ($("#image" + num).length > 0) {
                        var formData = new FormData();
                        formData.append("image", that.files[0]);
                        formData.append("csrfmiddlewaretoken", $.cookie('csrftoken'));
                        $.ajax({
                            url: upload_image,
                            type: "POST",
                            data: formData,
                            processData: false,
                            contentType: false
                        }).done(function (r) {
                            var img = $("#image" + num);
                            $(that).remove();
                            img.attr("src", r.url);
                            img.removeAttr("id");
                            img.attr("data-id", r.id);
                        }).always(function () {
                            ajaxesLeft--;
                            if (ajaxesLeft == 0) {
                                save_text();
                            }
                        })
                    }
                }, 0);
            });
            // remove existing images
            for (var i = 0; i < images_to_delete.length; ++i) {
                var im = $("img[data-id=" + images_to_delete[i] + "]");
                if (!im.length) {
                    $.get(remove_image, {
                        id: images_to_delete[i]
                    }).always(function () {
                        --ajaxesLeft;
                        if (ajaxesLeft == 0) {
                            save_text();
                        }
                    });
                } else {
                    --ajaxesLeft;
                    if (ajaxesLeft == 0) {
                        save_text();
                    }
                }
            }

            if (ajaxesLeft == 0) {
                save_text();
            }

        }
    });

    editor.on("instanceReady", function () {
        $(".textpage-content").bind("DOMNodeRemoved", function (e) {
            if (e.target.tagName == "IMG") {
                var id = $(e.target).data("id");
                if (id) {
                    images_to_delete.push(id);
                }
            }
        });
    });

    var images_count = 0;
    editor.addCommand("add_image", { // create named command
        exec: function (edt) {
            var input = $('<input type="file" style="display: none;" accept="image/*">');
            input.on("change", function () {
                var num = ++images_count;
                var el = edt.document.createElement("img");
                $(el.$).attr("id", "image" + num);
                $(el.$).data("num", num);
                input.attr("id", "input" + num);
                input.data("num", num);

                input2base64(input[0], el.$);
                edt.insertElement(el);

                $("#images-form").append(input);
            });
            input.click();
        }
    });

    editor.ui.addButton('SaveButton', { // add new button and bind our command
        label: "Save",
        command: 'save',
        toolbar: 'clipboard',
        icon: '/static/bower/ckeditor/plugins/save/icons/save.png'
    });

    editor.ui.addButton('AddImageButton', { // add new button and bind our command
        label: "Image",
        command: 'add_image',
        toolbar: 'insert',
        icon: '/static/images/icon_picture.png'
    });

}