(function () {
    function SaveCategoriesButtonModel(data) {
        var self = this;

        self.url = {
            set_order: data.url.set_order,
            set_image: data.url.set_image,
            rmv_image: data.url.rmv_image,
            set_visible: data.url.set_visible
        };
        self.csrf = data.csrf;
        self.currentItem = ko.observable();

        self.items = ko.observableArray();

        self.init_order = ko.observable("");
        self.order = ko.observable("");

        self.currentItemTitle = ko.computed(function () {
            if (self.currentItem()) {
                return self.currentItem().title;
            }
            return "";
        });

        self.currentItemDescription = ko.computed(function () {
            if (self.currentItem()) {
                return self.currentItem().description;
            }
            return null;
        });

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
                        rmv_image: self.url.rmv_image,
                        set_visible: self.url.set_visible
                    },
                    csrf: self.csrf,
                    model: self
                });
                self.currentItem(model);
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
})();