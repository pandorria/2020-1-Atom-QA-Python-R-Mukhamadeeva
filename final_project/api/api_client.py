from urllib.parse import urljoin

import requests


class ApiClient:

    def __init__(self, username, password, email):
        self.base_url = 'http://127.0.0.1:3000/'
        self.session = requests.Session()
        response_reg = self.session.post(urljoin(self.base_url, '/reg'), json={
            'username': username,
            'password': password,
            'confirm': password,
            'email': email,
            'term': 'y',
            'submit': 'Registration'
        })
        if response_reg.status_code == 200:
            pass
        elif response_reg.status_code == 409:
            assert self.session.post(urljoin(self.base_url, '/login'), json={
                'username': username,
                'password': password,
                'submit': 'Login'
            }).ok
        else:
            raise

    def reg_user(self, username, email, password):
        data = {
            "username": username,
            "password": password,
            "email": email
        }
        response = self.session.post(urljoin(self.base_url, '/api/add_user'), json=data)
        return response.status_code

    def del_user(self, username):
        response = self.session.get(urljoin(self.base_url, f'/api/del_user/{username}'))
        return response.status_code

    def block_user(self, username):
        response = self.session.get(urljoin(self.base_url, f'/api/block_user/{username}'))
        return response.status_code

    def accept_user(self, username):
        response = self.session.get(urljoin(self.base_url, f'/api/accept_user/{username}'))
        return response.status_code
