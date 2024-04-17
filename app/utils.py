import altair as alt
import numpy as np
import pandas as pd

# Function for drawing confusion matrix
def produce_confusion(cm):
    data = pd.DataFrame(
        {
            "Actual": np.array(["Positive", "Negative", "Positive", "Negative"]),
            "Predicted": np.array(["Positive", "Negative", "Negative", "Positive"]),
            "Count": np.array([cm[0][0], cm[1][1], cm[1][0], cm[0][1]]),

            "Color": np.array(
                ["#66BB6A", "#66BB6A", "#EF5350", "#EF5350"]
            ), 
        }
    )

    heatmap = (
        alt.Chart(data)
        .mark_rect()
        .encode(
            x="Actual:N",
            y="Predicted:N",
            color=alt.Color("Color:N", scale=None, legend=None),
            tooltip=["Actual:N", "Predicted:N", "Count:Q"],
        )
        .properties(title="Confusion Matrix", width=300, height=350)
    )

    text = (
        alt.Chart(data)
        .mark_text(fontSize=16, fontWeight="bold")
        .encode(
            x="Actual:N",
            y="Predicted:N",
            text="Count:Q",
            color=alt.condition(
                alt.datum.Color == "#EF5350", alt.value("white"), alt.value("black")
            ),
        )
    )

    chart = (heatmap + text).configure_title(
        fontSize=18, fontWeight="bold", anchor="middle"
    )

    return chart


# Function for drawing ROC curve
def produce_roc(fpr, tpr, roc_auc):
    roc_data = pd.DataFrame({"False Positive Rate": tpr, "True Positive Rate": fpr})
    roc_chart = (
        alt.Chart(roc_data)
        .mark_line()
        .encode(
            x=alt.X("False Positive Rate", title="False Positive Rate (FPR)"),
            y=alt.Y("True Positive Rate", title="True Positive Rate (TPR)"),
        )
        .properties(title=f"ROC Curve (AUC = {roc_auc:.2f})")
    )
    return roc_chart
