'''This module will serve templates to a user
as well as decide what actions
should be taken depending on request type.'''
from flask import render_template, request, send_file
from application.home.common.generate import generate_budget, get_user_data
from application.home.common.convert_file import make_pdf, pdf_cleanup
from application.home.common.db_endpoints import create, read, delete
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

    # TODO: We'll need to use common.config.APPCONFIG to get app_url so that we
    #  can build the button target
    template = render_template('display.html', result = result)
    return template

@home_bp.route('/getpdf', methods=['GET'])
def getpdf():
    '''Given query parameters save, spend, timetogoal, and goal, we will
        generate a pdf file and return it as a filestream download.'''

    query_params = request.args.to_dict(flat=True)
    pdf_cleanup()
    file_path = make_pdf(query_params)

    return send_file(file_path, download_name='your_budget.pdf')

@home_bp.route('/budgets/<int:budget_id>', methods=['GET', 'DELETE'])
@home_bp.route('/budgets', methods=['PUT', 'GET'])
def budgets(budget_id = None):
    '''Routes requests for budget saving capabilities to the correct handler function.'''
    budget_result = None
    if request.method == 'GET' and budget_id is not None:
        budget_result = read(budget_id)
    elif request.method == 'GET' and budget_id is None:
        budget_result = read()
    
    if request.method == 'PUT':
        query_params = request.args.to_dict(flat=True)
        budget_result = create(query_params)
    
    if request.method == 'DELETE' and budget_id is not None:
        delete(budget_id)

