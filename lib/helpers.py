from db.models import session, Vehicle, ParkingSpot, Payment
from datetime import datetime
from sqlalchemy import func, case
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

def view_all_spots():
    spots = session.query(ParkingSpot).order_by(ParkingSpot.spot_number).all()
    if not spots:
        print("No parking spots found in the system.")
        return
    
    print("\nALL PARKING SPOTS:")
    print("-" * 60)
    print(f"{'Spot Number':<15}{'Type':<15}{'Status':<30}")
    print("-" * 60)
    
    for spot in spots:
        status = "Occupied" if spot.is_occupied else "Available"
        print(f"{spot.spot_number:<15}{spot.spot_type:<15}{status:<30}")

def view_available_spots():
    spots = session.query(ParkingSpot).filter_by(is_occupied=0).order_by(ParkingSpot.spot_number).all()
    if not spots:
        print("No available parking spots.")
        return
    
    print("\nAVAILABLE PARKING SPOTS:")
    print("-" * 45)
    print(f"{'Spot Number':<15}{'Type':<15}{'Status':<15}")
    print("-" * 45)
    
    for spot in spots:
        print(f"{spot.spot_number:<15}{spot.spot_type:<15}{'Available':<15}")

def add_new_spot():
    print("\nADD NEW PARKING SPOT")
    spot_number = input("Enter spot number (e.g., R001, H002, E003): ").strip().upper()
    
    existing_spot = session.query(ParkingSpot).filter_by(spot_number=spot_number).first()
    if existing_spot:
        print("Error: Spot with this number already exists.")
        return
    
    spot_type = input("Enter spot type (regular/handicap/electric): ").lower()
    while spot_type not in ['regular', 'handicap', 'electric']:
        print("Invalid spot type. Please enter regular, handicap, or electric.")
        spot_type = input("Enter spot type (regular/handicap/electric): ").lower()
    
    new_spot = ParkingSpot(
        spot_number=spot_number,
        spot_type=spot_type,
        is_occupied=0
    )
    
    session.add(new_spot)
    session.commit()
    
    print(f"\nNew parking spot added successfully!")
    print(f"Spot Number: {new_spot.spot_number}")
    print(f"Spot Type: {new_spot.spot_type.capitalize()}")    

def process_payment():
    print("\nPROCESS PAYMENT")
    license_plate = input("Enter license plate: ").strip().upper()
    
    vehicle = find_vehicle_by_plate(license_plate)
    if not vehicle or not vehicle.check_out_time:
        print("Error: Vehicle not found or not checked out.")
        return
    
    payment = session.query(Payment).filter_by(vehicle_id=vehicle.id, is_paid=0).first()
    if not payment:
        print("Error: No unpaid payment found for this vehicle.")
        return
    
    print(f"\nPayment Due: ${payment.amount:.2f}")
    print(f"Vehicle: {vehicle.license_plate}")
    print(f"Parking Duration: {(vehicle.check_out_time - vehicle.check_in_time)}")
    
    payment_method = input("Enter payment method (cash/credit/mobile): ").lower()
    while payment_method not in ['cash', 'credit', 'mobile']:
        print("Invalid payment method. Please enter cash, credit, or mobile.")
        payment_method = input("Enter payment method (cash/credit/mobile): ").lower()
    
    payment.payment_method = payment_method
    payment.is_paid = 1
    payment.payment_time = datetime.now()
    
    session.commit()
    
    print("\nPayment processed successfully!")
    print(f"Amount Paid: ${payment.amount:.2f}")
    print(f"Payment Method: {payment.payment_method.capitalize()}")
    print(f"Payment Time: {payment.payment_time}")

def view_all_payments():
    payments = session.query(Payment).join(Vehicle).all()
    if not payments:
        print("No payments found in the system.")
        return
    
    print("\nALL PAYMENTS:")
    print("-" * 90)
    print(f"{'License Plate':<15}{'Amount':<10}{'Method':<10}{'Paid':<10}{'Payment Time':<20}{'Check-in':<20}{'Check-out':<20}")
    print("-" * 90)
    
    for payment in payments:
        paid_status = "Yes" if payment.is_paid else "No"
        method = payment.payment_method.capitalize() if payment.payment_method else "N/A"
        payment_time = payment.payment_time.strftime("%Y-%m-%d %H:%M") if payment.payment_time else "N/A"
        
        print(f"{payment.vehicle.license_plate:<15}${payment.amount:<9.2f}{method:<10}{paid_status:<10}{payment_time:<20}{payment.vehicle.check_in_time.strftime('%Y-%m-%d %H:%M'):<20}{payment.vehicle.check_out_time.strftime('%Y-%m-%d %H:%M') if payment.vehicle.check_out_time else 'N/A':<20}")

def view_unpaid_payments():
    payments = session.query(Payment).filter_by(is_paid=0).join(Vehicle).all()
    if not payments:
        print("No unpaid payments found.")
        return
    
    print("\nUNPAID PAYMENTS:")
    print("-" * 70)
    print(f"{'License Plate':<15}{'Amount':<10}{'Check-in':<20}{'Check-out':<20}")
    print("-" * 70)
    
    for payment in payments:
        print(f"{payment.vehicle.license_plate:<15}${payment.amount:<9.2f}{payment.vehicle.check_in_time.strftime('%Y-%m-%d %H:%M'):<20}{payment.vehicle.check_out_time.strftime('%Y-%m-%d %H:%M') if payment.vehicle.check_out_time else 'N/A':<20}")      

def daily_revenue_report():
    date_str = input("Enter date for report (YYYY-MM-DD) or leave blank for today: ").strip()
    if date_str:
        try:
            report_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return
    else:
        report_date = datetime.now().date()
    
    payments = session.query(Payment).filter(
        Payment.is_paid == 1,
        Payment.payment_time >= datetime.combine(report_date, datetime.min.time()),
        Payment.payment_time <= datetime.combine(report_date, datetime.max.time())
    ).all()
    
    total_revenue = sum(p.amount for p in payments)
    
    print(f"\nDAILY REVENUE REPORT FOR {report_date}")
    print("-" * 60)
    print(f"Total Payments Processed: {len(payments)}")
    print(f"Total Revenue: ${total_revenue:.2f}")
    print("\nPayment Methods Breakdown:")
    
    methods = {}
    for payment in payments:
        method = payment.payment_method or 'unknown'
        methods[method] = methods.get(method, 0) + payment.amount
    
    for method, amount in methods.items():
        count = len([p for p in payments if (p.payment_method or 'unknown') == method])
        print(f"{method.capitalize()}: ${amount:.2f} ({count} payments)")
    
    print("-" * 60)

def occupancy_report():
    total_spots = session.query(ParkingSpot).count()
    occupied_spots = session.query(ParkingSpot).filter_by(is_occupied=1).count()
    occupancy_rate = (occupied_spots / total_spots) * 100 if total_spots > 0 else 0
    
    print("\nOCCUPANCY REPORT")
    print("-" * 60)
    print(f"Total Parking Spots: {total_spots}")
    print(f"Occupied Spots: {occupied_spots}")
    print(f"Vacant Spots: {total_spots - occupied_spots}")
    print(f"Occupancy Rate: {occupancy_rate:.1f}%")
    print("\nBy Spot Type:")
    
    spot_types = session.query(
        ParkingSpot.spot_type,
        func.count(ParkingSpot.id).label('total'),
        func.sum(
            case([(ParkingSpot.is_occupied == 1, 1)], else_=0)
        ).label('occupied')
    ).group_by(ParkingSpot.spot_type).all()
    
    for st in spot_types:
        type_occupancy = (st.occupied / st.total) * 100 if st.total > 0 else 0
        print(f"{st.spot_type.capitalize()}: {int(st.occupied)}/{st.total} ({type_occupancy:.1f}%)")
    
    print("-" * 60)