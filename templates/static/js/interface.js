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

    function TableEffects() {
        var self = this;
        self.toggleColumnClass = function (td_target, class_name, toggle) {
            var t = parseInt($(td_target).index()) + 1;
            $('td:nth-child(' + t + ')').toggleClass(class_name, toggle);
        }
    }

    window.TableEffects = new TableEffects();
    window.InterfaceAlerts = new InterfaceAlerts();
}());


$(function() {
    $("img.lazy").lazyload({
    });
    $("img.lazy.fadein").lazyload({
        effect : "fadeIn"
    });
});