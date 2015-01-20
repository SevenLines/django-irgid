window.ExcursionPriceComputer = function (price_list) {
    var item, price;
    var formPriceCalculator = document.forms['price-calculator'];
    var cookie_settings = {expires: 7, path: '/'};

    var compute_price = function () {
        var adults_count = parseInt(formPriceCalculator.adults_count.value) || 0;
        var children_count = parseInt(formPriceCalculator.children_count.value) || 0;
        var ppl_count = adults_count + children_count;

        $.cookie("adults_count", adults_count, cookie_settings);
        $.cookie("children_count", children_count, cookie_settings);

        for (var i = 0; i < price_list.length; ++i) {
            item = price_list[i];
            if (item[0] <= ppl_count && ppl_count <= item[1]) {
                console.log(item);
                price = adults_count * item[3] + children_count * item[2] + item[4];
                $("#priceOut").text(price);
                if (item[4] && !item[3] && !item[2]) {
                    $("#priceAdult").text(~~(item[4] / ppl_count));
                    $("#priceChildren").text(~~(item[4] / ppl_count));
                } else {
                    $("#priceAdult").text(item[3]);
                    $("#priceChildren").text(item[2]);
                }
                return;
            }
        }
        item = price_list[price_list.length - 1];
        price = adults_count * item[3] + children_count * item[2] + item[4];
        $("#priceOut").text(price);
    };
    $(formPriceCalculator).find("input[type=text]").on("input change", compute_price);

    formPriceCalculator.adults_count.value = $.cookie("adults_count") || 1;
    formPriceCalculator.children_count.value = $.cookie("children_count") || 12;

    compute_price();
};

// left menu fixed control
$(function () {
    var $menu = $(".list-group-menu").first();
    var $parent = $(".container-content").first();
    if ($menu.length) {
        var top = $menu.position().top - 10;
        var check = false;
        var event = function () {
            if ($menu.height() < $(this).height() && $(this).scrollTop() > top) {
                $menu.css({
                    position: "fixed",
                    top: 10
                });
                check = true;
            } else if (check) {
                $menu.css({
                    position: "",
                    top: ""
                });
                check = false;
            }
        };
        $(window).scroll(event).resize(event);
    }
});

$(function () {
    if (!$("html").is(".lt-ie9, .lt-ie8, .lt-ie7")) {
        $('#excursion-description, .description').hyphenate('ru');
    }
});
