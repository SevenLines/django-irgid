from django_assets import Bundle, register
from django_assets.env import get_env

get_env().append_path("templates/static")

main_js = Bundle('bower/jquery/dist/jquery.min.js',
                 'bower/bootstrap/dist/js/bootstrap.min.js',
                 'js/interface.js',
                 filters="yui_js",
                 output="js/main.min.js")

main_css = Bundle('bower/bootstrap/dist/css/bootstrap.min.css',
                  'css/style.css',
                  filters="cssmin",
                  output="css/main.min.css")

register("main_js", main_js)
register("main_css", main_css)
