#Author: Sawiru Wimalatunge
#Date: 24.12.2024
#Student ID: w2120775 / 20232505

import csv
from w2120775_code import validate_date_input, process_csv_data, save_results_to_file, display_outcomes  # Import from task_a_b_c.py
from graphics import *

# Task D: Histogram Display
class HistogramApp:
    def __init__(self, traffic_data, date):
        """
        Initializes the histogram application with the traffic data and selected date.
        """
        self.traffic_data = traffic_data # to store traffic data
        self.date = date # to store the date
        self.win = None #placeholder for the graphical window object

    def setup_window(self):
        """
        Sets up the Tkinter window and canvas for the histogram.
        """
        self.win = GraphWin("Histogram", 1280, 720) #creating the window
        self.win.setBackground(color_rgb(237, 242, 238)) #background colour of the window

    def draw_histogram(self):
        """
        Draws the histogram with axes, labels, and bars.
        """
        margin = 100 #margin around the window
        window_width = 1280
        window_height = 720
        bar_width = 15 #width of each bar
        category_spacing = (window_width - (2 * margin)) / len(self.traffic_data) #space between categories
        max_height = window_height - (4 * margin) # max height for bars
        max_value = max(max(values) for values in self.traffic_data.values()) #max value for bars
        
        # title of the histogram 
        title = Text(Point(window_width / 2, margin), f"Histogram of Vehicle Frequency per Hour ({self.date})")
        title.setSize(16)
        title.setStyle("bold")
        title.setTextColor("black")
        title.draw(self.win) # draws the title on the window
        
        # x-axis line
        x_axis = Line(Point(margin, window_height - margin), Point(window_width - margin - bar_width, window_height - margin))
        x_axis.setOutline("gray")
        x_axis.draw(self.win)
        
        # x-axis label
        x_axis_name = Text(Point((window_width / 2), window_height - margin + 50), "Hours 00:00 to 24:00")
        x_axis_name.setStyle("bold")
        x_axis_name.setTextColor("gray")
        x_axis_name.draw(self.win)
        
        # loops through hour category to get the values
        for label, values in self.traffic_data.items():
            x_start = margin + int(label) * category_spacing # calculate the starting x-coordinate for the bars
            bar1_x1 = x_start                                #left x-coordinate of the first bar
            bar1_x2 = bar1_x1 + bar_width                    #right x-coordinate of the first bar
            bar2_x1 = bar1_x2                                #left x-coordinate of the second bar
            bar2_x2 = bar2_x1 + bar_width                    #right x-coordinate of the second bar
            
            # calculating the heights of the bars
            bar1_height = (values[0] / max_value) * max_height
            bar2_height = (values[1] / max_value) * max_height
            y_base = window_height - margin #base y-coordinate for the bars
            
            # first bar
            bar1 = Rectangle(Point(bar1_x1, y_base - bar1_height), Point(bar1_x2, y_base))
            bar1.setFill("lightgreen")
            bar1.setOutline("gray")
            bar1.draw(self.win)
            
            # second bar
            bar2 = Rectangle(Point(bar2_x1, y_base - bar2_height), Point(bar2_x2, y_base))
            bar2.setFill("lightcoral")
            bar2.setOutline("gray")
            bar2.draw(self.win)
            
            # text displaying the value of the first bars
            bar1_text = Text(Point(bar1_x1 + bar_width / 2, y_base - bar1_height - 10), str(values[0]))
            bar1_text.setSize(10)
            bar1_text.setStyle("bold")
            bar1_text.setTextColor("black")
            bar1_text.draw(self.win)
            
            # text displaying the value of the second bars
            bar2_text = Text(Point(bar2_x1 + bar_width / 2, y_base - bar2_height - 10), str(values[1]))
            bar2_text.setSize(10)
            bar2_text.setStyle("bold")
            bar2_text.setTextColor("black")
            bar2_text.draw(self.win)
            
            # label for the hour (below the bars)
            label_text = Text(Point((bar1_x1 + bar2_x2) / 2, y_base + 15), label)
            label_text.setSize(10)
            label_text.setStyle("bold")
            label_text.draw(self.win)

            info_text = Text(
                Point(window_width / 2, window_height - (margin / 2)+ 35),
                 "Hour with least vehicles in Hanley Highway/Westway: :00 ( vehicles)"
            )
            info_text.setSize(12)
            info_text.setStyle("bold")
            info_text.setTextColor("blue")
            info_text.draw(self.win)

    def add_legend(self):
        """
        Adds a legend to the histogram to indicate which bar corresponds to which junction.
        """
        margin = 100
        
        # legend box for Elm Avenue/Rabbit road
        elm_legend_box = Rectangle(Point(margin, margin + (margin / 2)), Point(margin + 20, margin + (margin / 2) + 20))
        elm_legend_box.setFill("lightgreen")
        elm_legend_box.setOutline("gray")
        elm_legend_box.draw(self.win)
        
        # text for Elm Avenue/Rabbit road
        elm_legend = Text(Point(margin + 120, margin + (margin / 2) + 10), "Elm Avenue/Rabbit Road")
        elm_legend.setSize(12)
        elm_legend.setTextColor("black")
        elm_legend.draw(self.win)
        
        # legend box for for Hanley highway/Westway
        hanley_legend_box = Rectangle(Point(margin, margin + (margin / 2) + 30), Point(margin + 20, margin + (margin / 2) + 50))
        hanley_legend_box.setFill("lightcoral")
        hanley_legend_box.setOutline("gray")
        hanley_legend_box.draw(self.win)
        
        # text for Hanley highway/Westway
        hanley_legend = Text(Point(margin + 122, margin + (margin / 2) + 40), "Hanley Highway/Westway")
        hanley_legend.setSize(12)
        hanley_legend.setTextColor("black")
        hanley_legend.draw(self.win)

    def run(self):
        """
        Runs the Tkinter main loop to display the histogram.
        """
        self.setup_window()    # sets up the window
        self.draw_histogram()  # draws the histogram
        self.add_legend()      # Adds the legend to the window
        
        try:
            # Waits for a mouse click to close the window if it's still open
            self.win.getMouse()
        except GraphicsError:
            pass
        finally:
            # closes the graphical window safely
            self.win.close()


# Task E: Code Loops to Handle Multiple CSV Files
class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.
        """
        self.current_data = None

    def load_csv_file(self, file_path):
        """
        Loads a CSV file and processes its data.
        """
        try:
            with open(file_path, "r") as file:
                reader = csv.DictReader(file) # reads the CSV file as a dictionary
                self.current_data = list(reader) # converts the data into a list of dictionaries
                hourly_count = {} # dictionary to store hourly counts of each junction
                for row in self.current_data:
                    hour = int(row["timeOfDay"].split(":")[0])  # extracts the hour from the time
                    junction = row["JunctionName"].lower().strip() 

                    if hour not in hourly_count:
                        hourly_count[hour] = [0, 0] #initializing counts for both junctions
                    
                    #increment counts based on the name
                    if junction == "elm avenue/rabbit road":
                        hourly_count[hour][0] += 1
                    elif junction == "hanley highway/westway":
                        hourly_count[hour][1] += 1
                return hourly_count
        except FileNotFoundError:
            return None 

    def clear_previous_data(self):
        """
        Clears data from the previous run to process a new dataset.
        """
        self.current_data = None # reset the current data
        
    def handle_user_interaction(self):
        """
        Handles user input for processing multiple files.
        """
        while True:
            choice = input("Do you want to select another data file for a different date? (Y/N): ").strip().upper()
            if choice == "Y":
                self.clear_previous_data()
                return True
            elif choice == "N":
                return False
            print("Invalid input. Please enter 'Y' or 'N'.")

    def process_files(self):
        """
        Main loop for handling multiple CSV files until the user decides to quit.
        """
        while True:
            # gets the input from the user
            day, month, year = validate_date_input()
            date = f"{day:02d}/{month:02d}/{year}" # formats the date
            filename = f"traffic_data{day:02d}{month:02d}{year}.csv" # constructs the file name
            processed_data = process_csv_data(filename) # processes the data
            
            if processed_data:
                print(f"data file selected is {filename}") # displays the file name
                display_outcomes(processed_data) # Display calculated outcomes
                save_results_to_file(processed_data, filename, file_name="results.txt") # saves results to a file
                
                traffic_data = self.load_csv_file(filename) # loads traffic data for the selected file
                app = HistogramApp(traffic_data, date)  # creates a histogram
                app.run() # runs application to display the histogram
                
            if not self.handle_user_interaction(): # if user dosen't want to continue
                print("End of run")
                break       

#Main
MultiCSVProcessor().process_files()
