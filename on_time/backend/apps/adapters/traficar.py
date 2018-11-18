import requests


class TraficarSdk:
    def cars(self):
        response = requests.get(
            'https://api.traficar.pl/eaw-rest-api/car',
            params={'shapeId': 2},
        )
        return response.json()['cars']
