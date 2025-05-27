from db.models import session, Vehicle, ParkingSpot, Payment
from datetime import datetime
import sys

def display_welcome():
    print("\n" + "="*50)
    print(" " * 15 + "PARKMINDER SYSTEM")
    print("="*50 + "\n")

def display_main_menu():
    print("\nMAIN MENU:")
    print("1. Vehicle Operations")
    print("2. Parking Spot Operations")
    print("3. Payment Operations")
    print("4. Reports")
    print("5. Exit")
    return input("Please select an option (1-5): ")

def display_vehicle_menu():
    print("\nVEHICLE OPERATIONS:")
    print("1. Check-in Vehicle")
    print("2. Check-out Vehicle")
    print("3. View All Vehicles")
    print("4. Find Vehicle by License Plate")
    print("5. Back to Main Menu")
    return input("Please select an option (1-5): ")

def display_spot_menu():
    print("\nPARKING SPOT OPERATIONS:")
    print("1. View All Parking Spots")
    print("2. View Available Spots")
    print("3. Add New Parking Spot")
    print("4. Back to Main Menu")
    return input("Please select an option (1-4): ")

def display_payment_menu():
    print("\nPAYMENT OPERATIONS:")
    print("1. Process Payment")
    print("2. View All Payments")
    print("3. View Unpaid Payments")
    print("4. Back to Main Menu")
    return input("Please select an option (1-4): ")

def display_reports_menu():
    print("\nREPORTS:")
    print("1. Daily Revenue Report")
    print("2. Occupancy Report")
    print("3. Back to Main Menu")
    return input("Please select an option (1-3): ")

def get_valid_input(prompt, input_type=str):
    while True:
        try:
            user_input = input_type(input(prompt))
            return user_input
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")

def find_vehicle_by_plate(license_plate):
    return session.query(Vehicle).filter_by(license_plate=license_plate).first()

def find_available_spot(spot_type='regular'):
    return session.query(ParkingSpot).filter_by(spot_type=spot_type, is_occupied=0).first()

def calculate_parking_fee(check_in_time, check_out_time=None):
    if not check_out_time:
        check_out_time = datetime.now()
    duration = (check_out_time - check_in_time).total_seconds() / 3600  # hours
    return round(duration * 2.5, 2)  # $2.50 per hour