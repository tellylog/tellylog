"""This file holds the Person class"""
from .parent import Parent


class Person(Parent):
    """
    Class to get data of actors, directors, producers,...

    Attributes:
        URLS (dict): Holds all relevant urls
    """

    URLS = {
        'person_url': 'person/{id}',
    }

    def get_person(self, person_id):
        """
        Get information about a Person via id.

        Args:
            person_id (int): Id of the person

        Returns:
            bool: False on failure
            dict: Dictionary with the response on success
        """
        target = self.base_uri + self.URLS['person_url'].format(id=person_id)
        response = self.make_request(target=target)
        if not response:
            return False
        return response
