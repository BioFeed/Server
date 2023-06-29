import unittest
import requests
import random

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
        r = random.randint(0, 10000)
        print('Random number: ', r)
        if (len(argv) == 0) or (argv[0].lower() == 'y'):
            url, port, protocol = LOCAL_URL, LOCAL_PORT, 'http'
        else:
            url, port, protocol = DISTANT_URL, DISTANT_PORT, 'https'
        url = f'{protocol}://{url}:{port}'

        tests = [
            (
                {"name": "carotte", "date": r, "photo": "base64ici", "token": TOKEN},
                '/store_data'
            ),
            (
                {"command": "clear", "token": TOKEN},
                '/command'
            ),
            (
                {"name": "carotte1", "date": r, "photo": "base64ici", "token": TOKEN},
                '/store_data'
            ),
            (
                {"name": "carotte2", "date": r, "photo": "base64ici", "token": TOKEN},
                '/store_data'
            ),
            (
                {"name": "courgette", "date": r, "photo": "base64ici", "token": "wrong_token"},
                '/store_data'
            ),
            (
                {"name": "carotte3", "date": r, "photo": "base64ici", "token": TOKEN},
                '/store_data'
            ),
            (
                {"name": "carotte4", "date": r, "photo": "base64ici", "token": TOKEN},
                '/store_data'
            ),
            (
                {"name": "carotte5", "date": r, "photo": "base64ici", "token": TOKEN},
                '/store_data'
            ),
            (
                {"name": "carotte6", "date": r, "photo": "base64ici", "token": TOKEN},
                '/store_data'
            ),
            (
                {"name": "carotte7", "date": r, "photo": "base64ici", "token": TOKEN},
                '/store_data'
            ),
            (
                {"name": "carotte8", "date": r, "photo": "base64ici", "token": TOKEN},
                '/store_data'
            ),
            (
                {"name": "carotte9", "date": r, "photo": "base64ici", "token": TOKEN},
                '/store_data'
            ),
            (
                {"name": "carotte10", "date": r, "photo": "base64ici", "token": TOKEN},
                '/store_data'
            ),
            (
                {"name": "tomate", "date": r, "photo": "base64ici", "token": TOKEN},
                '/store_data'
            )
        ]
        for x in tests:
            response = send_post_request(url + x[1], x[0])
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
