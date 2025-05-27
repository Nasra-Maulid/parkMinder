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

def vehicle_check_in():
    print("\nVEHICLE CHECK-IN")
    license_plate = input("Enter license plate: ").strip().upper()
    
    if find_vehicle_by_plate(license_plate):
        print("Error: Vehicle with this license plate is already checked in.")
        return
    
    vehicle_type = input("Enter vehicle type (car/truck/motorcycle): ").lower()
    while vehicle_type not in ['car', 'truck', 'motorcycle']:
        print("Invalid vehicle type. Please enter car, truck, or motorcycle.")
        vehicle_type = input("Enter vehicle type (car/truck/motorcycle): ").lower()
    
    spot_type = 'regular'
    if vehicle_type == 'truck':
        spot_type = 'regular'
    elif vehicle_type == 'motorcycle':
        spot_type = random.choice(['regular', 'motorcycle'])
    
    spot = find_available_spot(spot_type)
    if not spot:
        print("No available spots of the required type.")
        return
    
    new_vehicle = Vehicle(
        license_plate=license_plate,
        vehicle_type=vehicle_type,
        parking_spot_id=spot.id
    )
    
    spot.is_occupied = 1
    session.add(new_vehicle)
    session.commit()
    
    print(f"\nVehicle checked in successfully!")
    print(f"License Plate: {license_plate}")
    print(f"Assigned Spot: {spot.spot_number}")
    print(f"Check-in Time: {new_vehicle.check_in_time}")

def vehicle_check_out():
    print("\nVEHICLE CHECK-OUT")
    license_plate = input("Enter license plate: ").strip().upper()
    
    vehicle = find_vehicle_by_plate(license_plate)
    if not vehicle or vehicle.check_out_time:
        print("Error: Vehicle not found or already checked out.")
        return
    
    vehicle.check_out_time = datetime.now()
    spot = vehicle.parking_spot
    spot.is_occupied = 0
    
    # Calculate fee
    fee = calculate_parking_fee(vehicle.check_in_time, vehicle.check_out_time)
    
    # Create payment record
    payment = Payment(
        vehicle_id=vehicle.id,
        amount=fee,
        payment_time=vehicle.check_out_time,
        payment_method=None,
        is_paid=0
    )
    
    session.add(payment)
    session.commit()
    
    print(f"\nVehicle checked out successfully!")
    print(f"License Plate: {license_plate}")
    print(f"Parking Duration: {(vehicle.check_out_time - vehicle.check_in_time)}")
    print(f"Total Fee: ${fee:.2f}")

def view_all_vehicles():
    vehicles = session.query(Vehicle).all()
    if not vehicles:
        print("No vehicles found in the system.")
        return
    
    print("\nALL VEHICLES:")
    print("-" * 80)
    print(f"{'License Plate':<15}{'Type':<10}{'Check-in':<20}{'Check-out':<20}{'Spot':<10}")
    print("-" * 80)
    
    for vehicle in vehicles:
        check_out = vehicle.check_out_time.strftime("%Y-%m-%d %H:%M") if vehicle.check_out_time else "Not checked out"
        print(f"{vehicle.license_plate:<15}{vehicle.vehicle_type:<10}{vehicle.check_in_time.strftime('%Y-%m-%d %H:%M'):<20}{check_out:<20}{vehicle.parking_spot.spot_number:<10}")