"""This file holds the Person class."""
from datetime import datetime, timedelta
from ._parent import _Parent


class Person(_Parent):

    """
    Class to get data of actors, directors, producers,...

    Attributes:
        URLS (dict): Holds all relevant urls
    """

    URLS = {
        'person_url': 'person/{id}',
        'changes': 'person/{id}/changes',
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
        request = self.make_request.delay(
            target=target, headers=self.headers, params=self.params, json=True)
        try:
            response = request.get()
        except:
            response = False
        if not response:
            return False
        return response

    def get_changes(self, person_id, start_date=None):
        """
        Get all the Changes from a start date until now.

        The start_date needs to be in the Format YYYY-MM-DD.
        The maximum start_date is two weeks before now.

        Args:
            person_id (int): ID of the person
            start_date (str): String in the Format YYYY-MM-DD

        Returns:
            bool: False on failure or dict is empty
            dict: Dict with changes
        """
        two_weeks_ago = datetime.today() - \
            timedelta(weeks=2)  # Date two weeks ago
        try:  # Try to get a valid date from start_date string.
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            # Check if start_date is in the last two weeks
            if start_date < two_weeks_ago:
                start_date = two_weeks_ago
            elif start_date > datetime.today():
                start_date = two_weeks_ago
        # Triggerd when no valid date can be extracted from start_date
        except (ValueError, TypeError):
            start_date = two_weeks_ago
        # Convert dates back to strings
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')
        target = (self.base_uri +
                  self.URLS['changes'].format(id=person_id))
        params = self.params
        params['start_date'] = start_date
        params['end_date'] = end_date
        request = self.make_request.delay(
            target=target, params=params, headers=self.headers, json=True)
        try:
            response = request.get()
        except:
            response = False
        if not response['changes']:
            return False
        return response
