"""Initialize Flask app."""
from flask import Flask
from flask_assets import Environment, Bundle
from application.budget.db import get_db_connection

def create_app() -> Flask:
    """Create and returns a Flask application."""

    app = Flask(__name__, instance_relative_config=False)
    assets = Environment(app)
    app.config.from_pyfile('config.py')
    
    with app.app_context():
        # Import parts of our application
        from .home import routes
        from .budget import routes

        # Register Blueprints
        app.register_blueprint(home.home_bp)
        app.register_blueprint(budget.budget_bp, url_prefix='/budget')

        # Register Assets (For now js_all is just one file but eventually
        #                  there will be multiple bundled files)
        java_script = Bundle('../home/static/saved_budgets.js', output='packed.js')
        assets.register("js_all", java_script)
        return app

IN_UWSGI = True
try:
    from uwsgidecorators import postfork
    @postfork
    def connect_after_fork():
        '''Reconnects to database after server forks.'''
        get_db_connection()
except:
    IN_UWSGI = False
    def connect_after_fork():
        print("-----connect_after_fork was called outside of UWSGI-----")
