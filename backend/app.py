from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Salary Prediction API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained model and preprocessor
try:
    BASE_DIR = Path(__file__).resolve().parent
    model = joblib.load(BASE_DIR / "best_model.pkl")
    preprocessor = joblib.load(BASE_DIR / "preprocessor.pkl")
    print("Model and preprocessor loaded successfully!")
    print(f"Model type: {type(model)}")
    print(f"Expected features: {preprocessor.feature_names_in_}")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None
    preprocessor = None

# List of all skills the model expects
ALL_SKILLS = [
    "AWS",
    "Azure",
    "Computer Vision",
    "Data Visualization",
    "Deep Learning",
    "Docker",
    "GCP",
    "Git",
    "Hadoop",
    "Java",
    "Kubernetes",
    "Linux",
    "MLOps",
    "Mathematics",
    "NLP",
    "PyTorch",
    "Python",
    "R",
    "SQL",
    "Scala",
    "Spark",
    "Statistics",
    "Tableau",
    "TensorFlow",
]

# Years experience mapping
YEARS_EXPERIENCE_MAPPING = {
    "0-1": 0.5,
    "1-3": 2,
    "3-5": 4,
    "5-7": 6,
    "7-10": 8.5,
    "10+": 12,
}


# Pydantic models for request/response
class PredictionInput(BaseModel):
    jobTitle: str
    experienceLevel: str
    yearsExperience: str
    employmentType: str
    remoteWork: str
    companySize: str
    country: str
    industry: str
    education: str


class PredictionResponse(BaseModel):
    success: bool
    predictedSalary: float
    currency: str
    period: str
    input: dict
    note: str


class HealthResponse(BaseModel):
    status: str
    message: str
    model: str
    preprocessor: str


def preprocess_input(data: PredictionInput):
    """
    Convert input data to the format expected by the model
    The model expects these columns in order:
    - remote_ratio (numeric)
    - years_experience (numeric)
    - skill_* columns (binary 0/1 for each skill)
    - skill_count (total number of skills)
    - job_title (categorical)
    - experience_level (categorical)
    - employment_type (categorical)
    - company_location (categorical)
    - company_size (categorical)
    - education_required (categorical)
    - industry (categorical)
    """
    # Create a dictionary with all expected features
    input_dict = {}

    # Numeric features
    input_dict["remote_ratio"] = int(data.remoteWork) / 100  # Convert to 0-1 scale
    input_dict["years_experience"] = YEARS_EXPERIENCE_MAPPING.get(data.yearsExperience, 2)

    # Skill features - set all to 0 as default (we don't collect this in the form)
    for skill in ALL_SKILLS:
        input_dict[f"skill_{skill}"] = 0

    # Skill count - set to 0 as we don't collect skills
    input_dict["skill_count"] = 0

    # Categorical features
    input_dict["job_title"] = data.jobTitle
    input_dict["experience_level"] = data.experienceLevel
    input_dict["employment_type"] = data.employmentType
    input_dict["company_location"] = data.country
    input_dict["company_size"] = data.companySize
    input_dict["education_required"] = data.education
    input_dict["industry"] = data.industry

    # Convert to DataFrame (preprocessor expects this format)
    df = pd.DataFrame([input_dict])

    return df


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    model_status = "loaded" if model is not None else "not loaded"
    preprocessor_status = "loaded" if preprocessor is not None else "not loaded"
    return {
        "status": "healthy",
        "message": "API is running",
        "model": model_status,
        "preprocessor": preprocessor_status,
    }


@app.post("/api/predict", response_model=PredictionResponse)
async def predict_salary(input_data: PredictionInput):
    """
    Predict salary based on input features
    """
    try:
        # Check if model is loaded
        if model is None or preprocessor is None:
            raise HTTPException(
                status_code=500,
                detail="Model not loaded. Please check server logs.",
            )

        # Preprocess input
        input_df = preprocess_input(input_data)

        # Transform using preprocessor
        try:
            features_transformed = preprocessor.transform(input_df)
        except Exception as e:
            print(f"Preprocessing error: {e}")
            print(f"Input DataFrame:\n{input_df}")
            raise HTTPException(
                status_code=500,
                detail=f"Preprocessing error: {str(e)}",
            )

        # Make prediction
        try:
            predicted_salary = model.predict(features_transformed)[0]
        except Exception as e:
            print(f"Prediction error: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Prediction error: {str(e)}",
            )

        # Ensure prediction is positive
        predicted_salary = max(0, predicted_salary)

        # Return prediction
        return {
            "success": True,
            "predictedSalary": round(float(predicted_salary), 2),
            "currency": "USD",
            "period": "annual",
            "input": input_data.dict(),
            "note": "Prediction based on trained GradientBoostingRegressor model",
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@app.get("/api/model-info")
async def model_info():
    """Return information about the model"""
    if model is None:
        raise HTTPException(
            status_code=500,
            detail="Model not loaded",
        )

    return {
        "model_type": str(type(model).__name__),
        "model_params": model.get_params() if hasattr(model, "get_params") else "N/A",
        "expected_features": list(preprocessor.feature_names_in_) if preprocessor else [],
        "n_features": preprocessor.n_features_in_ if preprocessor else 0,
        "note": "This model expects skill data which is not collected in the form. Default values are used for skills.",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
