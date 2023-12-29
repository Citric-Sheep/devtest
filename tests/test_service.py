import unittest
import requests


class TestService(unittest.TestCase):
    """
    Test cases for the Elevator Service API.

    These tests use the requests library to interact with the Elevator Service API
    and ensure that the endpoints are functioning as expected.

    Test methods:
        - test_call_elevator: Test the 'call_elevator' endpoint.
        - test_reset_elevator: Test the 'reset_elevator' endpoint.
        - test_get_last_call: Test the 'get_last_call' endpoint.
        - test_get_elevator_calls: Test the 'get_elevator_calls' endpoint.
        - test_get_data_csv: Test the 'get_data_csv' endpoint.
    """

    def test_call_elevator(self):
        """
        Test the 'call_elevator' endpoint.
w
        Sends a POST request to call the elevator to a specific destination floor.
        Asserts that the response status code is 200 and the returned message indicates success.
        """
        response = requests.post("http://localhost:8000/call-elevator",
                                 json={
                                     "target_floor": 12,
                                     "user_floor": 1
                                 })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["message"], "Elevator called successfully")

    def test_reset_elevator(self):
        """
        Test the 'reset_elevator' endpoint.

        Sends a DELETE request to reset the elevator.
        Asserts that the response status code is 200 and the returned message indicates success.
        """
        response = requests.delete("http://localhost:8000/reset-elevator")
        self.assertEqual(response.status_code, 200)

    def test_get_last_call(self):
        """
        Test the 'get_last_call' endpoint.

        Sends a GET request to retrieve information about the last elevator call.
        Asserts that the response status code is 200 and the returned message indicates success.
        """
        response = requests.get("http://localhost:8000/get-last-call")
        self.assertEqual(response.status_code, 200)

    def test_get_elevator_calls(self):
        """
        Test the 'get_elevator_calls' endpoint.

        Sends a GET request to retrieve a list of all elevator calls.
        Asserts that the response status code is 200, the returned message indicates success,
        and the 'data' field is a list.
        """
        response = requests.get("http://localhost:8000/get-elevator-calls")
        self.assertEqual(response.status_code, 200)

    def test_get_data_csv(self):
        """
        Test the 'get_data_csv' endpoint.

        Sends a GET request to retrieve data in CSV format.
        Asserts that the response status code is 200.
        """
        response = requests.get("http://localhost:8000/get-data-csv")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
