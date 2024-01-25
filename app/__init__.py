# our main app
from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

# manage users
from flask_ldap3_login import LDAP3LoginManager

ldaplogin_manager = LDAP3LoginManager(app)

from flask_login import LoginManager

login_manager = LoginManager(app)
login_manager.login_view = 'home.login'
login_manager.login_message = 'Для доступа к этой странице нужно авторизоваться'

users = {}

# register blueprints
from .home import home
app.register_blueprint(home)
from .alias import alias
app.register_blueprint(alias, url_prefix='/alias')
from .proxy import proxy
app.register_blueprint(proxy, url_prefix='/proxy')