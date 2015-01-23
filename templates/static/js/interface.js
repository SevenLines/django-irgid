/**
 * Created by m on 09.01.15.
 */

dismissRelatedImageLookupPopup = function (win, chosenId, chosenThumbnailUrl, chosenDescriptionTxt) {
    var el;

    var name = win.name;

    if (el = document.getElementById(name + "_image_id")) {
        $(el).val(chosenId).trigger("change");
    }

    if (el = document.getElementById(name + "_image_url")) {
        if (el.tagName == "INPUT") {
            $(el).val(chosenThumbnailUrl).trigger("change");
        } else {
            el.src = chosenThumbnailUrl;
        }
    }

    if (RelatedImageLookupPopupBeforeClose) {
        RelatedImageLookupPopupBeforeClose(win, chosenId, chosenThumbnailUrl, chosenDescriptionTxt);
    }

    win.close();
};


(function () {
    function InterfaceAlerts() {
        var self = this;

        self.blink = function (color, delay) {
            var bg = $('body');
            var bg_css = bg.css("background");
            bg.css("background-color", color);
            setTimeout(function () {
                $("body").css("background", bg_css);
            }, delay);
        };

        self.showSuccess = function () {
            self.blink("#AAFF88", 1000);
        };
        self.showFail = function () {
            self.blink("#FFAA88", 1000);
        };
    }

    window.InterfaceAlerts = new InterfaceAlerts();
}());


$(function () {
    $("img.lazy").lazyload({});
    $("img.lazy.fadein").lazyload({
        effect: "fadeIn"
    });
});

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

window.input2base64f = function(input_element, callback) {
    var file = input_element.files[0];
    var fileReader = new FileReader();
    fileReader.onload = function (e) {
        if (callback) callback(e);
    };
    fileReader.readAsDataURL(file);
};

window.input2base64 = function (input_element, output_image) {
    input2base64f(input_element, function (r) {
        output_image.src = e.target.result;
    });
};


