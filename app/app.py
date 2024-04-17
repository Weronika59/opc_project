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
        n_estim = st.slider("Number of trees", min_value=10, step=10, max_value=2000)
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

    