import customtkinter as ctk
from settings import *
import mysql.connector
from datetime import datetime, timedelta
import tkinter as tk

db = mysql.connector.connect(
    host = "34.116.155.148",
    user = "root",
    passwd = "root",
    database = "hotel"
)
mycursor = db.cursor()

class App(ctk.CTk):

    def __init__(self):

        super().__init__(fg_color = BLUE)
        self.title("HospITality")
        self.geometry("1024x576")
        self.minsize(800,450)

        self.columnconfigure(0, weight = 1, uniform = "a")
        self.columnconfigure(1, weight = 3, uniform = "a")
        self.rowconfigure(0, weight = 1, uniform = "a")
        self.rowconfigure(1, weight = 9, uniform = "a")


        self.my_title = ctk.CTkLabel(self, text = "HospITality")
        self.my_title.grid(row = 0, column = 1, sticky = "nsew")

        self.dialog_box = Dialog(self)
        self.all_rooms = AllRooms(self)

        self.arrival_date = self.dialog_box.arrival_dater.date_value
        self.departure_date = self.dialog_box.departure_dater.date_value
        self.capacity_value = self.dialog_box.capacitier.value

        self.check_button = ctk.CTkButton(self, text = "check", command = self.checker)
        self.check_button.grid(row = 0, column = 0, sticky = "nsew")

        self.mainloop()

    def checker(self):
        # Define the room and date range
        for i, room in enumerate(self.all_rooms.rooms):
            print(i)
            room_id = room[0]  # Replace with the desired room ID
            start_date = self.arrival_date.get() # Replace with the desired start date
            print(f"start my desired value = {start_date}")
            end_date = self.departure_date.get() # Replace with the desired end date
            print(f"end my desired value = {end_date}")
            num_people = self.capacity_value.get()  # Replace with the desired number of people
            print(f"my desired value = {num_people}")
            # Prepare the SQL query to check room occupancy and capacity
            query = "SELECT * FROM guests WHERE room_id = %s AND check_out_date >= %s AND check_in_date <= %s"
            data = (room_id, start_date, end_date)

            # Execute the query
            mycursor.execute(query, data)

            # Fetch the result
            occupancy = mycursor.fetchall()

            # Check if the room is occupied within the date range and if it can fit the specified number of people
            if occupancy:
                self.all_rooms.room_boxes[i].configure(fg_color = "#ff88bb")
                print("The room is occupied within the specified date range.")
            else:
                # Query the 'rooms' table to check the room capacity
                capacity_query = "SELECT capacity FROM rooms WHERE room_id = %s"
                capacity_data = (room_id,)
                mycursor.execute(capacity_query, capacity_data)
                room_capacity = mycursor.fetchone()

                if room_capacity and room_capacity[0] >= num_people:
                    self.all_rooms.room_boxes[i].configure(fg_color = "#88ffbb")
                    print("The room is available and can fit the specified number of people.")
                else:
                    print("The room is either occupied or cannot fit the specified number of people.")
                    self.all_rooms.room_boxes[i].configure(fg_color = "#ffbb88")


    

class Dialog(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent)
        self.rowconfigure((0,1,2,3,4,5,6,7), weight = 1, uniform = "a")
        self.columnconfigure(0, weight = 1, uniform = "a")
        self.fg_color = "#3344ff"
        self.configure(fg_color = self.fg_color)
        self.grid(column = 0, row = 1, sticky = "nsew")

        self.arrival_date_manager = DateManager()
        self.arrival_dater = Dater(self, self.arrival_date_manager, row=0, text = "Arrival")

        self.departure_date_manager = DateManager()
        self.departure_dater = Dater(self, self.departure_date_manager, row=2, text ="Departure")

        self.capacitier = Capacitier(self, 6, "Liczba osób")

class Capacitier(ctk.CTkFrame):
    def __init__(self, parent, row, text):
        super().__init__(master = parent)
        self.rowconfigure((0, 1), weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=3, uniform="a")
        self.columnconfigure(2, weight=1, uniform="a")
        self.grid(column=0, row=row, sticky="nsew")

        self.value = tk.IntVar(self)  # Initialize the value to 0
        self.label = ctk.CTkLabel(self, text = text)
        self.label.grid(column = 0, row = 0, columnspan = 3, sticky = "nsew")

        self.capacity_variable = tk.StringVar(self)

        self.value_label = ctk.CTkLabel(self, text = text)
        self.value_label.configure(text=f"Value: {self.value}", textvariable = self.value)
        self.value_label.grid(column = 1, row = 1, sticky = "nsew")
        increment_button = ctk.CTkButton(self, text=">", command=self.increment)
        increment_button.grid(column = 2, row = 1, sticky = "nsew")

        decrement_button = ctk.CTkButton(self, text="<", command=self.decrement)
        decrement_button.grid(column = 0, row = 1, sticky = "nsew")

    def increment(self):
        if self.value.get() < 6:
            self.value.set(self.value.get() + 1)
            self.value_label.configure(text=f"Value: {self.value.get()}", textvariable = self.value)

    def decrement(self):
        if self.value.get() > 0:
            self.value.set(self.value.get() - 1)
            self.value_label.configure(text=f"Value: {self.value.get()}", textvariable = self.value)
        
class Dater(ctk.CTkFrame):
    def __init__(self, parent, date_manager, row, text):
        super().__init__(master=parent)
        self.rowconfigure((0, 1), weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=3, uniform="a")
        self.columnconfigure(2, weight=1, uniform="a")
        self.grid(column=0, row=row, sticky="nsew")

        self.date_value = tk.StringVar(self)

        self.arrival_label = ctk.CTkLabel(self, text = text)
        self.arrival_label.grid(column = 0, row = 0, columnspan = 3, sticky = "nsew")

        self.date_manager = date_manager
        self.date_label = DateLabel(self, self.date_manager, textvariable = self.date_value)
        self.increment_button = DateButton(self, self.date_manager, self.date_value, increment=True)
        self.decrement_button = DateButton(self, self.date_manager, self.date_value, increment=False)

        self.date_label.grid(column=1, row=1, sticky="nsew")
        self.increment_button.grid(column=2, row=1, sticky="nsew")
        self.decrement_button.grid(column=0, row=1, sticky="nsew")
        self.date_manager.set_label(self.date_label)

class DateLabel(ctk.CTkLabel):
    def __init__(self, parent, date_manager, textvariable):
        super().__init__(parent)
        self.date_manager = date_manager
        self.configure(text=self.date_manager.get_date())
        self.textvariable = textvariable

    def update_date(self):
        self.configure(text=self.date_manager.get_date(), textvariable = self.textvariable)

class DateButton(ctk.CTkButton):
    def __init__(self, parent, date_manager, textvariable, increment=True):
        text = ">" if increment else "<"
        super().__init__(parent, text=text, command=self.update_date)
        self.textvariable = textvariable
        self.date_manager = date_manager
        self.increment = increment


    def update_date(self):
        if self.increment:
            self.date_manager.increment_date()
            self.textvariable.set(self.date_manager.get_date())
        else:
            self.date_manager.decrement_date()
            self.textvariable.set(self.date_manager.get_date())
        self.date_manager.update_label()

class DateManager:
    def __init__(self):
        self.current_date = datetime.now()
        self.date_label = None

    def set_label(self, date_label):
        self.date_label = date_label

    def increment_date(self):
        self.current_date += timedelta(days=1)

    def decrement_date(self):
        self.current_date -= timedelta(days=1)

    def get_date(self):
        return self.current_date.strftime("%Y-%m-%d")

    def update_label(self):
        if self.date_label:
            self.date_label.update_date()

# Execute the SELECT query to retrieve the rooms
query = "SELECT * FROM rooms"
mycursor.execute(query)

# Fetch all the rows from the result
rooms = mycursor.fetchall()

# Create a list to store the room numbers
room_numbers = []

# Iterate through the rows and extract the room numbers
for room in rooms:
    room_id, room_number, capacity = room
    room_numbers.append(room_number)

# print(rooms)
# wstepne_pokoje = [[0,1,5, True],
#                   [1,2,3, False],
#                   [2,3,2, True],
#                   [3,4,3, True],
#                   [4,5,5, False],
#                   [5,6,2, True],
#                   [6,7,2, True],
#                   [7,8,6, False],
#                   [8,9,2, True],
#                   [9,10,5, False],]

class AllRooms(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent)
        self.columnconfigure((0,1,2,3,4), weight = 1, uniform = "a")
        self.rowconfigure((0,1), weight = 1, uniform = "a")
        self.fg_color = "#ffbb88"
        self.configure(fg_color = self.fg_color)
        self.grid(column = 1, row = 1, sticky = "nsew")

        self.rooms = []
        self.room_boxes = []
        for i, room in enumerate(rooms):
            self.rooms.append(room)
            self.room_boxes.append(RoomBox(self, room[1], room[2]))
        
        loop_counts = [5,2] #columns and rows at [0] and [1]
        for i in range(loop_counts[0]):
            for j in range(loop_counts[1]):
                current_iterations = (j * loop_counts[0]) + i
                self.room_boxes[current_iterations].grid(column = i, row = j, sticky = "nsew")

class RoomBox(ctk.CTkFrame):
    def __init__(self, parent, room_number, room_capacity, is_avaiable = True):
        super().__init__(master = parent)
        self.is_avaiable = is_avaiable
        self.__display_availability_color()
        self.rowconfigure((0,1,2,3), weight = 1, uniform = "a")
        self.columnconfigure((0,1,2,3), weight = 1, uniform = "a")
        self.room_number = room_number
        self.room_capacity = room_capacity

        self.room_label = ctk.CTkLabel(self, text = f"Room number: {room_number}", text_color = "#333333")
        self.room_capacity = ctk.CTkLabel(self, text = f"Room capacity: {room_capacity}", text_color = "#333333")
        self.room_label.grid(row = 0, column = 0, columnspan = 4, rowspan = 2, sticky="nsew")
        self.room_capacity.grid(row = 2, column = 0, columnspan = 4, rowspan = 2, sticky="nsew")


    def __display_availability_color(self):
        if self.is_avaiable:
            self.configure(fg_color = "#88ffbb")
        else:
            self.configure(fg_color = "#ffbb88")

if __name__ == "__main__":
    App()