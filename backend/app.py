from pathlib import Path
from typing import List

import numpy as np
import onnxruntime as ort
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI(title="Salary Prediction API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent

# Numeric feature order and scaler stats pulled from the original sklearn StandardScaler
NUMERIC_FEATURES: List[str] = [
    "remote_ratio",
    "years_experience",
    "skill_AWS",
    "skill_Azure",
    "skill_Computer Vision",
    "skill_Data Visualization",
    "skill_Deep Learning",
    "skill_Docker",
    "skill_GCP",
    "skill_Git",
    "skill_Hadoop",
    "skill_Java",
    "skill_Kubernetes",
    "skill_Linux",
    "skill_MLOps",
    "skill_Mathematics",
    "skill_NLP",
    "skill_PyTorch",
    "skill_Python",
    "skill_R",
    "skill_SQL",
    "skill_Scala",
    "skill_Spark",
    "skill_Statistics",
    "skill_Tableau",
    "skill_TensorFlow",
    "skill_count",
]
NUMERIC_MEAN = np.array(
    [
        49.08888889,
        6.18364444,
        0.13377778,
        0.1424,
        0.15075556,
        0.14995556,
        0.144,
        0.12444444,
        0.16355556,
        0.1736,
        0.16151111,
        0.16977778,
        0.20311111,
        0.17786667,
        0.14275556,
        0.12791111,
        0.1432,
        0.18666667,
        0.29937778,
        0.15484444,
        0.22746667,
        0.1904,
        0.14124444,
        0.12453333,
        0.156,
        0.20275556,
        3.99191111,
    ],
    dtype=np.float32,
)
NUMERIC_SCALE = np.array(
    [
        40.81738313,
        5.50715567,
        0.3404134,
        0.34945993,
        0.35781045,
        0.35702785,
        0.35108973,
        0.3300879,
        0.36987178,
        0.37876515,
        0.36800173,
        0.37543746,
        0.40231454,
        0.38240046,
        0.34982339,
        0.33399081,
        0.35027669,
        0.38964371,
        0.45798551,
        0.36175633,
        0.41919635,
        0.39261666,
        0.34827353,
        0.33018901,
        0.36285534,
        0.40205191,
        0.81727264,
    ],
    dtype=np.float32,
)

# Categorical levels from the original OneHotEncoder (drop="first")
CATEGORY_LEVELS = {
    "job_title": [
        "AI Architect",
        "AI Consultant",
        "AI Product Manager",
        "AI Research Scientist",
        "AI Software Engineer",
        "AI Specialist",
        "Autonomous Systems Engineer",
        "Computer Vision Engineer",
        "Data Analyst",
        "Data Engineer",
        "Data Scientist",
        "Deep Learning Engineer",
        "Head of AI",
        "ML Ops Engineer",
        "Machine Learning Engineer",
        "Machine Learning Researcher",
        "NLP Engineer",
        "Principal Data Scientist",
        "Research Scientist",
        "Robotics Engineer",
    ],
    "experience_level": ["EN", "EX", "MI", "SE"],
    "employment_type": ["CT", "FL", "FT", "PT"],
    "company_location": [
        "Australia",
        "Austria",
        "Canada",
        "China",
        "Denmark",
        "Finland",
        "France",
        "Germany",
        "India",
        "Ireland",
        "Israel",
        "Japan",
        "Netherlands",
        "Norway",
        "Singapore",
        "South Korea",
        "Sweden",
        "Switzerland",
        "United Kingdom",
        "United States",
    ],
    "company_size": ["L", "M", "S"],
    "education_required": ["Associate", "Bachelor", "Master", "PhD"],
    "industry": [
        "Automotive",
        "Consulting",
        "Education",
        "Energy",
        "Finance",
        "Gaming",
        "Government",
        "Healthcare",
        "Manufacturing",
        "Media",
        "Real Estate",
        "Retail",
        "Technology",
        "Telecommunications",
        "Transportation",
    ],
}
CATEGORY_ORDER = [
    "job_title",
    "experience_level",
    "employment_type",
    "company_location",
    "company_size",
    "education_required",
    "industry",
]

# Map UI inputs to numeric years used in training
YEARS_EXPERIENCE_MAPPING = {
    "0-1": 0.5,
    "1-3": 2,
    "3-5": 4,
    "5-7": 6,
    "7-10": 8.5,
    "10+": 12,
}


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


def _standardize_numeric(values: List[float]) -> np.ndarray:
    raw = np.array(values, dtype=np.float32)
    return (raw - NUMERIC_MEAN) / NUMERIC_SCALE


def _encode_categorical(feature: str, value: str) -> List[float]:
    categories = CATEGORY_LEVELS[feature]
    # drop="first" -> skip the first category
    return [1.0 if value == cat else 0.0 for cat in categories[1:]]


def build_feature_vector(data: PredictionInput) -> np.ndarray:
    """
    Re-implement the preprocessing pipeline from the original sklearn ColumnTransformer.
    """
    try:
        remote_ratio = float(data.remoteWork)
    except (TypeError, ValueError):
        remote_ratio = 0.0
    years_exp = YEARS_EXPERIENCE_MAPPING.get(data.yearsExperience, 2.0)

    # Skills are not captured in the UI; set to zero as in the previous implementation.
    numeric_raw = [
        remote_ratio,
        years_exp,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ]
    numeric_scaled = _standardize_numeric(numeric_raw)

    categorical_values = {
        "job_title": data.jobTitle,
        "experience_level": data.experienceLevel,
        "employment_type": data.employmentType,
        "company_location": data.country,
        "company_size": data.companySize,
        "education_required": data.education,
        "industry": data.industry,
    }

    categorical_encoded: List[float] = []
    for feature in CATEGORY_ORDER:
        categorical_encoded.extend(_encode_categorical(feature, categorical_values.get(feature, "")))

    feature_vector = np.concatenate([numeric_scaled, np.array(categorical_encoded, dtype=np.float32)], axis=0)
    if feature_vector.shape[0] != 90:
        raise ValueError(f"Feature vector has wrong size: {feature_vector.shape[0]}")
    return feature_vector.reshape(1, -1).astype(np.float32)


def load_session():
    model_path = BASE_DIR / "best_model.onnx"
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found at {model_path}")
    session = ort.InferenceSession(model_path.read_bytes(), providers=["CPUExecutionProvider"])
    return session


try:
    session = load_session()
    MODEL_STATUS = "loaded"
except Exception as e:
    print(f"Error loading ONNX model: {e}")
    session = None
    MODEL_STATUS = f"error: {e}"


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy" if session is not None else "unavailable",
        "message": "API is running",
        "model": MODEL_STATUS,
    }


@app.post("/api/predict", response_model=PredictionResponse)
async def predict_salary(input_data: PredictionInput):
    """
    Predict salary based on input features using ONNXRuntime to stay lightweight on Vercel.
    """
    if session is None:
        raise HTTPException(status_code=500, detail="Model not loaded. Please check server logs.")

    try:
        features = build_feature_vector(input_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Input preprocessing failed: {e}")

    try:
        ort_outputs = session.run(None, {"X": features})
        predicted_salary = float(ort_outputs[0][0][0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ONNX inference failed: {e}")

    predicted_salary = max(0.0, predicted_salary)

    return {
        "success": True,
        "predictedSalary": round(predicted_salary, 2),
        "currency": "USD",
        "period": "annual",
        "input": input_data.dict(),
        "note": "Prediction based on ONNX model via ONNX Runtime",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
