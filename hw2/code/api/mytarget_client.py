from urllib.parse import urljoin
import requests


class ResponseStatusCodeException(Exception):
    pass


class MyTargetClient:

    def __init__(self, email, password):
        self.base_url = 'https://target.my.com/'
        self.token = None
        self.session = requests.Session()
        self.email = email
        self.password = password
        self.login()

    def _request(self, method, location, status_code=200, headers=None, params=None, data=None, json_data=None):
        url = urljoin(self.base_url, location)
        if json_data:
            response = self.session.request(method, url, headers=headers, params=params, json=json_data)
        else:
            response = self.session.request(method, url, headers=headers, params=params, data=data)

        if response.status_code != status_code:
            raise ResponseStatusCodeException(f' Got {response.status_code} {response.reason} for URL "{url}"')

        return response

    def get_token(self):
        location = 'csrf/'
        headers = self._request('GET', location).headers
        self.token = headers['Set-Cookie'].split(';')[0].split('=')[-1]

    def login(self):
        location = 'https://auth-ac.my.com/auth?lang=ru&nosavelogin=0'

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://target.my.com/'
        }

        data = {
            'login': self.email,
            'password': self.password,
            'continue': 'https://target.my.com/auth/mycom?state=target_login%3D1#email',
            'failure': 'https://account.my.com/login/'
        }

        response = self._request('POST', location, headers=headers, data=data)
        self.get_token()
        return response

    def create_segment(self, name):
        data = {"name": name, "pass_condition": 1,
                "relations": [
                    {"object_type": "remarketing_player", "params": {"type": "positive", "left": 365, "right": 0}}],
                "logicType": "or"}

        headers = {
            'Content-Type': 'application/json',
            'Referer': 'https://target.my.com/segments/segments_list/new',
            'X-CSRFToken': self.token,
            'X-Requested-With': 'XMLHttpRequest',
        }

        location = 'api/v2/remarketing/segments.json'

        return self._request('POST', location, headers=headers, json_data=data)

    def delete_segment(self, segment_id):
        location = f'api/v2/remarketing/segments/{segment_id}.json'
        headers = {
            'Referer': 'https://target.my.com/segments/segments_list',
            'X-CSRFToken': self.token,
            'X-Requested-With': 'XMLHttpRequest',
        }
        return self._request('POST', location, 204, headers=headers)
