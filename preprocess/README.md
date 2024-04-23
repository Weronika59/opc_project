### Preprocess Microservice

This microservice handles the management of data used by the system. Here data is fetching from the Database Microservice and preparing for model training. It provides APIs for storing, retrieving and updating data.

There are two endpoints for getting raw data (used later for data preview in UI microservice) and getting preprocessed data (user later for model training).