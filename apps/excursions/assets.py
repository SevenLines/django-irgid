from django_assets import Bundle, register
from django_assets.env import get_env

get_env().append_path("templates/static")
get_env().append_path("excursions/static")

excursions_admin_js = Bundle(
    'bower/Sortable/Sortable.min.js',
    'bower/knockout/dist/knockout.js',
    'js/excursions/admin/ExcursionCategoryModel.js',
    'js/excursions/admin/SaveCategoriesButtonModel.js',
    'js/excursions/admin/ExcursionModel.js',
    filters="yui_js",
    output="js/excursions/main.min.js")

register("excursions_admin_js", excursions_admin_js)
