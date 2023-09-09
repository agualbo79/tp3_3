from flask import Flask, jsonify
from flask_cors import CORS
from config import Config

from .routes.film_bp import film_bp
from .database import DatabaseConnection
from .models.exceptions import CustomException, FilmNotFound,InvalidDataError  # Importamos las excepciones necesarias

def init_app():
    """Crea y configura la aplicación Flask"""
    
    app = Flask(__name__, static_folder=Config.STATIC_FOLDER, template_folder=Config.TEMPLATE_FOLDER)
    
    CORS(app, supports_credentials=True)

    app.config.from_object(
        Config
    )

    DatabaseConnection.set_config(app.config)

    app.register_blueprint(film_bp, url_prefix='/films')

    # Agrega el manejador de excepciones para FilmNotFound
    @app.errorhandler(FilmNotFound)
    def handle_film_not_found_exception(e):
        response = jsonify(error={
            'code': e.status_code,
            'name': e.name,
            'description': e.description,
        })
        response.status_code = e.status_code
        return response

    # Agrega el manejador de excepciones para InvalidDataError
    @app.errorhandler(InvalidDataError)
    def handle_invalid_data_error(e):
        response = jsonify(error={
            'code': e.status_code,
            'name': e.name,
            'description': e.description,
        })
        response.status_code = e.status_code
        return response

    return app