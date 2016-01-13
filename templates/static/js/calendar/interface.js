/**
 * Created by mk on 13.01.16.
 */
(function () {

    var DayInfoModel = Backbone.Model.extend({
        defaults: {
            day: 1,
            weekday: 1,
            month: 1,
            year: 2016,
            description: null
        },

        toJSON: function () {
            var attr = _.clone(this.attributes);
            delete attr.init_description;
            return attr
        },

        has_changed: function () {
            return this.get('description') != this.get('init_description');
        },

        reset: function () {
            this.set('init_description', this.description);
        }
    });

    var DayInfoView = Backbone.View.extend({
        render: function () {
            if (this.model.has_changed()) {
                this.$el.addClass('changed');
            } else {
                this.$el.removeClass('changed');
            }

            $(this.calendar_day_el).toggleClass('blank', !this.model.get('description'));
        },

        initialize: function () {
            var that = this;
            this.description_el = this.$el.find('.description')[0];
            this.calendar_day_el = $("#calendar-day-" + this.model.get('day'))[0];

            this.model.on('change', this.render, this);

            this.editor = CKEDITOR.inline(this.description_el, {
                extraPlugins: 'justify,sharedspace,pastefromword,colorbutton',
                removePlugins: 'maximize,resize',
                enterMode: CKEDITOR.ENTER_BR,
                shiftEnterMode: CKEDITOR.ENTER_P,
                sharedSpaces: {
                    top: 'topToolbar',
                    bottom: 'bottomToolbar'
                }
            });

            this.editor.on('change', function () {
                that.model.set('description', that.editor.getData());
            });

            this.model.set('init_description', this.editor.getData());
            this.model.set('description', this.editor.getData());
        }
    });

    var DaysCollection = Backbone.Collection.extend({
        save: function (url) {
            var items = new DaysCollection(this.filter(function(item) {
                return item.has_changed();
            }));

            if (!url) {
                return;
            }

            $.post(url, {
                'csrfmiddlewaretoken': $.cookie('csrftoken'),
                'items': JSON.stringify(items.toJSON())
            }).done(function () {
                InterfaceAlerts.showSuccess();
            });
        }
    });

    window.CalendarInterface = Backbone.View.extend({
        events: {
            'click button#save-calendar-button': 'saveCalendar'
        },

        saveCalendar: function () {
            this.days.save(this.save_url);
        },

        initialize: function () {
            this.days = new DaysCollection();
            this.save_url = this.$el.find("#save-calendar-button").data('url');
            var that = this;

            $(".day-info").each(function () {
                var model = new DayInfoModel({
                    day: $(this).data('day'),
                    weekday: $(this).data('weekday'),
                    month: $(this).data('month'),
                    year: $(this).data('year')
                });
                that.days.add(model);

                new DayInfoView({
                    el: this,
                    model: model
                })
            });
        }
    });

})();