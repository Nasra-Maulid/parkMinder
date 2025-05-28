# ParkMinder - Parking Management System

ParkMinder is a comprehensive parking management system that allows operators to manage vehicles, parking spots, and payments through a command-line interface.

## Features

- Vehicle check-in and check-out
- Parking spot management
- Payment processing
- Reporting (revenue, occupancy)
- Database persistence with SQLAlchemy

## Database Schema

The system uses three main tables:

1. **vehicles** - Tracks all vehicles in the parking lot
   - license_plate (unique identifier)
   - vehicle_type
   - check_in_time
   - check_out_time
   - parking_spot_id (foreign key)

2. **parking_spots** - Manages all parking spots
   - spot_number (unique identifier)
   - spot_type (regular, handicap, electric)
   - is_occupied (boolean)

3. **payments** - Records all payments
   - vehicle_id (foreign key)
   - amount
   - payment_time
   - payment_method
   - is_paid (boolean)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Nasra-Maulid/parkMinder
   cd parkminder

2. Set up the environment:
    pipenv install
    pipenv shell

3. Initialize the database:
    PYTHONPATH=. alembic upgrade head
    PYTHONPATH=. python lib/db/seed.py
 
