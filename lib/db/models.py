import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# -------------------
# Model Definitions
# -------------------

class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key=True)
    license_plate = Column(String, unique=True, nullable=False)
    vehicle_type = Column(String)
    check_in_time = Column(DateTime, default=datetime.now)
    check_out_time = Column(DateTime)
    parking_spot_id = Column(Integer, ForeignKey('parking_spots.id'))

    parking_spot = relationship("ParkingSpot", back_populates="vehicles")
    payment = relationship("Payment", back_populates="vehicle", uselist=False)

    def __repr__(self):
        return f"<Vehicle(license_plate='{self.license_plate}', type='{self.vehicle_type}')>"

class ParkingSpot(Base):
    __tablename__ = 'parking_spots'

    id = Column(Integer, primary_key=True)
    spot_number = Column(String, unique=True, nullable=False)
    spot_type = Column(String, nullable=False)
    is_occupied = Column(Integer, default=0)

    vehicles = relationship("Vehicle", back_populates="parking_spot")

    def __repr__(self):
        return f"<ParkingSpot(spot_number='{self.spot_number}', type='{self.spot_type}', occupied={bool(self.is_occupied)})>"

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=False)
    amount = Column(Float)
    payment_time = Column(DateTime, default=datetime.now)
    payment_method = Column(String)
    is_paid = Column(Integer, default=0)

    vehicle = relationship("Vehicle", back_populates="payment")

    def __repr__(self):
        return f"<Payment(amount={self.amount}, method='{self.payment_method}', paid={bool(self.is_paid)})>"

# -------------------
# Optional Setup
# -------------------

# Absolute path to the database under lib/db/
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'parkminder.db'))
engine = create_engine(f"sqlite:///{DB_PATH}")

# Only create tables if explicitly run
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Database tables created.")

Session = sessionmaker(bind=engine)
session = Session()
