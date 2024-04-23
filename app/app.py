import requests
from utils import *
import streamlit as st 


def train_model_request():
    response = requests.post('http://train:5001/train/', json = {'n_estimators': int(n_estim),
                                                                'max_depth': int(max_depth), 
                                                                'min_samples_split': int(min_split), 
                                                                'min_samples_leaf': int(min_leaf), 
                                                                'criterion': str(criterion)})
    status = response.json()['status']
    return status

def pred_model_request():
    response = requests.post('http://train:5001/predict/', json = pred_dane)
    y_pred = response.json()['y_pred']
    return y_pred


# Title of the application
st.title('Predicting airline customer satisfaction')

# Data preview
with st.expander("Data preview"):
    response = requests.get('http://preprocess:5000/raw_data/')
    data = response.json()['raw_data']
    colnames = response.json()['colnames']
    df = pd.DataFrame(data=data, columns=colnames)
    st.dataframe(df.head(10))

# Configuration model hyperparameters
with st.sidebar.form(key="hyperparameters_form"):
    st.header("Configuration of Random Forest model")

    criterion = st.selectbox("Criterion",["gini", "entropy", "log_loss"])

    c1,c2 = st.columns(2)
    with c1:
        n_estim = st.slider("Number of trees", min_value=10, step=10, max_value=1000)
    with c2:
        max_depth = st.slider("Max depth", min_value=1, step=1, max_value=40)
    c1,c2 = st.columns(2)
    with c1:
        min_split = st.slider("Min samples split", min_value=2, step=1, max_value=10)
    with c2:
        min_leaf = st.slider("Min samples leaf", min_value=1, step=1, max_value=10)

    submit_button = st.form_submit_button("Train model", type="primary")


# Model traning and evaluation
if submit_button:
    status = train_model_request()
    
    if status == 'success':
        st.success('A model was trained with the given hyperparameters')
        metrics = requests.get('http://train:5001/eval_model/').json()['metrics']

        c1,c2 = st.columns(2)

        c1.metric(label="Training Score", value=round(metrics['train_score']))

        with c2:
            st.metric(
                label="Test Score",
                value=round(metrics['test_score'], 3)
            )

        c1,c2,c3 = st.columns(3)

        with c1:
            st.metric(label="Precision", value=round(metrics['precision'], 3))
        with c2:
            st.metric(label="Recall", value=round(metrics['recall'], 3))
        with c3:
            st.metric(label="F1", value=round(metrics['f1'], 3))


        c1, c2 = st.columns(2)
        with c1:
            st.altair_chart(produce_confusion(metrics['confusion']), use_container_width=True)
        with c2:
            st.altair_chart(produce_roc(metrics['fpr'], metrics['tpr'], metrics['roc_auc']), use_container_width=True)

    else:
        st.error('Failure to train a model')

# Model prediction
with st.expander("Data predicion"):
    form = st.form(key='my_form')
    gender = form.selectbox("Gender", options=['Male', 'Female'])
    cust_type = form.selectbox("Customer Type", options=['Loyal Customer', 'disloyal Customer'])
    age = form.number_input("Age", min_value=1)
    type_of_tr = form.selectbox("Type of travel", options=['Personal Travel', 'Business travel'])
    clas = form.selectbox("Class", options=['Business', 'Eco', 'Eco Plus'])
    fl_dist = form.number_input("Flight Distance", min_value=1)
    wifi = form.selectbox("Inflight wifi service", [1,2,3,4,5])
    depart = form.selectbox("Departure arrival time convenient", options=[1,2,3,4,5])
    online = form.selectbox("Ease of online booking", options=[1,2,3,4,5])
    gate = form.selectbox("Gate location", options=[1,2,3,4,5])
    food = form.selectbox("Food and drink", options=[1,2,3,4,5])
    boarding = form.selectbox("Online boarding", options=[1,2,3,4,5])
    seat = form.selectbox("Seat comfort", options=[1,2,3,4,5])
    entertainment = form.selectbox("Inflight entertainment", options=[1,2,3,4,5])
    on_board = form.selectbox("On board service", options=[1,2,3,4,5])
    leg = form.selectbox("Leg room service", options=[1,2,3,4,5])
    baggage = form.selectbox("Baggage handling", options=[1,2,3,4,5])
    checkin = form.selectbox("Checkin service", options=[1,2,3,4,5])
    service = form.selectbox("Inflight service", options=[1,2,3,4,5])
    clean = form.selectbox("Cleanliness", options=[1,2,3,4,5])
    dep_delay = form.number_input("Departure delay in minutes", min_value=0)
    arr_del = form.number_input("Arrival delay in minutes", min_value=0)

    st.write('Press predict to have your prediction printed below')
        
    pred_dane = {'gender': gender,
                    'cust_type': cust_type,
                    'age': age,
                    'type_of_tr': type_of_tr,
                    'clas': clas,
                    'fl_dist': fl_dist,
                    'wifi': wifi,
                    'depart': depart,
                    'online': online,
                    'gate': gate,
                    'food': food,
                    'boarding': boarding,
                    'seat': seat,
                    'entertainment': entertainment,
                    'on_board': on_board,
                    'leg': leg,
                    'baggage': baggage,
                    'checkin': checkin,
                    'service': service,
                    'clean': clean,
                    'dep_delay': dep_delay,
                    'arr_delay': arr_del}

    submit_button2 = form.form_submit_button('Predict')

    if submit_button2:
        try:
            y_pred = pred_model_request()
            st.write(f'Predicted satisfaction: {y_pred}')
        except Exception as e:
            st.error('Failure to predict a model')

