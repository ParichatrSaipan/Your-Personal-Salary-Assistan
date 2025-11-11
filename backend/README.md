# Salary Prediction API

Backend API for predicting salaries based on job characteristics, built with **FastAPI**.

## Setup

1. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python app.py
```

Or use uvicorn directly:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

**Note:** If port 5000 is already in use on macOS (by AirPlay/ControlCenter), the server will run on port 8000 instead.

## API Documentation

FastAPI provides automatic interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

### Health Check
```
GET /api/health
```

### Predict Salary
```
POST /api/predict
Content-Type: application/json

{
  "jobTitle": "Data Scientist",
  "experienceLevel": "SE",
  "yearsExperience": "5-7",
  "employmentType": "FT",
  "remoteWork": "100",
  "companySize": "L",
  "country": "United States",
  "industry": "Technology",
  "education": "Master"
}
```

Response:
```json
{
  "success": true,
  "predictedSalary": 125000.50,
  "currency": "USD",
  "period": "annual",
  "input": { ... }
}
```

### Model Info
```
GET /api/model-info
```

## Integrating Your Trained Model

1. Train your model using your preferred ML framework (scikit-learn, TensorFlow, PyTorch, etc.)

2. Save the model:
```python
import pickle
pickle.dump(model, open('salary_model.pkl', 'wb'))
```

3. Update `app.py`:
   - Uncomment the model loading code at the top
   - Replace the placeholder prediction logic with actual model prediction
   - Ensure feature preprocessing matches your training pipeline

Example:
```python
from model_loader import load_model

# Load model at startup
model = load_model('salary_model.pkl')

# In predict_salary function:
predicted_salary = model.predict(features)[0]
```

## Feature Encoding

The API expects the following fields and automatically encodes them:

- **jobTitle**: 10 categories (0-9)
- **experienceLevel**: EN, MI, SE, EX (0-3)
- **yearsExperience**: Converted to numeric midpoint
- **employmentType**: FT, PT, CT, FL (0-3)
- **remoteWork**: 0, 50, 100 (percentage)
- **companySize**: S, M, L (0-2)
- **country**: 15 countries (0-14)
- **industry**: 11 industries (0-10)
- **education**: 4 levels (0-3)

Make sure your model training uses the same encoding scheme.
