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
python train_models.py    # Train ML models (~2 min on 500k records)
python application.py     # Start the API server
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

The app opens at `http://localhost:3000`. The API runs at `http://localhost:8000`.

## Dataset

The synthetic dataset (`moroccan_students_scholarship_dataset_500k.csv`) contains 500,000 Moroccan student records with features such as GPA, exam scores, family income, dependents, distance, region, and labeled targets (financial capacity, scholarship class, enrollment probability).

**⚠️ The dataset is not included in this repository** (it's gitignored, see `.gitignore`) and there is no script here to regenerate it. Without it, `train_models.py` cannot run, so `modeles_entraines/*.pkl` cannot be (re)produced.

**Known limitation — silent heuristic fallback:** each model wrapper (`backend/modeles/regression_lineaire.py`, `arbre_decision.py`, `svm.py`) loads its `.pkl` on startup and, on any failure (missing file, or a `numpy`/`scikit-learn` version mismatch with the environment that pickled it — the versions must match `backend/requirements.txt`), silently falls back to a stub model fit on 4 hardcoded dummy rows, or to inline heuristic rules in `predire()`. This fallback logs a warning but does not fail startup or the API call, so predictions can look real while actually coming from the stub.
- As shipped, only `modele_arbre_decision.pkl` exists under `modeles_entraines/`; `modele_regression_lineaire.pkl` and `modele_svm.pkl` are absent, so those two models **always** run on the heuristic fallback until you train on a real dataset.
- If you have access to the original dataset, place it at the repo root and run `python train_models.py` inside a venv built from `backend/requirements.txt` (pinned `numpy==1.24.3`, `scikit-learn==1.3.2`) to produce trustworthy `.pkl` files.

## Documentation

- [Technical documentation](docs/DOCUMENTATION.md) — architecture diagrams, data flow, ML model diagrams, use-case/sequence/activity diagrams (in French)
- [Interactive presentation guide](docs/PRESENTATION_README.md) — how the 15-slide in-app presentation feature works, navigation, and content per slide (in French)

## License

Built for the academic project "Système Intelligent d'Admission et d'Attribution de Bourses" — Academic Year 2025–2026.
