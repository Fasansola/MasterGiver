# mailerlite_integration/mailerlite.py
import requests
from django.conf import settings

class MailerLiteClient:
    def __init__(self):
        self.api_key = settings.MAILERLITE_API_KEY
        self.base_url = 'https://api.mailerlite.com/api/v2'
        self.headers = {
            'X-MailerLite-ApiKey': self.api_key,
            'Content-Type': 'application/json'
        }

    def add_subscriber(self, email, name='', group_id=None):
        endpoint = f'{self.base_url}/subscribers'
        
        data = {
            'email': email,
            'name': name,
            'resubscribe': True,
        }

        if group_id:
            endpoint = f'{self.base_url}/groups/{group_id}/subscribers'

        try:
            response = requests.post(endpoint, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error adding subscriber to MailerLite: {str(e)}")
            raise