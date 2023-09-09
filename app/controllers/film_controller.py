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
        """Crea una nueva película.
    
    Este método primero valida los datos en la petición POST para asegurarse de que tienen el formato correcto. Si alguno de los datos no cumple con las validaciones, se lanza una excepción `InvalidDataError`.
    
    Si todos los datos son válidos, se crea una nueva película en la base de datos con los datos proporcionados en la petición POST.
    
    Returns:
        dict: Un diccionario con un mensaje indicando que la película se creó correctamente.
        int: Un código de estado HTTP 201 indicando que la operación fue exitosa y se creó un nuevo recurso."""
        data = request.json

        # Validaciones de datos
        if len(data.get('title', '')) < 3:
            raise InvalidDataError(400, 'Invalid Data', 'El título debe tener al menos tres caracteres.')

        if not isinstance(data.get('language_id', 0), int):
            raise InvalidDataError(400, 'Invalid Data', 'El ID de idioma debe ser un número entero')

        if not isinstance(data.get('rental_duration', 0), int):
            raise InvalidDataError(400, 'Invalid Data', 'La duración del alquiler debe ser un número entero')

        if not isinstance(data.get('rental_rate', 0), int):
            raise InvalidDataError(400, 'Invalid Data', 'La tarifa de alquiler debe ser un número enteror')

        if not isinstance(data.get('replacement_cost', 0), int):
            raise InvalidDataError(400, 'Invalid Data', 'El costo de reposición debe ser un número entero.')

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
        """ Actualiza una película por su ID.
    
    Este método primero verifica si el ID de la película existe en la base de datos utilizando el método `exists`. Si el ID no existe, se lanza una excepción `FilmNotFound`.
    
    Luego, valida los datos en la petición PUT para asegurarse de que tienen el formato correcto. Si alguno de los datos no cumple con las validaciones, se lanza una excepción `InvalidDataError`.
    
    Finalmente, si la película existe y los datos son válidos, se actualiza la película en la base de datos.
    
    Args:
        film_id (int): El ID de la película que se desea actualizar.
    
    Returns:
        dict: Un diccionario con un mensaje indicando que la película se actualizó correctamente.
        int: Un código de estado HTTP 200 indicando que la operación fue exitosa."""
        data = request.json
        print("Data recibida para actualización:", data)
        
        # Verifica si el ID de la película existe
        film = Film(film_id=film_id)
        if not film.exists():
            raise FilmNotFound(film_id)
        
        # Prepara los datos para la actualización
        update_data = {}
        
        # Valida los datos de entrada
        if 'title' in data and len(data['title']) < 3:
            raise InvalidDataError(status_code=400, description='El atributo title debe tener tres caracteres como mínimo.')
        
        if 'language_id' in data and not isinstance(data['language_id'], int):
            raise InvalidDataError(status_code=400, description='El atributo language_id debe ser un número entero.')
        
        if 'rental_duration' in data and not isinstance(data['rental_duration'], int):
            raise InvalidDataError(status_code=400, description='El atributo rental_duration debe ser un número entero.')
        
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
        
        if 'special_features' in data:
            special_features_allowed = ['Trailers', 'Commentaries', 'Deleted Scenes', 'Behind the Scenes']
            if not all(feature in special_features_allowed for feature in data['special_features']):
                raise InvalidDataError(status_code=400, description='El atributo special_features debe ser una lista de strings válidos.')
            update_data['special_features'] = data['special_features']
        
        # Actualiza la película solo si es una instancia válida de la clase Film y los datos son válidos
        if isinstance(film, Film) and update_data:
            film.update(film_id, update_data)
        
        return {'message': 'Film updated successfully'}, 200

    @classmethod
    def delete(cls, film_id):
        """
    Ejercicio 5.     
    Elimina una película por su ID.
    
    Antes de intentar eliminar la película, verifica si el ID de la película existe en la base de datos utilizando el método `exists` definido en el Ejercicio 3. Si el ID no existe, se lanza una excepción personalizada llamada `FilmNotFound`, que se definió en el Ejercicio 1.
    
    Args:
        film_id (int): El ID de la película que se desea eliminar.
    
    Returns:
        dict: Un diccionario con un mensaje indicando que la película se eliminó correctamente.
        int: Un código de estado HTTP 204 indicando que la operación fue exitosa.
    """
        film = Film(film_id=film_id)
        # Antes de eliminar, verifica si la película existe
        if not film.exists():
            raise FilmNotFound(film_id)
        
        Film.delete(film)
        return {'message': 'Film deleted successfully'}, 204