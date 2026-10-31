# ML Model Drift Monitoring Dashboard

An advanced machine learning monitoring platform built to track data quality, detect data drift, monitor prediction changes, evaluate model performance, and identify when model retraining is required.

## Project Overview

Machine learning models can lose accuracy over time when real-world data changes. This is known as model drift.

This project provides a monitoring solution for retail sales prediction models. It compares incoming sales data with reference data, evaluates prediction distributions, monitors model performance, and generates alerts when monitoring thresholds are exceeded.

## Technology Stack

- Python
- FastAPI – REST API backend
- Streamlit – Interactive dashboard
- Scikit-learn – Machine learning
- Pandas and NumPy – Data processing
- SciPy – Statistical calculations
- Plotly – Interactive visualizations
- SQLite / SQLAlchemy – Database
- Pytest – Testing
- Docker – Containerization

## System Architecture

1. Sales data is generated or submitted to the system.
2. Data validation checks the incoming dataset.
3. The trained ML model generates predictions.
4. Data drift monitoring compares incoming features against reference data.
5. Prediction drift monitoring identifies changes in prediction distributions.
6. Performance monitoring evaluates predictions against actual sales.
7. Alert rules identify critical issues.
8. Retraining logic evaluates whether a candidate model should be trained and compared with the current model.
9. The Streamlit dashboard displays monitoring results.

## Dashboard Modules

- Sales Overview
- Data Quality Monitoring
- Data Drift Monitoring
- Prediction Drift Monitoring
- Model Performance
- Alerts and Incidents
- Model Registry
- Retraining Center

## Run Locally

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start the FastAPI backend

```bash
python -m uvicorn app.main:app --reload
```

API: http://127.0.0.1:8000

API documentation: http://127.0.0.1:8000/docs

### Start the Streamlit dashboard

```bash
streamlit run dashboard/Home.py
```

Dashboard: http://localhost:8501

## Project Use Cases

- Retail sales prediction monitoring
- Detecting changes in incoming business data
- Monitoring machine learning model reliability
- Identifying prediction distribution changes
- Evaluating model performance over time
- Supporting model retraining decisions
- Demonstrating MLOps monitoring workflows

## Important

This is a local demonstration project. The localhost URLs work only on your computer. Public access requires deployment to a hosting platform. Model retraining decisions require evaluation and approval; the system does not automatically promote every candidate model.

## Author

Vrunda Utekar

GitHub: https://github.com/vrundautekar111
