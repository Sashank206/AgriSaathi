# AgriSaathi – Our Farmer Friend

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React_19_+_Vite-61DAFB?logo=react&logoColor=black)](https://react.dev)
[![Tailwind CSS](https://img.shields.io/badge/Styling-Tailwind_CSS_v4-38B2AC?logo=tailwind-css&logoColor=white)](https://tailwindcss.com)
[![MongoDB](https://img.shields.io/badge/Database-MongoDB_Atlas-47A248?logo=mongodb&logoColor=white)](https://mongodb.com)

**AgriSaathi** is an AI-powered agricultural advisory platform designed to help Indian farmers make informed, data-driven farming decisions. The platform unifies deep-learning plant disease diagnosis, location-driven crop recommendations, transparent fertilizer market comparisons, and smart agro-meteorological alerts into a single cohesive system.

---

## 🌾 Core Modules Overview

1. **AI-Based Plant Disease Detection & Treatment Recommendation (Primary AI)**
   - Upload leaf images or capture photos live via mobile/desktop camera.
   - High-throughput image validation (file integrity, resolution thresholds, format checks).
   - Modular CNN/ResNet-50 pipeline ready for trained Keras weights.
   - Comprehensive agronomic knowledge base (early blight, late blight, bacterial blight, blast) providing symptoms, organic biocontrols, and chemical treatments.
   - One-click case routing to certified Krishi Vigyan Kendra (KVK) Agricultural Experts.

2. **Location-Based Smart Crop Recommendation**
   - **No manual NPK chemical guessing required.**
   - Evaluates location via browser GPS or State/District selection.
   - Combines regional ICAR soil series, practical irrigation sources (Borewell, Canal, Rain-fed), and seasonal climate patterns (Kharif, Rabi, Zaid).
   - Scikit-learn Random Forest / XGBoost interface with transparent fallback reporting.

3. **Fertilizer Price & Quality Comparison**
   - Verified product catalog (Urea, DAP, MOP, SSP, Complex NPK, Vermicompost, Zinc Sulfate).
   - Mathematical multi-factor ranking formula:
     $$S_i = \alpha\left(1 - \frac{u_i}{u_{\max}}\right) + (1 - \alpha)\left(\frac{r_i}{r_{\max}}\right)$$
   - Interactive $\alpha$ weighting slider allowing farmers to balance unit cost (₹/kg) against peer review ratings.

4. **Weather Monitoring & Smart Agricultural Alerts**
   - Live satellite meteorological feed via OpenWeatherMap API with automatic regional climate fallback.
   - Rule-based agricultural alert engine for heavy downpours (waterlogging risks), gusty winds (cereal lodging risks), frost/chilling warnings, and excessive heat stress.

---

## 🏛️ Monorepo Architecture

```
AgriSaathi/
|
|-- frontend/                       # React 19 + Vite + Tailwind CSS v4
|   |-- src/
|   |   |-- components/             # Reusable UI: Navbar, Footer, Sidebar, Header, etc.
|   |   |-- context/                # AuthContext (JWT session state & role management)
|   |   |-- dashboards/             # FarmerDashboard, AdminDashboard, ExpertDashboard
|   |   |-- layouts/                # PublicLayout, DashboardLayout (Protected routes)
|   |   |-- pages/                  # Landing, Features, How It Works, About, Contact,
|   |   |                           # DiseaseDetection, CropRecommendation,
|   |   |                           # FertilizerComparison, WeatherPage, Login, Register
|   |   |-- services/               # Axios API client layer (api.js)
|   |   |-- App.jsx                 # Client-side router & role guards
|   |   |-- main.jsx                # Application mount point
|   |-- package.json
|   |-- vite.config.js
|
|-- backend/                        # Python FastAPI Backend
|   |-- app/
|   |   |-- api/                    # REST route controllers (auth, disease, crop,
|   |   |                           # fertilizers, weather, admin, expert)
|   |   |-- core/                   # Configuration (pydantic-settings), JWT security
|   |   |-- database/               # Motor MongoDB async client & index management
|   |   |-- middleware/             # Role-based access control & Bearer token guard
|   |   |-- models/                 # Collection models
|   |   |-- schemas/                # Pydantic v2 validation schemas
|   |   |-- services/               # Modular service interfaces (CNN, Crop, Weather, Fert)
|   |   |-- main.py                 # FastAPI application factory & static mounting
|   |-- tests/                      # Automated Pytest test suite
|   |-- uploads/                    # Local storage for uploaded leaf pathology images
|   |-- requirements.txt
|   |-- .env.example
|
|-- ml/                             # Machine Learning Interfaces & Storage
|   |-- disease_detection/          # CNN model interface & labels.json
|   |-- crop_recommendation/        # Random Forest / XGBoost interface
|   |-- datasets/                   # Training splits and agronomic datasets documentation
|   |-- saved_models/               # Directory for .h5, .keras, .pkl weight artifacts
|
|-- README.md
|-- .gitignore
```

---

## 🚀 Quickstart Installation Guide

### Prerequisites

- **Node.js**: v18.0.0 or higher (v22+ recommended)
- **Python**: v3.10 to v3.14+
- **MongoDB**: Local MongoDB instance (`mongodb://localhost:27017`) or free MongoDB Atlas cluster connection string. _(Note: Backend includes in-memory fallback for local development if MongoDB is offline)._

---

### Step 1: Set Up Backend

1. Navigate to the `backend/` directory:

   ```bash
   cd backend
   ```

2. Create and activate a Python virtual environment:

   ```bash
   # Windows PowerShell
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:

   ```bash
   cp .env.example .env
   ```

   _(Optionally add your `OPENWEATHER_API_KEY` or MongoDB Atlas URI in `.env`)._

5. Run the FastAPI server:

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   - **Interactive API Docs (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **Alternative Docs (ReDoc)**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
   - **Health Endpoint**: [http://localhost:8000/api/health](http://localhost:8000/api/health)

6. Run automated test suite:
   ```bash
   pytest tests/test_api.py -v
   ```

---

### Step 2: Set Up Frontend

1. In a separate terminal, navigate to `frontend/`:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 🔑 One-Click Evaluator Roles

On the Login screen (`/login`), click any of the **1-Click Evaluator** buttons to test role-based access immediately:

| Role                   | Demo Email              | Password    | Access Capabilities                                                             |
| ---------------------- | ----------------------- | ----------- | ------------------------------------------------------------------------------- |
| **Farmer**             | `farmer@agrisaathi.org` | `farmer123` | Farmer Dashboard, Disease Scan, Crop Recommender, Fertilizer Compare, Weather   |
| **Agriculture Expert** | `expert@agrisaathi.org` | `expert123` | Expert Verification Hub, Pending Pathology Queue, Clinical Diagnosis Submission |
| **System Admin**       | `admin@agrisaathi.org`  | `admin123`  | System Operations Dashboard, User Directory, Product Catalog Management         |

---

