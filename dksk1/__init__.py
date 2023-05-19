###
#   Bu dosya web app'imizi oluşturmak için yazdığımız kodları içerir
###

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATİONS'] = False  # uyarılarla alakalı bir şey. olmasa da olur.
app.config['SECRET_KEY'] = 'os6400'  # secret_key belirlemeden form kullanamıyoruz. Bu anahtar ilerleyen aşamalarda environment değişkeni olarak verilecek güvenlik sebebiyle. Ancak şu anda geliştirmedeyiz.
app.app_context().push()  # app_context() sağlanmadan database kullanamıyoruz flaskın yeni versiyonlarda. Bu satır olmadan hiçbir şey çalışmıyor.

# Burada da app imizde kullanacağımız class'lar için instancelarımızı oluşturduk
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from dksk1 import routes # sonda import ettik çünkü öteki türlü circular importa sebep olurdu