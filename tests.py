import unittest
import requests

# Information:
TOKEN = 'X9oIrX4UlQsjY5P0XXtO'
DISTANT_URL = 'biofeed.vitavault.fr'
DISTANT_PORT = 443
LOCAL_URL = 'localhost'
LOCAL_PORT = 5000


def send_post_request(url, data):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data, headers=headers)
    return response


class MyTestCase(unittest.TestCase):
    def test_local_post_request(self):
        argv = input('Local ? [Y|n] > ')
        if argv[0].lower() == 'y':
            url, port, protocol = LOCAL_URL, LOCAL_PORT, 'http'
        else:
            url, port, protocol = DISTANT_URL, DISTANT_PORT, 'https'
        url = f'{protocol}://{url}:{port}'

        tests = [
            (
                {"name": "carotte", "date": 1234, "photo": "base64ici", "token": TOKEN},
                '/store_data'
            )
        ]
        for x in tests:
            response = send_post_request(url + x[1], x[0])
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
