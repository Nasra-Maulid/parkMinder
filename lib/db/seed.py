from models import Vehicle, ParkingSpot, Payment, session
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker()

def seed_database():
    # Clear existing data
    session.query(Payment).delete()
    session.query(Vehicle).delete()
    session.query(ParkingSpot).delete()
    
    # Create parking spots
    spot_types = ['regular', 'handicap', 'electric']
    spots = []
    for i in range(1, 21):
        spot_type = random.choice(spot_types)
        spot = ParkingSpot(
            spot_number=f"{spot_type[0].upper()}{i:03d}",
            spot_type=spot_type,
            is_occupied=random.choice([0, 0, 0, 1])  # 25% chance of being occupied
        )
        spots.append(spot)
    
    session.add_all(spots)
    session.commit()
    
    # Create vehicles with payments
    for _ in range(15):
        check_in_time = fake.date_time_this_month()
        check_out_time = check_in_time + timedelta(hours=random.randint(1, 48))
        
        vehicle = Vehicle(
            license_plate=fake.license_plate(),
            vehicle_type=random.choice(['car', 'truck', 'motorcycle']),
            check_in_time=check_in_time,
            check_out_time=check_out_time if random.choice([True, False]) else None,
            parking_spot_id=random.choice([s.id for s in spots if s.is_occupied])
        )
        
        session.add(vehicle)
        session.commit()
        
        if vehicle.check_out_time:
            hours_parked = (vehicle.check_out_time - vehicle.check_in_time).total_seconds() / 3600
            rate = 2.5  # $2.50 per hour
            amount = round(hours_parked * rate, 2)
            
            payment = Payment(
                vehicle_id=vehicle.id,
                amount=amount,
                payment_time=vehicle.check_out_time,
                payment_method=random.choice(['cash', 'credit', 'mobile']),
                is_paid=random.choice([0, 1])
            )
            
            session.add(payment)
    
    session.commit()
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()