### Train Microservice

This microservice is responsible for training machine learning model and making prediction based on the input data provided by user through the UI application. Here prepared data is getting from the preprocess microservice. Also there is being build `initial_train()` function for building model without hyperparameters. When the user enters model hyperparameters, the model (with them) is being build and trained by `train_model()` function. Then, model is evaluating using the `eval_model()` function.

There are five endpoints - two for posting trained model and predicion, and three for getting preprocessed data, getting model hyperparameters and model evaluation.
