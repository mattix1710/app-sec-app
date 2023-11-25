from flask import Flask

def create_app():
    app = Flask(__name__)
    
    ############################################
    # import app blueprints (auth, api, etc.)
    
    # registering MAIN blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # registering AUTH blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    # registering API blueprint
    
    # TODO: create API - for now, leave it commented
    # from .api import api as api_blueprint
    # app.register_blueprint(api_blueprint, url_prefix='/api/')
    
    return app

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)