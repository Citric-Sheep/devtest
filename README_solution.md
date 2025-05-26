# Elevator Resting Floor Data Pipeline

This repository implements the core of a data engineering and feature preparation pipeline for the "elevator resting floor" modeling challenge.

## Structure

- **generate_dataset.py**  
  Extracts raw event data from the SQLite database and saves it as a pickle artifact for further processing.

- **preprocess.py**  
  Performs feature engineering on event data, including time-based, cyclical, rolling, and conditional features. Data is output in a clean, ML-ready tabular format. All boolean fields are encoded as integers (0/1).

- **train.py**  
  Trains a prediction model to anticipate the next calling floor based on historical demand and engineered features. Uses a temporal split to separate train/test, reflecting real-world deployment.

- **model.py**  
  Defines a class for loading the trained model and producing predictions given new data. Features are recomputed for single-record inference, using defaults for features that require historical context.

- **settings.py**  
  Centralizes all file paths, feature lists, and relevant pipeline constants.

## Data Model

Events are stored in a table named `elevator_calls`, with at minimum:
- `timestamp`
- `calling_floor`

During preprocessing, additional features are derived, including:
- Previous resting floor
- Time-based and cyclical encodings
- Rolling counts and averages per floor
- Conditional frequencies based on the previous resting floor

## Key Design Choices

- **Temporal split:**  
  Train/test sets are split chronologically to simulate realistic production inference and avoid data leakage.

- **Feature set:**  
  Engineered features include recent call frequencies, conditional stats (e.g., "calls from floor X when resting at Y"), and cyclical encodings for hours/days.

- **Data artifacts:**  
  Intermediate datasets and models are versioned and stored as pickles for reproducibility.

- **Extendability:**  
  The current schema and scripts are straightforward to adapt for multi-elevator scenarios or richer sensor data.

## Usage

1. Generate or extract event data:
```
python 01_generate_dataset.py
````

2. Preprocess features:
```
python 02_preprocess.py
```

3. Train the model:
```
python 03_train.py
```

4. Run inference (from a notebook or script):
```
from model import ElevetorModel
m = ElevetorModel()
m.predict({"timestamp": "2024-06-01 10:00:00", "calling_floor": 5, "resting_floor": 3})
```

## Next Steps
- **Collect production data:**  
  Integrate this pipeline with a live data source (e.g., sensor logs, building management API) to gather real elevator usage data. Real behavioral data will reveal meaningful demand patterns and allow for richer feature engineering.

- **Iterate on feature engineering:**  
  With real data, re-evaluate which features are most predictive. Additional signals—such as trip direction, user IDs, or elevator occupancy—could be incorporated. Time-of-day and seasonality patterns should be validated and potentially modeled more granularly.

- **Model evaluation and tuning:**  
  Compare different algorithms (tree-based models, time series approaches, etc.), run cross-validation, and monitor for overfitting. Feature importance analysis will help prioritize which features drive prediction quality.

- **Error analysis:**  
  Systematically analyze cases where the model mispredicts. Use these insights to refine feature sets, handle edge cases, and improve the definition of the "optimal" resting floor policy (e.g., optimizing for average wait time vs. call frequency).

- **Scalability:**  
  Extend the schema and pipeline to handle multiple elevators and more complex building layouts. Add support for batch ingestion and parallel processing as needed.

- **Productionization:**  
  Package the pipeline for deployment as a service (API, scheduled job, etc.). Add monitoring for data drift and model performance. Establish processes for regular retraining and validation as new data arrives.

- **Testing and validation:**  
  Add automated tests to cover core feature transformations and edge cases. Validate that the data pipeline handles missing values, outliers, and schema changes gracefully.

---

## Assumptions

- **Synthetic data:**  
  The current pipeline uses generated data to demonstrate the end-to-end flow. No assumptions about actual user behavior, peak times, or real demand cycles are built in; all results and scores should be interpreted in that light. The model is designed to be robust to real data once available.

- **Resting floor logic:**  
  The “resting_floor” feature is approximated as the last known floor at which a call occurred. In a production setting, this would ideally be recorded explicitly when the elevator becomes idle.

- **Single-elevator focus:**  
  The data model assumes a single elevator in the building. Extension to multiple elevators would require an additional `elevator_id` field and further schema adjustments.

- **Border cases (e.g., move-ins/move-outs, group calls):**  
  The pipeline currently does not account for outlier scenarios such as bulk move-ins/move-outs (unusually high demand from a single floor), or simultaneous calls by multiple users. All events are treated as independent, single-person elevator calls. In real deployments, these cases may need special handling or outlier filtering.

- **No assumption on trip direction or group occupancy:**  
  Calls are treated as single-direction, single-user events. The system does not currently attempt to infer or record whether multiple users are entering/exiting together, or the direction of elevator travel (up vs. down) for each call.

---


