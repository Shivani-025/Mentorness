
import sqlite3
import pandas as pd

# Load the dataset
file_path = 'Hotel Reservation Dataset.csv'
hotel_data = pd.read_csv(file_path)

# Connect to a SQLite database (or create one if it doesn't exist)
conn = sqlite3.connect('hotel_reservations.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE hotel_reservations (
    Booking_ID TEXT,
    no_of_adults INTEGER,
    no_of_children INTEGER,
    no_of_weekend_nights INTEGER,
    no_of_week_nights INTEGER,
    type_of_meal_plan TEXT,
    room_type_reserved TEXT,
    lead_time INTEGER,
    arrival_date TEXT,
    market_segment_type TEXT,
    avg_price_per_room REAL,
    booking_status TEXT
)
''')

# Insert data into the table
hotel_data.to_sql('hotel_reservations', conn, if_exists='append', index=False)

# Queries
queries = {
    "total_reservations": "SELECT COUNT(*) AS total_reservations FROM hotel_reservations;",
    "most_popular_meal_plan": "SELECT type_of_meal_plan, COUNT(*) AS count FROM hotel_reservations GROUP BY type_of_meal_plan ORDER BY count DESC LIMIT 1;",
    "average_price_with_children": "SELECT AVG(avg_price_per_room) AS avg_price FROM hotel_reservations WHERE no_of_children > 0;",
    "reservations_in_year_20XX": "SELECT COUNT(*) AS reservations_in_year FROM hotel_reservations WHERE strftime('%Y', arrival_date) = '20XX';",
    "most_common_room_type": "SELECT room_type_reserved, COUNT(*) AS count FROM hotel_reservations GROUP BY room_type_reserved ORDER BY count DESC LIMIT 1;",
    "weekend_reservations": "SELECT COUNT(*) AS weekend_reservations FROM hotel_reservations WHERE no_of_weekend_nights > 0;",
    "highest_and_lowest_lead_time": "SELECT MAX(lead_time) AS highest_lead_time, MIN(lead_time) AS lowest_lead_time FROM hotel_reservations;",
    "most_common_market_segment": "SELECT market_segment_type, COUNT(*) AS count FROM hotel_reservations GROUP BY market_segment_type ORDER BY count DESC LIMIT 1;",
    "confirmed_reservations": "SELECT COUNT(*) AS confirmed_reservations FROM hotel_reservations WHERE booking_status = 'Confirmed';",
    "total_adults_and_children": "SELECT SUM(no_of_adults) AS total_adults, SUM(no_of_children) AS total_children FROM hotel_reservations;",
    "avg_weekend_nights_with_children": "SELECT AVG(no_of_weekend_nights) AS avg_weekend_nights FROM hotel_reservations WHERE no_of_children > 0;",
    "reservations_per_month": "SELECT strftime('%m', arrival_date) AS month, COUNT(*) AS reservations FROM hotel_reservations GROUP BY month;",
    "avg_nights_per_room_type": "SELECT room_type_reserved, AVG(no_of_weekend_nights + no_of_week_nights) AS avg_nights FROM hotel_reservations GROUP BY room_type_reserved;",
    "most_common_room_type_with_children": "SELECT room_type_reserved, COUNT(*) AS count, AVG(avg_price_per_room) AS avg_price FROM hotel_reservations WHERE no_of_children > 0 GROUP BY room_type_reserved ORDER BY count DESC LIMIT 1;",
    "highest_avg_price_per_market_segment": "SELECT market_segment_type, AVG(avg_price_per_room) AS avg_price FROM hotel_reservations GROUP BY market_segment_type ORDER BY avg_price DESC LIMIT 1;"
}

# Execute queries and collect results
results = {}
for query_name, query in queries.items():
    cursor.execute(query.replace('20XX', '2018'))  # Replace 20XX with 2018 for the example
    results[query_name] = cursor.fetchall()

# Print results
for query_name, result in results.items():
    print(f"{query_name}: {result}")

# Close connection
conn.close()
