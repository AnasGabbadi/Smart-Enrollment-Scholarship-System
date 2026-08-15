# Smart Enrollment & Scholarship System

An intelligent enrollment and scholarship management system for Moroccan students, powered by Machine Learning. The system uses three ML models (Linear Regression, Decision Tree, and SVM) to predict financial capacity, recommend scholarship types, and estimate enrollment probability through a consensus-based ranking mechanism.

## Architecture

```
React Frontend (port 3000)  <-->  FastAPI Backend (port 8000)  <-->  MongoDB
        |                              |
   Tailwind CSS                   3 ML Models (pickle)
   Chart.js / Recharts            LinearRegression
   framer-motion                  DecisionTreeClassifier
   lucide-react                   SGDClassifier (SVM surrogate)
```

## Features

### Machine Learning Pipeline
- **Linear Regression** — Predicts financial capacity score (0–100) using GPA, exam score, income, dependents, and distance
- **Decision Tree** — Recommends scholarship type (None / 25% / 50% / 100%) based on GPA, income, and dependents
- **SVM (SGD Classifier)** — Predicts enrollment probability (Low / Medium / High)
- **Consensus Ranking** — Merges all three model scores to rank students respecting yearly quotas

### Admin Dashboard
- Student CRUD with approval/rejection workflow
- Yearly quota management for scholarships
- ML model performance visualization (accuracy, precision, F1, feature importance)
- Consensus-based student ranking with quota-aware allocation
- Export reports (PDF, PNG, CSV)
- System statistics overview

### Student Interface
- Registration with Moroccan Baccalaureate data
- AI-generated recommendations: financial capacity, scholarship type, enrollment probability
- Profile management

### Interactive Presentation
- 15-slide interactive 3D presentation built with Framer Motion and Recharts
- Covers ML concepts, dataset, model details, and results

## Tech Stack

| Layer       | Technology                                      |
|-------------|-------------------------------------------------|
| Frontend    | React 18, Tailwind CSS 3, Chart.js, Recharts, Framer Motion |
| Backend     | Python 3.11+, FastAPI, scikit-learn, joblib     |
| Database    | MongoDB (PyMongo)                               |
| Auth        | passlib + bcrypt                                |
| API Style   | RESTful, Pydantic v2 validation                 |

## API Endpoints

| Prefix              | Description                         |
|---------------------|-------------------------------------|
| `/api/v1/etudiants`   | Student CRUD, login, approve/reject |
| `/api/v1/predictions` | ML predictions for a student        |
| `/api/v1/modeles`     | Model info, performance, comparison |
| `/api/v1/statistiques` | System stats and chart generation  |
| `/api/v1/quotas`      | Yearly scholarship quota management |
| `/api/v1/ml-ranking`  | Consensus-based student ranking     |

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- MongoDB (local or Atlas)

### Backend Setup

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and configure your MongoDB URI. Then:

```bash
python generate_dataset.py  # Generate the synthetic dataset (~5s, 30k rows)
python train_models.py      # Train the 3 ML models (~seconds)
python application.py       # Start the API server
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

The app opens at `http://localhost:3000`. The API runs at `http://localhost:8000`.

## Dataset

The original dataset used early in this project (500,000 rows) was lost and never committed — it was never versioned in git, only referenced by filename. Rather than ship a project that can't actually be trained end-to-end, the dataset is now **generated synthetically** by [`backend/generate_dataset.py`](backend/generate_dataset.py), with a fixed seed (`SEED = 42`) so it's fully reproducible: anyone who clones the repo gets the exact same data by running the script, instead of trusting an opaque 500k-row CSV nobody can verify.

```bash
cd backend
python generate_dataset.py   # writes moroccan_students_scholarship_dataset.csv at the repo root
```

- **30,000 rows** by default (override with `N_LIGNES_DATASET`, e.g. `N_LIGNES_DATASET=50000 python generate_dataset.py`) — enough to train all 3 models properly, small enough to regenerate and train in seconds on any machine that clones the repo, instead of the original's 500k rows.
- Columns: `gpa`, `exam_score`, `family_income`, `dependents`, `distance_km`, `region`, plus the 3 targets `financial_capacity_score` (regression), `scholarship_class` (0–3), and `enrollment_probability_class` (0–2).
- Features are drawn from distributions chosen to resemble the real quantities (log-normal income, Poisson dependents, exponential distance, Moroccan-region weights), and each target is a weighted composite of the features **plus Gaussian noise added before thresholding** — so the problem has a real but imperfect signal, not a deterministic rule that would produce unrealistically perfect metrics.
- **The generated CSV is gitignored** (`*.csv` in `.gitignore`) — only the generator script is committed. Every clone regenerates its own copy from the same seed rather than storing a 30k-row CSV in git history.

**No more silent heuristic fallback:** each model wrapper (`backend/modeles/regression_lineaire.py`, `arbre_decision.py`, `svm.py`) loads its `.pkl` on startup and, on any failure (missing file, or a `numpy`/`scikit-learn` version mismatch with the environment that pickled it — the versions must match `backend/requirements.txt`), falls back to a stub model fit on a handful of hardcoded rows, or to inline heuristic rules in `predire()`. Running the two commands below produces all 3 `.pkl` files, so all 3 models load and predict from real trained weights instead of the fallback:

```bash
python generate_dataset.py
python train_models.py       # 80/20 split, trains and saves all 3 models
```

### Model performance (30,000-row synthetic dataset, seed 42, 80/20 split)

Recalculated from scratch against the regenerated dataset — not carried over from the old, lost 500k dataset.

| Model | Target | Metric | Value |
|-------|--------|--------|-------|
| Linear Regression | `financial_capacity_score` | R² | 0.285 |
| | | RMSE | 12.14 |
| | | MAE | 9.67 |
| Decision Tree | `scholarship_class` (4 classes) | Accuracy | 46.5% |
| | | F1 (weighted) | 0.432 |
| SGD Classifier ("SVM") | `enrollment_probability_class` (3 classes) | Accuracy | 46.9% |
| | | F1 (weighted) | 0.411 |

These are honest numbers for a noisy synthetic problem — well above chance (33%/25% baselines for 3/4-class targets) but not the near-perfect scores an opaque or leaky dataset would produce. `SGDClassifier` is scale-sensitive, so `svm.py` fits and persists a `StandardScaler` alongside the model and applies it at both train and inference time; skipping that step (as an earlier version of this pipeline did) silently drops accuracy below the majority-class baseline.

To reproduce these numbers yourself: `cd backend && python generate_dataset.py && python train_models.py` — the script prints the same metrics recalculated live, not hardcoded.

## Documentation

- [Technical documentation](docs/DOCUMENTATION.md) — architecture diagrams, data flow, ML model diagrams, use-case/sequence/activity diagrams (in French)
- [Interactive presentation guide](docs/PRESENTATION_README.md) — how the 15-slide in-app presentation feature works, navigation, and content per slide (in French)

## License

Built for the academic project "Système Intelligent d'Admission et d'Attribution de Bourses" — Academic Year 2025–2026.
