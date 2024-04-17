import logging
import requests             
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from fastapi import FastAPI
from typing import Dict, Any
from sklearn.metrics import auc
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import roc_curve

# Function for getting preprocessed data from 'preprocess'
def get_preprocess_data():
    response = requests.get('http://preprocess:5000/preprocess_data/')    
    data = response.json()['data']
    return data
    
# Defining model with hyperparameters
def train_model(X_train, y_train, **hyperparameters):
    forest = RandomForestClassifier(**hyperparameters)
    forest.fit(X_train, y_train)
    return forest

# Defining model without hyperparameters
def initial_train():
    x = get_preprocess_data()
    X_train = x['X_train']
    y_train = x['y_train']
    
    forest = RandomForestClassifier()
    forest.fit(X_train, y_train)
    
    return forest   
 
# Function for evaluating model
def eval_model():    
    global MODEL

    data = get_preprocess_data()
    
    X_test = np.array(data['X_test'])
    X_train = np.array(data['X_train'])
    y_train = np.array(data['y_train'])
    y_test = np.array(data['y_test'])

    y_scores = MODEL.predict_proba(X_test)[:, 0]
    y_pred = MODEL.predict(X_test)

    train_score = MODEL.score(X_train, y_train)
    test_score = MODEL.score(X_test, y_test)
    precision = precision_score(y_true=y_test, y_pred=y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    confusion = confusion_matrix(y_true=y_test, y_pred=y_pred)
    fpr, tpr, _ = roc_curve(y_test, y_scores)
    roc_auc = auc(tpr, fpr)

    return {'train_score': train_score,
            'test_score': test_score,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'confusion': confusion.tolist(), 
            'fpr': fpr.tolist(),
            'tpr': tpr.tolist(),
            'roc_auc': roc_auc
            }


MODEL = initial_train()
    

app = FastAPI()
# Model training
@app.post("/train/")
def train_model2(hyperparameters: Dict[str, Any]):
    data = get_preprocess_data()

    try: 
        global MODEL
        X_train, y_train = data['X_train'], data['y_train']
        MODEL = train_model(X_train=X_train, y_train= y_train, **hyperparameters)
        status = 'success'
    except Exception as e:
        logging.error(str(e))
        status = 'failed'
        
    return {'status': status}

# Getting model hyperparameters
@app.get('/get_model_params/')
async def return_params():
    return {'model_params': MODEL.get_params()}

# Evaluating model
@app.get('/eval_model/')
def evaluate_model():
    metrics = eval_model()
    return {'metrics': metrics}

# Fetch preprocessed data
@app.get('/get_dataset/')
async def get_dataset():
    data = get_preprocess_data()
    return {'dataset': data}
