# Elevator Resting Floor Data Collector

## 🚀 Objective
Record elevator usage events to later train a predictive model that suggests the ideal "resting floor" for an elevator.

## 📦 How to Run

### Local Environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
