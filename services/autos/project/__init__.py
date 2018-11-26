# services/users/project/__init__.py


import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# inicializa la db


db = SQLAlchemy()


def create_app(script_info=None):
    # instancia la app
    app = Flask(__name__)

    # enable CORS
    CORS(app)  # nuevo

    # establece la configuración
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # establece extensiones
    db.init_app(app)
    #toolbar.init_app(app)

    # registra blueprints
    from project.api.autos import autos_blueprint
    app.register_blueprint(autos_blueprint)

    # contexto shell para flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
