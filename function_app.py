import logging
import azure.functions as func
from prediction import make_prediction

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="http_trigger_thomas")
def http_trigger_thomas(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    # Get query params (as strings)
    tenure = req.params.get("tenure")
    monthly = req.params.get("monthly")
    techsupport = req.params.get("techsupport")

    # Validate required parameters first
    if not (tenure and monthly and techsupport):
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass tenure, monthly, techsupport to get a prediction.",
            status_code=400,
        )

    try:
        # Call your model/prediction function
        prediction = make_prediction(
            tenure=tenure,
            MonthlyCharges=monthly,
            TechSupport_yes=techsupport,
        )
    except Exception as e:
        # Return a 500 on unexpected errors from prediction
        logging.exception("Prediction failed")
        return func.HttpResponse(f"Prediction error: {e}", status_code=500)

    return func.HttpResponse(
        f"Hello. The probability that this customer will churn is {prediction}"
    )
