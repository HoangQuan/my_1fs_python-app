### Python with Flask (Chap 1) - get started

- Intall python
- Virtualenv
- Flask

#### 1. Python: Already installed If you don't have it installed, you can download it here.

#### 2. Vitualenv

  sudo apt install python-pip
  pip install virtualenv
  pip install virtualenvwrapper
  export WORKON_HOME=~/Envs
  sudo find / -name virtualenvwrapper.sh

  source /home/hoangquan/.local/bin/virtualenvwrapper.sh

  which virtualenvwrapper.sh
  
  Create env

  mkvirtualenv my-venv
  workon my-venv

mkdir happy_share
cd happy_share/

#### 3. install Flask

pip install Flask

#### 4. Database setup

We use Flask-SQLAlchemy for Object Relationship Mapper in 
PythonMySQL-python for Use a interface to MySQL


pip install flask-sqlalchemy mysql-python

#### 5. Config

Make config file 

touch config.py

```

  # config.py

class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments

class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

```
 
Create database config
  mkdir instance
    touch instance/config.py

```

# instance/config.py

SECRET_KEY = 'p9Bv<3Eid9%$i01'
SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/happy_share_db'


```

Create app
    
  touch app/__init__.py
  
  ```
# app/__init__.py

# third-party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)

    return app

  ```

----- Hello app ----


------------
# app/__init__.py
# export FLASK_APP=run.py
# export FLASK_CONFIG=development
# third-party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()

def create_app(config_name):
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_object(app_config[config_name])
  app.config.from_pyfile('config.py')
  db.init_app(app)

  # temporary route
  @app.route('/')
  def hello_world():
    return 'Hello, World!'

  return app



------------

Set
$ export FLASK_CONFIG=development
$ export FLASK_APP=run.py

Flask run

---- End Hello ------


#### 6. Model

##### 6.1 login
  pip install flask-login

Create LoginManager object

```
# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

class User(UserMixin, db.Model):
  """
  Create an User table
  """

  # Ensures table will be named in plural and not in singular
  # as is the name of the model
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(60), index=True, unique=True)
  username = db.Column(db.String(60), index=True, unique=True)
  first_name = db.Column(db.String(60), index=True)
  last_name = db.Column(db.String(60), index=True)
  password_hash = db.Column(db.String(128))
  # department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
  role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
  is_admin = db.Column(db.Boolean, default=False)

  @property
  def password(self):
    """
    Prevent pasword from being accessed
    """
    raise AttributeError('password is not a readable attribute.')

  @password.setter
  def password(self, password):
    """
    Set password to a hashed password
    """
    self.password_hash = generate_password_hash(password)

  def verify_password(self, password):
    """
    Check if hashed password matches actual password
    """
    return check_password_hash(self.password_hash, password)

  def __repr__(self):
      return '<User: {}>'.format(self.username)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

class Post(db.Model):
  """
  Create a Department table
  """

  __tablename__ = 'posts'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(60), unique=True)
  description = db.Column(db.String(200))
  users = db.relationship('User', backref='post',
                              lazy='dynamic')

  def __repr__(self):
    return '<Post: {}>'.format(self.name)

class Role(db.Model):
  """
  Create a Role table
  """

  __tablename__ = 'roles'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(60), unique=True)
  description = db.Column(db.String(200))
  users = db.relationship('User', backref='role',
                              lazy='dynamic')

  def __repr__(self):
    return '<Role: {}>'.format(self.name)

```

####  7. Migration

pip install flask-migrate

app/__init__.py

```
# app/__init__.py

# after existing third-party imports
from flask_migrate import Migrate

# existing code remains

def create_app(config_name):
    # existing code remains

    migrate = Migrate(app, db)

    from app import models

    return app

```

* No command 'flask' found => pip install flask-cli


flask db init
Mysql
create database happy_share_db


flask db migrate
  flask db upgrade

  
#### 8. Blueprints

  Blueprints are organising a flask app

like that:
└── dream-team
    ├── app
    │   ├── __init__.py
    │   ├── admin
    │   │   ├── __init__.py
    │   │   ├── forms.py
    │   │   └── views.py
    │   ├── auth
    │   │   ├── __init__.py
    │   │   ├── forms.py
    │   │   └── views.py
    │   ├── home
    │   │   ├── __init__.py
    │   │   └── views.py
    │   ├── models.py
    │   ├── static
    │   └── templates
    ├── config.py
    ├── instance
    │   └── config.py
    ├── migrations
    │   ├── README
    │   ├── alembic.ini
    │   ├── env.py
    │   ├── script.py.mako
    │   └── versions
    │       └── a1a1d8b30202_.py
    ├── requirements.txt
    └── run.py

- For Admin
mkdir app/admin
touch app/admin/__init__.py

```
# app/admin/__init__.py

from flask import Blueprint

admin = Blueprint('admin', __name__)

from . import views

```

- For Auth
mkdir app/auth
touch app/auth/__init__.py

```
# app/auth/__init__.py

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views

```

For home
mkdir app/home
touch app/home/__init__.py

```
# app/home/__init__.py

from flask import Blueprint

home = Blueprint('home', __name__)

from . import views

```


** cần tạo các file views.py cho từng thư mục

```
# app/__init__.py

# existing code remains

def create_app(config_name):
    # existing code remains

    from app import models

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    return app
```

#### 8.1 Home Blueprint
```
# app/home/views.py

from flask import render_template
from flask_login import login_required

from . import home

@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")

@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    return render_template('home/dashboard.html', title="Dashboard")
```

Layout
```
<!-- app/templates/base.html -->

<!DOCTYPE html>
<html lang="en">
<head>
    <title>{{ title }} | Project Dream Team</title>
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
    <link href="{{ url_for('static', filename='css/style.css') }}" rel="stylesheet">
    <link rel="shortcut icon" href="{{ url_for('static', filename='img/favicon.ico') }}">
</head>
<body>
    <nav class="navbar navbar-default navbar-fixed-top topnav" role="navigation">
        <div class="container topnav">
          <div class="navbar-header">
              <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">
                  <span class="sr-only">Toggle navigation</span>
                  <span class="icon-bar"></span>
                  <span class="icon-bar"></span>
                  <span class="icon-bar"></span>
              </button>
              <a class="navbar-brand topnav" href="{{ url_for('home.homepage') }}">Project Dream Team</a>
          </div>
          <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
              <ul class="nav navbar-nav navbar-right">
                  <li><a href="{{ url_for('home.homepage') }}">Home</a></li>
                  <li><a href="#">Register</a></li>
                  <li><a href="#">Login</a></li>
              </ul>
          </div>
        </div>
    </nav>
    <div class="wrapper">
      {% block body %}
      {% endblock %}
      <div class="push"></div>
    </div>
    <footer>
        <div class="container">
            <div class="row">
                <div class="col-lg-12">
                    <ul class="list-inline">
                        <li><a href="{{ url_for('home.homepage') }}">Home</a></li>
                        <li class="footer-menu-divider">⋅</li>
                        <li><a href="#">Register</a></li>
                        <li class="footer-menu-divider">⋅</li>
                        <li><a href="#">Login</a></li>
                    </ul>
                    <p class="copyright text-muted small">Copyright © 2016. All Rights Reserved</p>
                </div>
            </div>
        </div>
    </footer>
</body>
</html>
```

Views templates

```
<!-- app/templates/home/index.html -->

{% extends "base.html" %}
{% block title %}Home{% endblock %}
{% block body %}
<div class="intro-header">
    <div class="container">
        <div class="row">
            <div class="col-lg-12">
                <div class="intro-message">
                    <h1>Project Dream Team</h1>
                    <h3>The best company in the world!</h3>
                    <hr class="intro-divider">
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

```
Stylesheet

```
/* app/static/css/style.css */

body, html {
    width: 100%;
    height: 100%;
}

body, h1, h2, h3 {
    font-family: "Lato", "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-weight: 700;
}

a, .navbar-default .navbar-brand, .navbar-default .navbar-nav>li>a {
  color: #aec251;
}

a:hover, .navbar-default .navbar-brand:hover, .navbar-default .navbar-nav>li>a:hover {
  color: #687430;
}

footer {
    padding: 50px 0;
    background-color: #f8f8f8;
}

p.copyright {
    margin: 15px 0 0;
}

.alert-info {
    width: 50%;
    margin: auto;
    color: #687430;
    background-color: #e6ecca;
    border-color: #aec251;
}

.btn-default {
    border-color: #aec251;
    color: #aec251;
}

.btn-default:hover {
    background-color: #aec251;
}

.center {
    margin: auto;
    width: 50%;
    padding: 10px;
}

.content-section {
    padding: 50px 0;
    border-top: 1px solid #e7e7e7;
}

.footer, .push {
  clear: both;
  height: 4em;
}

.intro-divider {
    width: 400px;
    border-top: 1px solid #f8f8f8;
    border-bottom: 1px solid rgba(0,0,0,0.2);
}

.intro-header {
    padding-top: 50px;
    padding-bottom: 50px;
    text-align: center;
    color: #f8f8f8;
    background: url(../img/intro-bg.jpg) no-repeat center center;
    background-size: cover;
    height: 100%;
}

.intro-message {
    position: relative;
    padding-top: 20%;
    padding-bottom: 20%;
}

.intro-message > h1 {
    margin: 0;
    text-shadow: 2px 2px 3px rgba(0,0,0,0.6);
    font-size: 5em;
}

.intro-message > h3 {
    text-shadow: 2px 2px 3px rgba(0,0,0,0.6);
}

.lead {
    font-size: 18px;
    font-weight: 400;
}

.topnav {
    font-size: 14px;
}

.wrapper {
  min-height: 100%;
  height: auto !important;
  height: 100%;
  margin: 0 auto -4em;
}

```
Flask run and see your result


7.2 Auth Blueprint

pip install Flask-WTF
Form

```
# app/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import User

class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')

class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

```

Views.py

```
# app/auth/views.py

from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from forms import LoginForm, RegistrationForm
from .. import db
from ..models import User

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an User to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                            username=form.username.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=form.password.data)

        # add user to the database
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered! You may now login.')

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an user in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether user exists in the database and whether
        # the password entered matches the password in the database
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(
                form.password.data):
            # log user in
            login_user(user)

            # redirect to the dashboard page after login
            return redirect(url_for('home.dashboard'))

        # when login details are incorrect
        else:
            flash('Invalid email or password.')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')

@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an user out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))

```

pip install flask-bootstrap
In app/__init__.pry

from flask_bootstrap import Bootstrap
Bootstrap(app)
Views template

```
<!-- app/templates/auth/register.html -->

{% import "bootstrap/wtf.html" as wtf %}
{% extends "base.html" %}
{% block title %}Register{% endblock %}
{% block body %}
<div class="content-section">
  <div class="center">
    <h1>Register for an account</h1>
    <br/>
    {{ wtf.quick_form(form) }}
  </div>
</div>
{% endblock %}

```

```
<!-- app/templates/auth/login.html -->

{% import "bootstrap/utils.html" as utils %}
{% import "bootstrap/wtf.html" as wtf %}
{% extends "base.html" %}
{% block title %}Login{% endblock %}
{% block body %}
<div class="content-section">
  <br/>
  {{ utils.flashed_messages() }}
  <br/>
  <div class="center">
    <h1>Login to your account</h1>
    <br/>
    {{ wtf.quick_form(form) }}
  </div>
</div>
{% endblock %}

```

Home/dashboad

```
<!-- app/templates/home/dashboard.html -->

{% extends "base.html" %}
{% block title %}Dashboard{% endblock %}
{% block body %}
<div class="intro-header">
    <div class="container">
        <div class="row">
            <div class="col-lg-12">
                <div class="intro-message">
                    <h1>The Dashboard</h1>
                    <h3>We made it here!</h3>
                    <hr class="intro-divider">
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

```
