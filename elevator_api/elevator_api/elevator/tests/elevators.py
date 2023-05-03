# Django
from django.test import TestCase

# Python
import json

# Django Rest Framework
from rest_framework.test import APIClient
from rest_framework import status

from elevator_api.elevator.models import Elevator


class ElevatorTestCase(TestCase):
    """Elevators test case."""

    def setUp(self):
        """Test case setup."""

        self.client = APIClient()

        self.elevator = self.client.post(
            '/elevators/elevators/', {'name': '1',
                                      'current_floor': 0,
                                      'max_floors': 10}, format='json')

    def test_create_elevator(self):
        """Test to validate the operation of elevator creation."""

        response = self.elevator

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        content = result
        self.assertIn('id', content)
        self.assertIn('name', content)
        self.assertIn('current_floor', content)
        self.assertIn('max_floors', content)

    def test_get_by_list_elevator(self):
        """Test to validate the operation of the list of elevators."""

        response = self.client.get('/elevators/elevators/')

        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIs(type(result), list)

        for content in result:
            self.assertIn('id', content)
            self.assertIn('name', content)
            self.assertIn('current_floor', content)
            self.assertIn('max_floors', content)

    def test_get_elevator(self):
        """Test to validate the operation of elevator get."""

        response = self.client.get(f'/elevators/elevators/{self.elevator.data["id"]}/')

        elevator = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIs(type(elevator), dict)

        self.assertIn('id', elevator)
        self.assertIn('name', elevator)
        self.assertIn('current_floor', elevator)
        self.assertIn('max_floors', elevator)

    def test_update_elevator(self):
        """Test to validate the operation of elevator update."""

        elevator_data = {
            'name': '1',
            "current_floor": 5,
            "max_floors": 10
        }

        response = self.client.put(
            f'/elevators/elevators/{self.elevator.data["id"]}/',
            elevator_data,
            format='json'
        )

        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', result)
        self.assertIn('name', result)
        self.assertIn('max_floors', result)
        self.assertIn('current_floor', result)

    def test_delete_elevator(self):
        """Test to validate the operation of elevator delete."""

        response = self.client.delete(
            f'/elevators/elevators/{self.elevator.data["id"]}/',
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        elevator_exists = Elevator.objects.filter(pk=self.elevator.data["id"])
        self.assertFalse(elevator_exists)
