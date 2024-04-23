CREATE DATABASE IF NOT EXISTS my_database;

USE my_database;

CREATE TABLE dane_satisfaction (
id INT AUTO_INCREMENT PRIMARY KEY,
Gender VARCHAR(10),
Customer_Type VARCHAR(50),
Age INT,
Type_of_Travel VARCHAR(50),
Class VARCHAR(50),
Flight_Distance INT,
Inflight_wifi_service INT,
Departure_Arrival_time_convenient INT,
Ease_of_Online_booking INT,
Gate_location INT,
Food_and_drink INT,
Online_boarding INT,
Seat_comfort INT,
Inflight_entertainment INT,
On_board_service INT,
Leg_room_service INT,
Baggage_handling INT,
Checkin_service INT,
Inflight_service INT,
Cleanliness INT,
Departure_Delay_in_Minutes INT,
Arrival_Delay_in_Minutes INT,
satisfaction VARCHAR(50)
);

LOAD DATA LOCAL INFILE 'dane_satisfaction2.csv'
INTO TABLE dane_satisfaction
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES; -- Ignore the header row
