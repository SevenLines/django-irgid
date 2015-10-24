from django_assets import Bundle, register
from django_assets.env import get_env

get_env().append_path("templates/static")
get_env().append_path("excursions/static")

main_js = Bundle('bower/jquery/dist/jquery.min.js',
                 'bower/bootstrap/dist/js/bootstrap.min.js',
                 'bower/jquery.cookie/jquery.cookie.js',
                 'bower/jquery.lazyload/jquery.lazyload.min.js',
                 'bower/jquery-impromptu/dist/jquery-impromptu.min.js',
                 'js/lib/jquery.hypher.js',
                 'js/lib/jquery.scrollchaser.js',
                 # 'js/lib/modernizr.custom.42386.js',
                 'js/lib/ru.js',
                 'js/interface.js',
                 'js/excursions/main.guest.js',
                 filters="yui_js",
                 output="js/main.min.js")

main_css = Bundle('bower/bootstrap/dist/css/bootstrap.min.css',
                  'bower/jquery-impromptu/dist/jquery-impromptu.min.css',
                  'css/style.css',
                  'css/excursions.css',
                  filters="cssmin",
                  output="css/main.min.css")

register("main_js", main_js)
register("main_css", main_css)
