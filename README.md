# Application for predicting airline customer satisfaction

This is a simple distributed application running across multiple Docker containers prepared for for the credit of the course Organizacja procesów obliczeniowych.

### Getting started

To run this app you need Docker Desktop application. 

This solution uses Python for User Interfase, microservices and FastApi for storing, retrieving and updating data.

Copy this repository to a folder of your choice and run this command in a command prompt to build and run the app:

`docker compose build & docker compose up`

The app will be running at http://localhost:5005.

### About the application

The application allows you to preview the data (main panel), configure the random forest model (sidebar) and train the model ("Train model" button).

After pressing this button, the main panel will display the metrics of the built model and its assessment of the fit to the test set. The classification matrix and ROC curve will also be drawn.*

*Also, arm yourself with patience, because the data is quite large (more than 100 thousand rows) :)

### Architecture


![](C:\Users\wnadw\Desktop\schemat.png "architecture")

*database* container is responsible for storing data.

*preprocess* is responsible for preparing the data for training the model in the next container.

*train* is responsible for building Random Forest model with the given hyperparameters and evaluating it on test data.

*app* is a front-end web application in Python with streamlit interface for training and evaluating model.


