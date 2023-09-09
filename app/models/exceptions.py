from flask import jsonify


class CustomException(Exception):

    def __init__(self, status_code, name = "Custom Error", description = 'Error'): 
        super().__init__()
        self.description = description
        self.name = name
        self.status_code = status_code

    def get_response(self):
        response = jsonify({
            'error': {
                'code': self.status_code,
                'name': self.name,
                'description': self.description,
            }
        })
        response.status_code = self.status_code
        return response

# ejercicio 1 
class FilmNotFound(CustomException):
    """
    Una excepción personalizada que se lanza cuando no se encuentra una película.
    
    Esta excepción hereda de la clase `CustomException` y se utiliza para indicar que no se pudo encontrar una película con el ID especificado en la base de datos.
    
    Args:
        film_id (int): El ID de la película que no se encontró.
    """
    def __init__(self, film_id):
        super().__init__(status_code=404, name="Film Not Found", description=f"Film with id {film_id} not found")    
        

class InvalidDataError(CustomException):
    """
    Una excepción personalizada que se lanza cuando los datos proporcionados son inválidos.
    
    Esta excepción hereda de la clase `CustomException` y se utiliza para indicar que los datos proporcionados en una petición no son válidos o tienen un formato incorrecto.
    
    Args:
        status_code (int): El código de estado HTTP que se debe devolver al cliente.
        name (str): El nombre de la excepción. Por defecto es "Invalid Data".
        description (str): Una descripción detallada del error. Por defecto es "Invalid data".
    """
    def __init__(self, status_code, name="Invalid Data", description='Invalid data'):
        super().__init__(status_code, name, description)        