"""API for making churn predictions using a FastAPI server.

Add fastapi and uvicorn to your environment with:
    uv add fastapi uvicorn # it is hosting the api for us

To serve the API, run:
    uv run uvicorn api:app --reload
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field

from prediction import make_prediction


# Field names match those used in the model training
# Aliases are more user-friendly names for the API
class Customer(BaseModel):
    tenure: int
    MonthlyCharges: int = Field(alias="monthly")
    TechSupport_yes: int = Field(alias="techsupport")


app = FastAPI() # makes it easy to define actions


@app.post("/predict")
def predict(customer: Customer): # taken from customer function
    """Make a churn prediction for a customer."""
    prediction = make_prediction(**customer.model_dump()) # e.g. tenure=tenure, etc.
    return {"prediction": prediction} # automatically converted into dictionary through json


@app.get("/schema")
def predict_schema():
    """Describe the expected fields for /predict."""
    return Customer.model_json_schema() # you can get the schema to run the api
