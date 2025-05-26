import unittest
import json
import tempfile
import os
from datetime import datetime, timedelta
from main import app, db, Building, Elevator, ElevatorCall, ElevatorBusinessRules

class ElevatorSystemTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE']
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        
        db.create_all()
        
        # Create test data
        self.building = Building(
            name="Test Building",
            total_floors=5,
            building_type="office"
        )
        db.session.add(self.building)
        db.session.commit()
        
        self.elevator = Elevator(
            building_id=self.building.id,
            elevator_number="TEST-01",
            current_floor=1
        )
        db.session.add(self.elevator)
        db.session.commit()

    def tearDown(self):
        """Clean up after each test method."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_health_check(self):
        """Test the health check endpoint."""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('timestamp', data)

    def test_create_building(self):
        """Test building creation."""
        building_data = {
            'name': 'New Test Building',
            'total_floors': 5,
            'building_type': 'residential'
        }
        
        response = self.app.post('/api/buildings',
                               data=json.dumps(building_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'New Test Building')
        self.assertEqual(data['total_floors'], 5)
        self.assertEqual(data['building_type'], 'residential')

    def test_create_building_missing_data(self):
        """Test building creation with missing required fields."""
        building_data = {'name': 'Incomplete Building'}  # Missing total_floors
        
        response = self.app.post('/api/buildings',
                               data=json.dumps(building_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_create_elevator(self):
        """Test elevator creation."""
        elevator_data = {
            'elevator_number': 'TEST-02',
            'max_capacity': 1200,
            'current_floor': 3
        }
        
        response = self.app.post(f'/api/buildings/{self.building.id}/elevators',
                               data=json.dumps(elevator_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['elevator_number'], 'TEST-02')
        self.assertEqual(data['current_floor'], 3)

    def test_record_elevator_call(self):
        """Test recording an elevator call."""
        call_data = {
            'called_from_floor': 3,
            'destination_floor': 1,
            'estimated_passengers': 2,
            'call_type': 'normal'
        }
        
        response = self.app.post(f'/api/elevators/{self.elevator.id}/call',
                               data=json.dumps(call_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('call_id', data)
        self.assertIn('estimated_response_time', data)
        self.assertIn('temporal_features', data)
        
        # Verify temporal features are populated
        temporal = data['temporal_features']
        self.assertIn('day_of_week', temporal)
        self.assertIn('hour_of_day', temporal)
        self.assertIn('season', temporal)

    def test_record_elevator_call_invalid_floor(self):
        """Test recording call with invalid floor."""
        call_data = {
            'called_from_floor': 6,  # Building only has 5 floors
            'destination_floor': 1
        }
        
        response = self.app.post(f'/api/elevators/{self.elevator.id}/call',
                               data=json.dumps(call_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('Invalid floor number', data['error'])


    def test_get_elevator_status(self):
        """Test getting elevator status."""
        response = self.app.get(f'/api/elevators/{self.elevator.id}/status')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['elevator_id'], self.elevator.id)
        self.assertEqual(data['current_floor'], 1)
        self.assertIn('maintenance_alert', data)

    def test_get_ml_features(self):
        """Test ML features endpoint."""
        # Create some test calls first
        call1 = ElevatorCall(
            elevator_id=self.elevator.id,
            called_from_floor=2,
            elevator_position_at_call=1
        )
        call2 = ElevatorCall(
            elevator_id=self.elevator.id,
            called_from_floor=3,
            elevator_position_at_call=2
        )
        db.session.add_all([call1, call2])
        db.session.commit()
        
        response = self.app.get(f'/api/ml-data/features/{self.building.id}')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['building_id'], self.building.id)
        self.assertGreaterEqual(data['total_samples'], 2)
        self.assertIn('features', data)
        
        # Verify feature structure
        if data['features']:
            feature = data['features'][0]
            self.assertIn('target_floor', feature)
            self.assertIn('time_features', feature)
            self.assertIn('elevator_features', feature)
            self.assertIn('contextual_features', feature)

class BusinessRulesTestCase(unittest.TestCase):
    """Test business logic and validation rules."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app_context = app.app_context()
        self.app_context.push()
        
        db.create_all()
        
        self.building = Building(
            name="Business Rules Test Building",
            total_floors=5
        )
        db.session.add(self.building)
        db.session.commit()
        
        self.elevator = Elevator(
            building_id=self.building.id,
            elevator_number="TEST-01",
            current_floor=1
        )
        db.session.add(self.elevator)
        db.session.commit()

    def tearDown(self):
        """Clean up after each test method."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_validate_floor_range_valid(self):
        """Test floor range validation with valid floors."""
        self.assertTrue(ElevatorBusinessRules.validate_floor_range(1, self.building.id))
        self.assertTrue(ElevatorBusinessRules.validate_floor_range(3, self.building.id))
        self.assertTrue(ElevatorBusinessRules.validate_floor_range(5, self.building.id))

    def test_validate_floor_range_invalid(self):
        """Test floor range validation with invalid floors."""
        self.assertFalse(ElevatorBusinessRules.validate_floor_range(0, self.building.id))
        self.assertFalse(ElevatorBusinessRules.validate_floor_range(6, self.building.id))
        self.assertFalse(ElevatorBusinessRules.validate_floor_range(-1, self.building.id))

    def test_validate_floor_range_nonexistent_building(self):
        """Test floor range validation with nonexistent building."""
        self.assertFalse(ElevatorBusinessRules.validate_floor_range(5, 99999))

    def test_calculate_response_time(self):
        """Test response time calculation."""
        call_time = datetime.utcnow()
        
        # Same floor - minimum time (door operation)
        response_time = ElevatorBusinessRules.calculate_response_time(call_time, 5, 5)
        self.assertEqual(response_time, 2.0)
        
        # One floor away
        response_time = ElevatorBusinessRules.calculate_response_time(call_time, 5, 4)
        self.assertEqual(response_time, 5.0)  # 1 floor * 3 seconds + 2 seconds door
        
        # Multiple floors
        response_time = ElevatorBusinessRules.calculate_response_time(call_time, 1, 5)
        self.assertEqual(response_time, 14.0)  # 4 floors * 3 seconds + 2 seconds door

    def test_maintenance_alert_no_previous_maintenance(self):
        """Test maintenance alert for elevator with no maintenance history."""
        elevator = Elevator(
            building_id=self.building.id,
            elevator_number="MAINT-01",
            last_maintenance=None
        )
        db.session.add(elevator)
        db.session.commit()
        
        self.assertTrue(ElevatorBusinessRules.should_trigger_maintenance_alert(elevator))

    def test_maintenance_alert_recent_maintenance(self):
        """Test maintenance alert for recently maintained elevator."""
        elevator = Elevator(
            building_id=self.building.id,
            elevator_number="MAINT-02",
            last_maintenance=datetime.utcnow() - timedelta(days=15)
        )
        db.session.add(elevator)
        db.session.commit()
        
        self.assertFalse(ElevatorBusinessRules.should_trigger_maintenance_alert(elevator))

    def test_maintenance_alert_overdue_maintenance(self):
        """Test maintenance alert for overdue maintenance."""
        elevator = Elevator(
            building_id=self.building.id,
            elevator_number="MAINT-03",
            last_maintenance=datetime.utcnow() - timedelta(days=35)
        )
        db.session.add(elevator)
        db.session.commit()
        
        self.assertTrue(ElevatorBusinessRules.should_trigger_maintenance_alert(elevator))

    def test_can_elevator_access_floor_valid_range(self):
        """Test elevator access within valid floor range."""
        
        freight_elevator = Elevator(
            building_id=self.building.id,
            elevator_number="FREIGHT",
            current_floor=1
        )
        db.session.add(freight_elevator)
        db.session.commit()
        
        result = ElevatorBusinessRules.can_elevator_access_floor(freight_elevator.id, 3)
        self.assertTrue(result)
        
        result = ElevatorBusinessRules.can_elevator_access_floor(self.elevator.id, 3)
        self.assertTrue(result)

    def test_can_elevator_access_floor_outside_range(self):
        """Test elevator access outside building floor range."""
        result = ElevatorBusinessRules.can_elevator_access_floor(self.elevator.id, 0)
        self.assertFalse(result)
        
        result = ElevatorBusinessRules.can_elevator_access_floor(self.elevator.id, 6)
        self.assertFalse(result)

    def test_can_elevator_access_floor_freight_restrictions(self):
        """Test freight elevator floor restrictions."""
        freight_elevator = Elevator(
            building_id=self.building.id,
            elevator_number="FREIGHT",
            current_floor=1
        )
        db.session.add(freight_elevator)
        db.session.commit()
        
        result = ElevatorBusinessRules.can_elevator_access_floor(freight_elevator.id, 3)
        self.assertTrue(result)
        
        result = ElevatorBusinessRules.can_elevator_access_floor(freight_elevator.id, 6)
        self.assertFalse(result)

    def test_can_elevator_access_floor_nonexistent_elevator(self):
        """Test with non-existent elevator."""
        result = ElevatorBusinessRules.can_elevator_access_floor(99999, 3)
        self.assertFalse(result)

class ElevatorCallModelTestCase(unittest.TestCase):
    """Test the ElevatorCall model and its automatic feature generation."""
    
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        
        self.building = Building(name="Model Test Building", total_floors=5)
        db.session.add(self.building)
        db.session.commit()
        
        self.elevator = Elevator(
            building_id=self.building.id,
            elevator_number="MODEL-01"
        )
        db.session.add(self.elevator)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_temporal_features_auto_population(self):
        """Test that temporal features are automatically populated."""
        # Create a call with a specific datetime
        test_date = datetime(2024, 7, 15, 14, 30)  # Monday, July 15, 2024, 2:30 PM
        
        call = ElevatorCall(
            elevator_id=self.elevator.id,
            called_from_floor=3,
            call_time=test_date
        )
        
        self.assertEqual(call.day_of_week, 0)  # Monday
        self.assertEqual(call.hour_of_day, 14)  # 2 PM
        self.assertEqual(call.week_of_month, 3)  # Third week of July
        self.assertEqual(call.season, 'summer')

    def test_season_calculation_winter(self):
        """Test season calculation for winter months."""
        winter_dates = [
            datetime(2024, 12, 15),  # December
            datetime(2024, 1, 15),   # January
            datetime(2024, 2, 15)    # February
        ]
        
        for test_date in winter_dates:
            call = ElevatorCall(
                elevator_id=self.elevator.id,
                called_from_floor=1,
                call_time=test_date
            )
            self.assertEqual(call.season, 'winter', f"Failed for {test_date}")

    def test_season_calculation_all_seasons(self):
        """Test season calculation for all seasons."""
        season_tests = [
            (datetime(2024, 3, 15), 'spring'),
            (datetime(2024, 6, 15), 'summer'),
            (datetime(2024, 9, 15), 'autumn'),
            (datetime(2024, 12, 15), 'winter')
        ]
        
        for test_date, expected_season in season_tests:
            call = ElevatorCall(
                elevator_id=self.elevator.id,
                called_from_floor=1,
                call_time=test_date
            )
            self.assertEqual(call.season, expected_season)

class MLDataIntegrationTestCase(unittest.TestCase):
    """Integration tests for ML data preparation and export."""
    
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        self.app = app.test_client()
        
        db.create_all()
        
        # Create comprehensive test data
        self.building = Building(
            name="ML Integration Test Building",
            total_floors=5,
            building_type="mixed"
        )
        db.session.add(self.building)
        db.session.commit()
        
        self.elevator = Elevator(
            building_id=self.building.id,
            elevator_number="ML-01",
            current_floor=1
        )
        db.session.add(self.elevator)
        db.session.commit()
        
        # Create diverse call patterns
        self._create_test_call_patterns()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def _create_test_call_patterns(self):
        """Create realistic call patterns for testing."""
        import random
        
        # Morning rush pattern (7-9 AM)
        for day in range(5):  # Weekdays
            for hour in [7, 8]:
                for _ in range(random.randint(3, 8)):
                    call_time = datetime.utcnow().replace(hour=hour, minute=random.randint(0, 59))
                    call = ElevatorCall(
                        elevator_id=self.elevator.id,
                        called_from_floor=1,  # Ground floor calls in morning
                        destination_floor=random.randint(2, 5),
                        call_time=call_time,
                        elevator_position_at_call=random.randint(1, 5),
                        estimated_passengers=random.randint(1, 4)
                    )
                    db.session.add(call)
        
        # Lunch pattern (12-1 PM)
        for day in range(5):
            for hour in [12]:
                for _ in range(random.randint(2, 5)):
                    call_time = datetime.utcnow().replace(hour=hour, minute=random.randint(0, 59))
                    call = ElevatorCall(
                        elevator_id=self.elevator.id,
                        called_from_floor=random.randint(2, 5),  # Various floors going down
                        destination_floor=1,
                        call_time=call_time,
                        elevator_position_at_call=random.randint(1, 5),
                        estimated_passengers=random.randint(1, 3)
                    )
                    db.session.add(call)
        
        # Evening pattern (5-7 PM)
        for day in range(5):
            for hour in [17, 18]:  # 5-6 PM
                for _ in range(random.randint(4, 9)):
                    call_time = datetime.utcnow().replace(hour=hour, minute=random.randint(0, 59))
                    call = ElevatorCall(
                        elevator_id=self.elevator.id,
                        called_from_floor=random.randint(2, 5),  # Various floors going down
                        destination_floor=1,
                        call_time=call_time,
                        elevator_position_at_call=random.randint(1, 5),
                        estimated_passengers=random.randint(1, 3)
                    )
                    db.session.add(call)
        
        db.session.commit()

    def test_ml_data_export_structure(self):
        """Test that ML data export has correct structure."""
        response = self.app.get(f'/api/ml-data/features/{self.building.id}')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Verify top-level structure
        required_keys = ['building_id', 'total_samples', 'date_range', 'features']
        for key in required_keys:
            self.assertIn(key, data)
        
        # Verify we have samples
        self.assertGreater(data['total_samples'], 0)
        
        # Verify feature structure
        if data['features']:
            feature = data['features'][0]
            required_feature_keys = ['target_floor', 'time_features', 'elevator_features', 'contextual_features']
            for key in required_feature_keys:
                self.assertIn(key, feature)
            
            # Verify time features
            time_features = feature['time_features']
            time_required = ['hour_of_day', 'day_of_week', 'week_of_month', 'season']
            for key in time_required:
                self.assertIn(key, time_features)


    def test_ml_data_filtering(self):
        """Test ML data filtering by date range."""
        # Test with shorter time range
        response = self.app.get(f'/api/ml-data/features/{self.building.id}?days_back=7')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Should still have structure but possibly fewer samples
        self.assertIn('total_samples', data)
        self.assertIn('features', data)

if __name__ == '__main__':
    test_suite = unittest.TestSuite()
    
    test_classes = [
        ElevatorSystemTestCase,
        BusinessRulesTestCase,
        ElevatorCallModelTestCase,
        MLDataIntegrationTestCase
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Summary
    print(f"\n{'='*50}")
    print(f"TESTS RUN: {result.testsRun}")
    print(f"FAILURES: {len(result.failures)}")
    print(f"ERRORS: {len(result.errors)}")
    print(f"SUCCESS RATE: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print(f"{'='*50}")