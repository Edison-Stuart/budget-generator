'''This module will serve templates to a user
as well as decide what actions
should be taken depending on request type.'''
from flask import render_template, request
from application.home.common.generate import generate_budget, get_user_data
from . import home_bp

@home_bp.route('/')
def home():
    '''Will render the homepage template'''
    return render_template('index.jinja2')

@home_bp.route('/about')
def about():
    '''Will render the about page template'''
    return render_template('about.jinja2')

@home_bp.route('/form', methods=['GET'])
def form():
    ''' Will render the form entry page template'''
    return render_template('form.jinja2')

@home_bp.route('/display', methods=['POST'])
def display():
    '''Will render the budget display page with info from form page'''
    user_data = get_user_data(request)
    response = generate_budget(user_data)
    result = {**user_data, **response}
    template = render_template('display.jinja2', result = result)
    return template
