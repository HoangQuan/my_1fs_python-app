# app/home/views.py

from flask import render_template
from flask_login import login_required

from . import admin

@admin.route('/admin/index')
def homepage():
  """
  Render the homepage template on the / route
  """
  return render_template('admin/index.html', title="Welcome")

@admin.route('/admin/dashboard')
@login_required
def dashboard():
  """
  Render the dashboard template on the /dashboard route
  """
  return render_template('admin/dashboard.html', title="Dashboard")
