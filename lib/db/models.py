from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import os

Base = declarative_base()

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
    spot_type = Column(String, nullable=False)  # 'regular', 'handicap', 'electric'
    is_occupied = Column(Integer, default=0)  # 0 for available, 1 for occupied
    
    vehicles = relationship("Vehicle", back_populates="parking_spot")
    
    def __repr__(self):
        return f"<ParkingSpot(spot_number='{self.spot_number}', type='{self.spot_type}', occupied={bool(self.is_occupied)})>"

class Payment(Base):
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=False)
    amount = Column(Float)
    payment_time = Column(DateTime, default=datetime.now)
    payment_method = Column(String)  # 'cash', 'credit', 'mobile'
    is_paid = Column(Integer, default=0)  # 0 for unpaid, 1 for paid
    
    vehicle = relationship("Vehicle", back_populates="payment")
    
    def __repr__(self):
        return f"<Payment(amount={self.amount}, method='{self.payment_method}', paid={bool(self.is_paid)})>"

# Database setup
engine = create_engine('sqlite:///parkminder.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()