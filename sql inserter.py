import mysql.connector
import random

# Establish a connection to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="hotel"
)

names1 = ["John", "Jan", "Monika", "Patryk", "Karol"]
names2 = ["Mesa", "Border", "Kalino", "Bossowski", "Essowski"]

mycursor = db.cursor()

# Insert guests
for i in range(10):
    guest_id = i + 1  # Generate a unique guest ID
    room_id = i  # Replace with the actual room ID
    first_name = random.choice(names1)
    last_name = random.choice(names2)
    lower_random = random.randint(1, 10)
    upper_random = random.randint(lower_random, 20)
    check_in_date = f"2023-07-{lower_random}"
    check_out_date = f"2023-07-{upper_random}"
    insert_query = "INSERT INTO guests (guest_id, room_id, first_name, last_name, check_in_date, check_out_date) VALUES (%s, %s, %s, %s, %s, %s)"

    data = (guest_id, room_id, first_name, last_name, check_in_date, check_out_date)
    mycursor.execute(insert_query, data)

db.commit()

# Close the cursor and the database connection
mycursor.close()
db.close()

