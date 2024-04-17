from fastapi import FastAPI
import pandas as pd
import numpy as np
import mysql.connector
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

# Database connection configuration
db_config = {
    'host': 'db',
    'user': 'my_user',
    'password': 'my_password',
    'database': 'my_database'
}

# Function to fetch data from the database
def get_data():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute('USE my_database')
        cursor.execute('SELECT * FROM dane_satisfaction;')
 
        data = cursor.fetchall()
        colnames = [column[0] for column in cursor.description]
 
        return {'data': data,
        'colnames': colnames}
 
    except mysql.connector.Error as error:
        return f"Error: {error}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    
# Function to prepare data for model training
def data_prep():
    data = get_data()
    
    dane = data['data']
    colnames = data['colnames']
    
    dane = pd.DataFrame(dane, columns = colnames)
        
    #character variables to categorical
    dane.Gender = dane.Gender.eq('Male').astype(int)

    dane['Customer_Type'] = dane['Customer_Type'].eq('Loyal Customer').astype(int)

    dane['Type_of_Travel'] = dane['Type_of_Travel'].eq('Personal Travel').astype(int)

    class_mapping = {'Eco': 0, 'Eco Plus': 1, 'Business': 2}
    dane['Class'] = dane['Class'].map(class_mapping)

    #bd
    #median for numeric variables
    dane['Age'] = dane['Age'].fillna(dane['Age'].median())
    dane['Flight_Distance'] = dane['Flight_Distance'].fillna(dane['Flight_Distance'].median())
    dane['Departure_Delay_in_Minutes'] = dane['Departure_Delay_in_Minutes'].fillna(dane['Departure_Delay_in_Minutes'].median())
    dane['Arrival_Delay_in_Minutes'] = dane['Arrival_Delay_in_Minutes'].fillna(dane['Arrival_Delay_in_Minutes'].median())

    #mode for categorical variables
    dane['Gender'] = dane['Gender'].fillna(0)
    dane['Customer_Type'] = dane['Customer_Type'].fillna(1)
    dane['Type_of_Travel'] = dane['Type_of_Travel'].fillna(0)
    dane['Class'] = dane['Class'].fillna(2)
    dane['Inflight_wifi_service'] = dane['Inflight_wifi_service'].fillna(3)
    dane['Departure_Arrival_time_convenient'] = dane['Departure_Arrival_time_convenient'].fillna(4)
    dane['Ease_of_Online_booking'] = dane['Ease_of_Online_booking'].fillna(3)
    dane['Gate_location'] = dane['Gate_location'].fillna(3)
    dane['Food_and_drink'] = dane['Food_and_drink'].fillna(4)
    dane['Online_boarding'] = dane['Online_boarding'].fillna(4)
    dane['Seat_comfort'] = dane['Seat_comfort'].fillna(4)
    dane['Inflight_entertainment'] = dane['Inflight_entertainment'].fillna(4)
    dane['On_board_service'] = dane['On_board_service'].fillna(4)
    dane['Leg_room_service'] = dane['Leg_room_service'].fillna(4)
    dane['Baggage_handling'] = dane['Baggage_handling'].fillna(4)
    dane['Checkin_service'] = dane['Checkin_service'].fillna(4)
    dane['Inflight_service'] = dane['Inflight_service'].fillna(4)
    dane['Cleanliness'] = dane['Cleanliness'].fillna(4)

    X = dane.loc[:, dane.columns != 'satisfaction']
    y = dane['satisfaction']
    y = LabelEncoder().fit_transform(y) 

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    scaler = MinMaxScaler()
    scaler.fit(X_train)
    
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    
    return {'X_train': np.array(X_train).tolist(), 
        'X_test': np.array(X_test).tolist(), 
        'y_train': np.array(y_train).tolist(), 
        'y_test': np.array(y_test).tolist()}


app = FastAPI()
# Fetch prepared data
@app.get("/preprocess_data/")
def get():
    x = data_prep()
    return {'data':x}

# Fetch raw data
@app.get("/raw_data/")
def raw_data():
    data = get_data()
    dane = data['data']
    colnames = data['colnames']
    return {'raw_data': dane,
            'colnames': colnames}
