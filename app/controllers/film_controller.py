from ..models.film_model import Film
from ..models.exceptions import FilmNotFound,InvalidDataError  
from flask import request, jsonify


from decimal import Decimal

class FilmController:
    """Film controller class"""

    @classmethod
    def get(cls, film_id):
        """Get a film by id"""
        film = Film(film_id=film_id)
        result = Film.get(film)
        if result is not None:
            return result.serialize(), 200
        else:
            # Si la película no se encuentra, lanza la excepción FilmNotFound
            raise FilmNotFound(film_id)
        
    @classmethod
    def get_all(cls):
        """Get all films"""
        film_objects = Film.get_all()
        films = []
        for film in film_objects:
            films.append(film.serialize())
        return films, 200
    
    @classmethod
    def create(cls):
        """Create a new film"""
        data = request.json

        # Validaciones de datos
        if len(data.get('title', '')) < 3:
            raise InvalidDataError(400, 'Invalid Data', 'Title must have at least three characters')

        if not isinstance(data.get('language_id', 0), int):
            raise InvalidDataError(400, 'Invalid Data', 'Language ID must be an integer')

        if not isinstance(data.get('rental_duration', 0), int):
            raise InvalidDataError(400, 'Invalid Data', 'Rental Duration must be an integer')

        if not isinstance(data.get('rental_rate', 0), int):
            raise InvalidDataError(400, 'Invalid Data', 'Rental Rate must be an integer')

        if not isinstance(data.get('replacement_cost', 0), int):
            raise InvalidDataError(400, 'Invalid Data', 'Replacement Cost must be an integer')

        special_features = data.get('special_features', [])
        if not isinstance(special_features, list) or not all(isinstance(feature, str) and feature in ['Trailers', 'Commentaries', 'Deleted Scenes', 'Behind the Scenes'] for feature in special_features):
            raise InvalidDataError(400, 'Invalid Data', 'Special Features must be a list of valid strings')

        # Crear la película si todas las validaciones son exitosas
        if data.get('rental_rate') is not None:
            data['rental_rate'] = Decimal(data.get('rental_rate')) / 100

        if data.get('replacement_cost') is not None:
            data['replacement_cost'] = Decimal(data.get('replacement_cost')) / 100

        film = Film(**data)
        Film.create(film)
        return {'message': 'Film created successfully'}, 201

    @classmethod
    def update(cls, film_id):
        """Update a film"""
        data = request.json
        print("Data recibida para actualización:", data)
        
        # Verifica si el ID de la película existe
        film = Film(film_id=film_id)
        if not film.exists():
            raise FilmNotFound(status_code=404, description=f"Film with id {film_id} not found")
        
        # Prepara los datos para la actualización
        update_data = {}
        if 'rental_rate' in data:
            rental_rate = data['rental_rate']
            if isinstance(rental_rate, float):
                rental_rate = Decimal(rental_rate).quantize(Decimal('0.00'))
            update_data['rental_rate'] = rental_rate
        
        if 'replacement_cost' in data:
            replacement_cost = data['replacement_cost']
            if isinstance(replacement_cost, float):
                replacement_cost = Decimal(replacement_cost).quantize(Decimal('0.00'))
            update_data['replacement_cost'] = replacement_cost
        
        # Actualiza la película solo si es una instancia válida de la clase Film
        if isinstance(film, Film) and update_data:
            film.update(update_data)
        
        return {'message': 'Film updated successfully'}, 200


    @classmethod
    def delete(cls, film_id):
        """Delete a film"""
        film = Film(film_id=film_id)
        # Antes de eliminar, verifica si la película existe
        existing_film = Film.get(film)
        if existing_film is not None:
            Film.delete(film)
            return {'message': 'Film deleted successfully'}, 204
        else:
            # Si la película no se encuentra, lanza la excepción FilmNotFound
            raise FilmNotFound(film_id)