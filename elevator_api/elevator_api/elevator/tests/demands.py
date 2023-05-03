# Django
from django.test import TestCase

# Python
import json

# Django Rest Framework
from rest_framework.test import APIClient
from rest_framework import status

from elevator_api.elevator.models import Elevator


class DemandTestCase(TestCase):
    """Demands test case."""

    def setUp(self):
        """Test case setup."""

        self.client = APIClient()

        elevator_response = self.client.post(
            '/elevators/elevators/', {'name': '1',
                                      'current_floor': 0,
                                      'max_floors': 10}, format='json')

        self.elevator_data = elevator_response.data

        demand_data = {
            "id": 1,
            "moment": "2023-04-30T18:06:00Z",
            "source_floor": 5,
            "destination_floor": 13,
            "rest_floor": 0,
            "elevator": self.elevator_data['id']
        }
        demand_response = self.client.post(
            '/elevators/demands/', demand_data, format='json')

        self.demand_response_data = demand_response.data

    def test_create_demand(self):
        """Test to validate the operation of demand creation."""

        demand_data = {
            "moment": "2023-05-01T18:06:00Z",
            "source_floor": 5,
            "destination_floor": 13,
            "rest_floor": 7,
            "elevator": self.elevator_data['id']
        }
        demand_response = self.client.post(
            '/elevators/demands/', demand_data, format='json')

        result = json.loads(demand_response.content)
        self.assertEqual(demand_response.status_code, status.HTTP_201_CREATED)

        content = result
        self.assertIn('id', content)
        self.assertIn('moment', content)
        self.assertIn('source_floor', content)
        self.assertIn('destination_floor', content)
        self.assertIn('rest_floor', content)
        self.assertIn('elevator', content)

    def test_get_by_list_demand(self):
        """Test to validate the operation of demand list."""

        response = self.client.get('/elevators/demands/')

        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIs(type(result), list)

        for content in result:
            self.assertIn('id', content)
            self.assertIn('moment', content)
            self.assertIn('source_floor', content)
            self.assertIn('destination_floor', content)
            self.assertIn('rest_floor', content)
            self.assertIn('elevator', content)

    def test_get_demand(self):
        """Test to validate the operation of demand get."""

        response = self.client.get(f'/elevators/demands/{self.demand_response_data["id"]}/')

        content = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIs(type(content), dict)

        self.assertIn('id', content)
        self.assertIn('moment', content)
        self.assertIn('source_floor', content)
        self.assertIn('destination_floor', content)
        self.assertIn('rest_floor', content)
        self.assertIn('max_floors', content)
        self.assertIn('elevator', content)

        self.assertIsInstance(content['elevator'], str)
        self.assertIsInstance(content['max_floors'], int)

    def test_update_demand(self):
        """Test to validate the operation of demand update."""

        demand_update_data = {
            "moment": "2023-05-02T18:06:00Z",
            "source_floor": 10,
            "destination_floor": 13,
            "rest_floor": 7,
            "elevator": self.elevator_data['id']
        }

        response = self.client.put(
            f'/elevators/demands/{self.demand_response_data["id"]}/',
            demand_update_data,
            format='json'
        )

        content = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', content)
        self.assertIn('moment', content)
        self.assertIn('source_floor', content)
        self.assertIn('destination_floor', content)
        self.assertIn('rest_floor', content)
        self.assertIn('elevator', content)

    def test_delete_elevator(self):
        """Test to validate the operation of demand delete."""

        response = self.client.delete(
            f'/elevators/demands/{self.demand_response_data["id"]}/',
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        elevator_exists = Elevator.objects.filter(pk=self.demand_response_data["id"])
        self.assertFalse(elevator_exists)
