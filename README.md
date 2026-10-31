
# SalesGuard AI

Advanced retail sales forecasting and model drift monitoring.

## Technology stack

- Python
- Pandas and NumPy
- Scikit-learn
- FastAPI
- Streamlit
- Plotly
- SQLite
- Pytest
- Docker

## Project objectives

1. Forecast product demand.
2. Validate incoming sales data.
3. Detect feature distribution drift.
4. Monitor prediction distribution changes.
5. Evaluate forecast accuracy after actual sales arrive.
6. Generate monitoring alerts.
7. Train and compare candidate models.
8. Require review before promoting a candidate.

## Installation

Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Generate sales data and train the model:

```powershell
python scripts/generate_sales_data.py
python scripts/train_model.py
```

Start the API:

```powershell
uvicorn app.main:app --reload
```

Start the dashboard in a second terminal:

```powershell
streamlit run dashboard/Home.py
```

## Local URLs

- Dashboard: http://localhost:8501
- API: http://127.0.0.1:8000
- API documentation: http://127.0.0.1:8000/docs

## Testing

```powershell
python -m pytest -v
```

## Important

The included dataset is synthetic. Replace it with properly
validated historical company sales before using the model
to make real business decisions.

The monitoring thresholds are illustrative. Retraining
produces a candidate model; it does not automatically
replace the active model.
