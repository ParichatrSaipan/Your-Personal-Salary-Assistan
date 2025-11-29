#  Data Analytics Project: Your Personal Salary Assistant WebApp

A full-stack web application that predicts salaries based on job characteristics using machine learning. This project is based on [data_analytics_project](https://github.com/ParichatrSaipan/data_analytics_project.git)

## Table of Contents

- [Tech Stack](#tech-stack)
- [Installation](#installation)
  - [Frontend Setup](#frontend-setup)
  - [Backend Setup](#backend-setup)
- [Usage](#usage)
  - [Running the Backend](#running-the-backend)
  - [Running the Frontend](#running-the-frontend-local-or-development-mode)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)

## Tech Stack

### Frontend
- React 19.2.0
- Vite (Rolldown)
- JavaScript/JSX

### Backend
- Python
- FastAPI
- scikit-learn (Machine Learning)
- ONNX (Model optimization)
- Pandas & NumPy

## Installation

### Frontend Setup
1. Clone the repository

```bash
git clone https://github.com/ParichatrSaipan/Your-Personal-Salary-Assistan.git
```

2. Install frontend dependencies:
```bash
cd Your-Personal-Salary-Assistan
npm install
```

### Backend Setup
1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install backend dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Backend
From the backend directory:
```bash
python app.py
```
Or using uvicorn:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```
The API will be available at `http://localhost:8000`

### Running the Frontend (local or Development mode)

Start the local or development server:
```bash
npm run dev
```

## Project Structure

```
Your-Personal-Salary-Assistan/
├── backend/              # FastAPI backend with ML model
│   ├── app.py           # Main API application
│   ├── best_model.pkl   # Trained ML model
│   ├── best_model.onnx  # Optimized ONNX model
│   ├── preprocessor.pkl # Data preprocessor
│   └── requirements.txt # Python dependencies
├── salary/              # React frontend application
├── package.json         # Root package configuration
└── README.md            # This file
```

## API Endpoints

- `GET /api/health` - Health check
- `POST /api/predict` - Predict salary based on job characteristics
- `GET /api/model-info` - Get model information

For detailed API documentation, see [backend/README.md](backend/README.md)

For details on how to train the model, see [data_analytics_project](https://github.com/ParichatrSaipan/data_analytics_project.git)
