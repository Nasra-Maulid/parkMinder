#!/usr/bin/env python3

from helpers import (
    display_welcome, display_main_menu, display_vehicle_menu, display_spot_menu,
    display_payment_menu, display_reports_menu, vehicle_check_in, vehicle_check_out,
    view_all_vehicles, find_vehicle_by_plate, view_all_spots, view_available_spots,
    add_new_spot, process_payment, view_all_payments, view_unpaid_payments,
    daily_revenue_report, occupancy_report
)

def main():
    display_welcome()
    
    while True:
        choice = display_main_menu()
        
        if choice == '1':  # Vehicle Operations
            while True:
                vehicle_choice = display_vehicle_menu()
                
                if vehicle_choice == '1':
                    vehicle_check_in()
                elif vehicle_choice == '2':
                    vehicle_check_out()
                elif vehicle_choice == '3':
                    view_all_vehicles()
                elif vehicle_choice == '4':
                    license_plate = input("Enter license plate to search: ").strip().upper()
                    vehicle = find_vehicle_by_plate(license_plate)
                    if vehicle:
                        print("\nVEHICLE FOUND:")
                        print(f"License Plate: {vehicle.license_plate}")
                        print(f"Type: {vehicle.vehicle_type}")
                        print(f"Check-in Time: {vehicle.check_in_time}")
                        print(f"Check-out Time: {vehicle.check_out_time if vehicle.check_out_time else 'Not checked out'}")
                        print(f"Parking Spot: {vehicle.parking_spot.spot_number}")
                    else:
                        print("Vehicle not found.")
                elif vehicle_choice == '5':
                    break
                else:
                    print("Invalid choice. Please try again.")
        
        elif choice == '2':  # Parking Spot Operations
            while True:
                spot_choice = display_spot_menu()
                
                if spot_choice == '1':
                    view_all_spots()
                elif spot_choice == '2':
                    view_available_spots()
                elif spot_choice == '3':
                    add_new_spot()
                elif spot_choice == '4':
                    break
                else:
                    print("Invalid choice. Please try again.")
        
        elif choice == '3':  # Payment Operations
            while True:
                payment_choice = display_payment_menu()
                
                if payment_choice == '1':
                    process_payment()
                elif payment_choice == '2':
                    view_all_payments()
                elif payment_choice == '3':
                    view_unpaid_payments()
                elif payment_choice == '4':
                    break
                else:
                    print("Invalid choice. Please try again.")
        
        elif choice == '4':  # Reports
            while True:
                report_choice = display_reports_menu()
                
                if report_choice == '1':
                    daily_revenue_report()
                elif report_choice == '2':
                    occupancy_report()
                elif report_choice == '3':
                    break
                else:
                    print("Invalid choice. Please try again.")
        
        elif choice == '5':  # Exit
            print("\nThank you for using ParkMinder. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()