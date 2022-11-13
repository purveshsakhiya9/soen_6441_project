import unittest
import requests

class MyTestCase(unittest.TestCase):
    def test_something(self):
        url = "https://car-api2.p.rapidapi.com/api/trims/6276"
        headers = {
            "X-RapidAPI-Key": "e9983c2065mshaf33398be4b091dp132915jsnb3a831923739",
            "X-RapidAPI-Host": "car-api2.p.rapidapi.com"
        }
        result = requests.request("GET", url, headers=headers)
        self.assertEqual(result.status_code, 200)  # add assertion here


if __name__ == '__main__':
    unittest.main()
