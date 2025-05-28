from db.models import session, Vehicle, ParkingSpot, Payment
from datetime import datetime, timedelta
import ipdb

def debug_session():
    print("\nDEBUG MODE ACTIVATED")
    print("Available objects:")
    print("- session: SQLAlchemy session")
    print("- Vehicle: Vehicle model class")
    print("- ParkingSpot: ParkingSpot model class")
    print("- Payment: Payment model class")
    print("- datetime: Python datetime module")
    print("- timedelta: Python timedelta class")
    print("\nStarting ipdb session...")
    ipdb.set_trace()

if __name__ == "__main__":
    debug_session()