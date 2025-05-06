#Author: Sawiru Wimalatunge
#Date: 10.12.2024
#Student ID: w2120775 / 20232505

#Task A: Input Validation

def validate_date_input():
    """
    Validates user input for the date (day(DD), month(MM), and year(YYYY)) to ensure they are within the expected range.
    Returns the day, month, and year.
    """
    
    #creating a dictionary with the months and the dates
    days_in_month = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 
                     7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    
    while True:
        # Validate day
        while True:
            try:
                day = int(input("Please enter the day of the survey in the format dd: "))
                if day < 1 or day > 31: #checking if the day is in range 1 to 31.
                    print("Out of range - values must be in the range 1 and 31.")
                    continue 
                break #break out of the loop and prompt the user for an input again.
            except ValueError: #prompt the user if the value is not an integer. 
                print("Integer required.")
        
        # Validate month
        while True:
            try:
                month = int(input("Please enter the month of the survey in the format MM: "))
                if month < 1 or month > 12: #checking if month is in range 1 to 12.
                    print("Out of range - values must be in the range 1 to 12.")
                    continue
                break
            except ValueError:
                print("Integer required.")

        # Validate year
        while True:
            try:
                year = int(input("Please enter the year of the survey in the format YYYY: "))
                if year < 2000 or year > 2024: #checking if year is in range 2000 to 2024.
                    print("Out of range - values must range from 2000 and 2024.")
                    continue
                break
            except ValueError:
                print("Integer required.")
        
        #checks if the given date is a leap year
        if leap_year(year):
            days_in_month[2] = 29 # if it's a leap year february will have 29 days
        else:
            days_in_month[2] = 28 # else will have 28 days
        
        if day > days_in_month[month]:
            print(f"Invalid date - day must be between 1 and {days_in_month[month]} for month {month}.")
            continue  # Restart the loop to re-enter the entire date
        else:
            # If all inputs are valid, return the date
            return day, month, year
        
def leap_year(year):
        #checks if it's a leap year
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)    

#Task E : Looping
def validate_continue_input():
    """
    Prompts the user to decide whether to load another dataset.
    Returns True if the user wants to continue, otherwise False.
    """
    while True:
        choice = input("Do you want to select a data file for a different date? Y/N : ").strip().upper()
        if choice == "Y": #if 'Y' then loads the new dataset.
            print("Loading new dataset...\n")
            return True
    
        elif choice == "N": #if 'N' then ends the program.
            print("End of run.")
            return False
    
        else:
            print("Please enter 'Y' or 'N'") #prompts the user for a valid input


import csv

# Task B: Process CSV Data
def process_csv_data(file_path):
    """
    Processes a CSV file containing traffic data and calculates various data.
    Returns the outcomes as a list.
    """
    try:
        # Open the CSV file and load its data into a list of dictionaries
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            data = list(reader)
        
        #total amount of vehicles
        total_vehicles = len(data)
        
        #total amount of trucks
        total_trucks = len(["present" for row in data if row["VehicleType"].lower().strip() == "truck"])
        
        #total amount of electric vehicles
        total_electric_vehicles = len(["present" for row in data if row["elctricHybrid"].lower().strip() == "true"])
        
        #total two wheeled vehicles
        total_two_wheeled_vehicles = len(["present" for row in data if row["VehicleType"].lower().strip() in ["bicycle","motorcycle","scooter"]])
        
        #total busses leaving Elm Avenue/Rabbit Road junction that's headed North
        busses_north = len(["present" for row in data if row["VehicleType"].lower().strip() == "buss" and row["JunctionName"].lower().strip() == "elm avenue/rabbit road" and row["travel_Direction_out"].lower().strip() == "n" ])
        
        #total vehicles passing through without turning left or right
        vehicles_straight = len(["present" for row in data if row["travel_Direction_in"] == row["travel_Direction_out"]])
        
        #percentage of all vehicles that are Trucks
        truck_percentage = round((total_trucks/total_vehicles)*100)
        
        #average number of bicycles per hour
        avg_bicycles_per_hour = round(len(["present" for row in data if row["VehicleType"].lower().strip() == "bicycle"])/24)
        
        #total vehicles over the speed limit
        over_speed_limit = len(["present" for row in data if int(row["VehicleSpeed"]) > int(row["JunctionSpeedLimit"])])
        
        #total vehicles through Elm Avenue/Rabbit Road 
        vehicles_elm_rabbit = len(["present" for row in data if row["JunctionName"].lower().strip() == "elm avenue/rabbit road"])
        
        #total vehicles through Hanley Highway/Westway junction 
        vehicles_hanley_westway = len(["present" for row in data if row["JunctionName"].lower().strip() == "hanley highway/westway"])
        
        #scooters through Elm Avenue/Rabbit Road 
        scooters_percentage_elm = int((len(["present" for row in data if row["VehicleType"].lower().strip() == "scooter" and row ["JunctionName"].lower().strip() == "elm avenue/rabbit road"])/vehicles_elm_rabbit)*100)
        
        #calculate total hours of rain
        rain_hours = set()  # Create a set to store rain hours
        for row in data:
            if "rain" in row["Weather_Conditions"].lower().strip():
                hour = int(row["timeOfDay"].split(":")[0])  # Extract the hour 
                rain_hours.add(hour)  # Add the hour to the set if it is raining

        total_rain_hours = len(rain_hours)  # The size of the set is the count of total raining hours
    
        # Calculate peak hours at Hanley Highway/Westway
        hanley_hourly_count = {}
        for row in data:
            if "Hanley Highway/Westway" in row["JunctionName"]:
                hour = int(row["timeOfDay"].split(":")[0])
                hanley_hourly_count[hour] = hanley_hourly_count.get(hour, 0) + 1

        peak_hour_vehicle_count_hanley = max(hanley_hourly_count.values()) # the peak hour vehicle count
        peak_hours = [hour for hour, count in hanley_hourly_count.items() if count == peak_hour_vehicle_count_hanley]
        peak_hour_time_hanley = f"between {peak_hours[0]}:00 and {peak_hours[0] + 1}:00" #times of the peak hours

        

        # loading all outcomes to a list
        outcomes = [
            total_vehicles, total_trucks, total_electric_vehicles, total_two_wheeled_vehicles, 
            busses_north, vehicles_straight, truck_percentage, avg_bicycles_per_hour, 
            over_speed_limit, vehicles_elm_rabbit, vehicles_hanley_westway, scooters_percentage_elm, 
            peak_hour_vehicle_count_hanley, peak_hour_time_hanley, total_rain_hours
        ]
        return outcomes
    
    except FileNotFoundError:
        print(f"Invalid input. No file available for the date you entered.")
        return None


def display_outcomes(outcomes):
# Displays the calculated outcomes in a formatted manner.
    
    print(f"""The total number of vehicles recorded for this date is {outcomes[0]}
The total number of trucks recorded for this date is {outcomes[1]}
The total number of electric vehicles recorded for this date is {outcomes[2]}
The total number of two-wheeled vehicles recorded for this date is {outcomes[3]}
The total number of busses leaving Elm Avenue/Rabbit Road heading North is {outcomes[4]}
The total number of vehicles passing through both junctions without turning left or right is  {outcomes[5]}
The percentage of all vehicles recorded that are trucks for this date is {outcomes[6]}%
The average number of bicycles per hour for this date is {outcomes[7]}
The total number of vehicles recorded as over the speed limit for this date is {outcomes[8]}
The total number of vehicles recorded through only Elm Avenue/Rabbit Road junction for this date is {outcomes[9]}
The total number of vehicles recorded through only Hanley Highway/Westway junction for this date is {outcomes[10]}
{outcomes[11]}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.
The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes[12]}
The most vehicles through Hanley Highway/Westway were recorded {outcomes[13]}
The number of hours of rain for this date is {outcomes[14]}

****************************************************

""")

# Task C: Save Results to Text File
def save_results_to_file(outcomes, filename, file_name="results.txt"):
    """
    Saves the processed outcomes to a text file and appends if the program loops.
    """
    content = f"""data file selected is {filename}
The total number of vehicles recorded for this date is {outcomes[0]}
The total number of trucks recorded for this date is {outcomes[1]}
The total number of electric vehicles recorded for this date is {outcomes[2]}
The total number of two-wheeled vehicles recorded for this date is {outcomes[3]}
The total number of busses leaving Elm Avenue/Rabbit Road heading North is {outcomes[4]}
The total number of vehicles passing through both junctions without turning left or right is  {outcomes[5]}
The percentage of all vehicles recorded that are trucks for this date is {outcomes[6]}%
The average number of bicycles per hour for this date is {outcomes[7]}
The total number of vehicles recorded as over the speed limit for this date is {outcomes[8]}
The total number of vehicles recorded through only Elm Avenue/Rabbit Road junction for this date is {outcomes[9]}
The total number of vehicles recorded through only Hanley Highway/Westway junction for this date is {outcomes[10]}
{outcomes[11]}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.
The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes[12]}
The most vehicles through Hanley Highway/Westway were recorded {outcomes[13]}
The number of hours of rain for this date is {outcomes[14]}

****************************************************

"""
    #open the file in append mode and write to it
    with open(file_name, "a+") as file:
        file.write(content)
        

