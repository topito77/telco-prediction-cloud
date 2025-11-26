# we are using the following libraries
import requests
import streamlit as st

DEV_API = "http://127.0.0.1:8000/predict"
PROD_API = "https://predictingforjay.azurewebsit..."

# fetches status of the response and returns something...
def fetch_prediction(payload: dict) -> dict:
    """Call the prediction API and return the JSON response"""
    response = requests.post(DEV_API, json=payload, timeout=5)
    response.raise_for_status()
    return response.json() 

# second helper function... not sure what either are doing
def fetch_prediction_from_production(params: dict) -> dict:
    """Call the production API and return the response.

    Our serverless function doesnt support JSON in or out
    Plus we need to increase the timeout for cold starts.
    """
    url = PROD_API + "&" + "&".join(f"{k}={v}" for k, v in params.items())
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    return response

### Streamlit Dashboard for Telco Churn Prediction
# when using streamlit you are usually using st.whatever to call streamlit functions

st.set_page_config(page_title="Telco Churn Predictor", page_icon="📊")


st.title("Telco Churn Prediction")
st.write("Enter customer details and get a churn prediction.")

# create two columns, first one on the left, second on the right
left, right = st.columns(2)

# you can get user input using streamlit widgets like select box
tenure = left.selectbox("Tenure (mths)", options=list(range(0, 121)))

# these are the values the user can select from
monthly = right.slider(
    "Monthly Charges", min_value=0, max_value=200, step=10, value=70
)

techsupport = int(st.toggle("Tech Support", value=False))

payload = {
    "tenure": int(tenure),
    "monthly": int(monthly),
    "techsupport": int(techsupport),
}

try:
    data = fetch_prediction(payload)
    prediction = data.get("prediction")

    st.subheader("Result")
    st.write(f"Model prediction: **{prediction}**")

    st.json(data)

except requests.RequestException as e:
    st.error(f"Error calling API: {e}")
