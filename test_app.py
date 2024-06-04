import unittest
from app import app, db, Floor, ElevatorEvent


class ElevatorTestCase(unittest.TestCase):
    """
    Test case for the Elevator application.
    """

    def setUp(self):
        """
        Set up a blank database before each test.
        """
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """
        Destroy the database after each test.
        """
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_floor(self):
        """
        Test the addition of a new floor.
        """
        response = self.app.post('/floors', json={'floor_number': 1})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Floor added', response.get_json().get('message'))

    def test_add_event(self):
        """
        Test the recording of a new elevator event.
        """
        self.app.post('/floors', json={'floor_number': 2})
        response = self.app.post('/events', json={
            'source_floor_id': 1,
            'destination_floor_id': 2,
            'num_persons': 3,
            'weight': 200.5,
            'event_type': 'call'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Event recorded', response.get_json().get('message'))

    def test_get_events(self):
        """
        Test retrieval of all elevator events.
        """
        self.app.post('/floors', json={'floor_number': 3})
        self.app.post('/events', json={
            'source_floor_id': 1,
            'destination_floor_id': 3,
            'num_persons': 4,
            'weight': 300.0,
            'event_type': 'call'
        })
        response = self.app.get('/events')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.get_json()) > 0)


if __name__ == '__main__':
    unittest.main()
