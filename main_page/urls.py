from django.conf.urls import patterns, url

urlpatterns = patterns("main_page.views",
       url(r"item/activate$", "set_active"),
       url(r"item/list$", "list_items"),
       url(r"item/save$", "save_item"),
       url(r"item/add$", "add_item"),
       url(r"item/remove$", "remove_item"),
       url(r"themes/list", 'list_themes'),
       url(r"themes/set", 'set_current_theme'),
       url(r"toggle-border$", "toggle_border"),
       url(r"toggle-img-bootstrap-cols$", "toggle_img_bootstrap_cols"),
       url(r"update-description$", "update_description"),
       url(r"item$", "item"),
       url(r"$", "index"),
)