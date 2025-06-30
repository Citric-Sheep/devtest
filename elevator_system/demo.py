#!/usr/bin/env python3
"""
Elevator Prediction System Demo
This script demonstrates the ML-focused elevator system that captures the "golden event".
"""

import requests
import time
import random

BASE_URL = "http://localhost:5000"

def call_elevator(floor, destination_floor=None):
    """Call the elevator from a specific floor"""
    data = {'floor': floor}
    if destination_floor:
        data['destination_floor'] = destination_floor
    
    response = requests.post(f"{BASE_URL}/call", json=data)
    if response.status_code == 201:
        return response.json()
    else:
        print(f"Error calling elevator: {response.text}")
        return None

def step_simulation():
    """Advance the simulation by one time unit"""
    response = requests.post(f"{BASE_URL}/step")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error stepping simulation: {response.text}")
        return None

def get_status():
    """Get current elevator status"""
    response = requests.get(f"{BASE_URL}/status")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error getting status: {response.text}")
        return None

def get_logs():
    """Get demand logs for ML training"""
    response = requests.get(f"{BASE_URL}/logs")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error getting logs: {response.text}")
        return None

def get_stats():
    """Get statistics for ML insights"""
    response = requests.get(f"{BASE_URL}/stats")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error getting stats: {response.text}")
        return None

def simulate_elevator_cycle(call_floor, destination_floor):
    """Simulate a complete elevator cycle"""
    print(f"\n=== Elevator Cycle ===")
    print(f"Call from floor: {call_floor}")
    print(f"Destination: {destination_floor}")
    
    # 1. Call the elevator
    result = call_elevator(call_floor, destination_floor)
    
    # 2. Step simulation until elevator reaches call floor  
    current_floor = result['elevator_state']['current_floor']  # Get actual elevator position from state
    print(f"Current floor: {current_floor}")
    ini_current_floor = current_floor
    # If elevator is already at call floor, we need one step to "arrive" there
    if current_floor == call_floor:
        step_result = step_simulation()
        print(f"Step result (arriving at call floor)...")
        current_floor = step_result['elevator_state']['current_floor']
    else:
        # Step until elevator reaches call floor
        while current_floor != call_floor:
            step_result = step_simulation()
            # print(f"Step result (until call floor): {step_result}")
            if step_result and step_result['moved']:
                current_floor = step_result['elevator_state']['current_floor']
                print(f"Moved to floor {current_floor} (until call floor)")
            else:
                # Elevator arrived at call floor
                current_floor = step_result['elevator_state']['current_floor']
                if current_floor == call_floor:
                    print(f"Arrived at call floor {current_floor}")
                break
    
    # 3. Step simulation until elevator reaches destination
    # First, ensure we've properly arrived at the call floor
    if current_floor == call_floor:
        # Take one more step to ensure the elevator has processed the call floor arrival
        step_result = step_simulation()
        print(f"Step result (processing call floor arrival)...")
        current_floor = step_result['elevator_state']['current_floor']
        if ini_current_floor == call_floor:
            print(f"Moved to floor {current_floor} (until destination floor)")
    # Now step until we reach the destination
    while current_floor != destination_floor:
        step_result = step_simulation()
        # print(f"Step result (until destination floor): {step_result}")
        if step_result and step_result['moved']:
            current_floor = step_result['elevator_state']['current_floor']
            print(f"Moved to floor {current_floor} (until destination floor)")
        else:
            # Elevator arrived at destination or stopped
            current_floor = step_result['elevator_state']['current_floor']
            if current_floor == destination_floor:
                print(f"Arrived at destination floor {current_floor}")
            break
    
    # 4. Final step to arrive and start resting
    step_result = step_simulation()
    if step_result:
        print(f"Arrived and started resting")
    
    return current_floor

def simulate_office_building():
    """Simulate a typical office building day"""
    print("=== Office Building Elevator Simulation ===")
    
    floors = list(range(1, 11))  # 10 floors
    
    # Morning rush hour (8-9 AM) - people coming to work
    print("\n--- Morning Rush Hour (8-9 AM) ---")
    for i in range(6):
        # Most people come from ground floor to various floors
        destination_floor = random.choice(floors[1:])  # Not ground floor
        simulate_elevator_cycle(1, destination_floor)
        time.sleep(0.1)  # Small delay between cycles
    
    # Mid-morning (9-11 AM) - some movement between floors
    print("\n--- Mid-Morning (9-11 AM) ---")
    for i in range(2):
        call_floor = random.choice(floors)
        destination_floor = random.choice([f for f in floors if f != call_floor])
        simulate_elevator_cycle(call_floor, destination_floor)
        time.sleep(0.1)
    
    # Lunch time (12-1 PM) - people going to cafeteria (floor 2)
    print("\n--- Lunch Time (12-1 PM) ---")
    for i in range(4):
        call_floor = random.choice(floors)
        simulate_elevator_cycle(call_floor, 2)  # Cafeteria floor
        time.sleep(0.1)
    
    # After lunch (1-2 PM) - people returning to their floors
    print("\n--- After Lunch (1-2 PM) ---")
    for i in range(4):
        destination_floor = random.choice(floors[1:])  # To various floors
        simulate_elevator_cycle(2, destination_floor)  # From cafeteria
        time.sleep(0.1)
    
    # Afternoon (2-5 PM) - some movement
    print("\n--- Afternoon (2-5 PM) ---")
    for i in range(2):
        call_floor = random.choice(floors)
        destination_floor = random.choice([f for f in floors if f != call_floor])
        simulate_elevator_cycle(call_floor, destination_floor)
        time.sleep(0.1)
    
    # Evening rush (5-6 PM) - people leaving work
    print("\n--- Evening Rush (5-6 PM) ---")
    for i in range(6):
        call_floor = random.choice(floors[1:])  # From various floors
        simulate_elevator_cycle(call_floor, 1)  # To ground floor
        time.sleep(0.1)

def analyze_ml_data():
    """Analyze the collected data for ML insights"""
    print("\n=== ML Data Analysis ===")
    
    # Get logs
    logs_data = get_logs()
    if not logs_data:
        return
    
    logs = logs_data['logs']
    print(f"\nTotal golden events captured: {len(logs)}")
    
    if len(logs) == 0:
        print("No data collected yet. Run some simulation first.")
        return
    
    # Analyze resting floor patterns
    resting_floor_counts = {}
    call_floor_counts = {}
    
    for log in logs:
        resting_floor = log['resting_floor']
        call_floor = log['call_floor']
        
        resting_floor_counts[resting_floor] = resting_floor_counts.get(resting_floor, 0) + 1
        call_floor_counts[call_floor] = call_floor_counts.get(call_floor, 0) + 1
    
    print("\nResting Floor Analysis:")
    for floor, count in sorted(resting_floor_counts.items()):
        print(f"  Floor {floor}: {count} times")
    
    print("\nCall Floor Analysis:")
    for floor, count in sorted(call_floor_counts.items()):
        print(f"  Floor {floor}: {count} calls")
    
    # Find most common call floor
    if call_floor_counts:
        most_common_call_floor = max(call_floor_counts, key=call_floor_counts.get)
        print(f"\nMost common call floor: {most_common_call_floor} ({call_floor_counts[most_common_call_floor]} calls)")
    
    # Analyze time patterns
    hour_counts = {}
    for log in logs:
        hour = log['hour_of_day']
        hour_counts[hour] = hour_counts.get(hour, 0) + 1
    
    print("\nHourly Call Patterns:")
    for hour in sorted(hour_counts.keys()):
        print(f"  {hour:02d}:00: {hour_counts[hour]} calls")
    
    # Get statistics
    stats = get_stats()
    if stats and stats['resting_patterns']:
        print("\nResting → Call Patterns:")
        for pattern in stats['resting_patterns'][:5]:  # Show top 5
            print(f"  Resting on {pattern['resting_floor']} → Call from {pattern['call_floor']}: {pattern['count']} times")

def main():
    """Main demonstration function"""
    print("Starting Elevator Prediction System Demo")
    print("Make sure the system is running on http://localhost:5000")
    
    # Check if system is running
    try:
        status = get_status()
        if status:
            print("Elevator system is running")
            print(f"Current logs: {status['total_logs']}")
        else:
            print("Elevator system is running (no activity yet)")
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to elevator system")
        print("Please start the system with: python main.py")
        return
    
    # Run simulation
    simulate_office_building()
    
    # Analyze data
    analyze_ml_data()
    
    # Show final status
    final_status = get_status()
    if final_status:
        print(f"\nFinal elevator state:")
        elevator_state = final_status['elevator']
        print(f"   Current floor: {elevator_state['current_floor']}")
        print(f"   Is resting: {elevator_state['is_resting']}")
        print(f"   Direction: {elevator_state['direction']}")
        print(f"   Total golden events: {final_status['total_logs']}")
    
    print("\nDemo completed!")
    print("The collected data can now be used to train ML models for optimal resting floor prediction.")
    print("\nKey ML Features Collected:")
    print("  - resting_floor: Where elevator was idle")
    print("  - call_floor: Where the next call came from")
    print("  - timestamp_rested: When elevator became idle")
    print("  - timestamp_called: When call was received")
    print("  - day_of_week: Day of the week (0-6)")
    print("  - hour_of_day: Hour of the day (0-23)")

if __name__ == "__main__":
    main() 