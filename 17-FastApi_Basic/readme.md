# NourishPak Prediction API

A FastAPI-based backend service for **NourishPak** — a Child Malnutrition Risk Prediction System. This API is the foundation that will later connect a trained machine learning model to web apps, mobile apps, and other services that need malnutrition risk predictions.

---

## 📌 What is FastAPI?

**FastAPI** is a modern Python web framework used to build APIs quickly and reliably. It's especially popular for machine learning projects because it:

- Is **fast** — built on top of Starlette and Pydantic, with async support.
- **Automatically validates** incoming data (so bad input is caught before it reaches your ML model).
- **Auto-generates interactive documentation** (Swagger UI) — no extra work needed.
- Uses standard Python type hints, making code easy to read and maintain.

In simple terms: FastAPI is what lets our ML model be "called" by other applications over the internet, instead of only running inside a Python script.

---

## 📌 What is a REST API?

A **REST API** (Representational State Transfer) is a common style of building APIs using standard web methods (HTTP verbs) and URLs.

| Method | Purpose | Example in this project |
|--------|---------|--------------------------|
| `GET`  | Retrieve data | Check API health, get project info |
| `POST` | Send data / create something | Send child health data to get a risk prediction |

Each piece of functionality lives at its own URL (called an **endpoint**), and the client (a website, mobile app, or another server) talks to it using these standard methods — no custom protocol needed.

---

## ⚙️ Installing Dependencies

Make sure you have **Python 3.8+** installed. Then install the required packages:

```bash
pip install fastapi uvicorn
```

| Package | Purpose |
|---------|---------|
| `fastapi` | The framework used to define the API and its endpoints |
| `uvicorn` | The server that actually runs the FastAPI app and handles requests |

> Tip: It's best practice to use a virtual environment:
> ```bash
> python -m venv venv
> source venv/bin/activate      # Windows: venv\Scripts\activate
> pip install fastapi uvicorn
> ```

---

## 🚀 Running the Server

From the project directory (where `main.py` is located), run:

```bash
uvicorn main:app --reload
```

- `main` → refers to the `main.py` file
- `app` → the FastAPI instance defined inside it
- `--reload` → automatically restarts the server when code changes (use only during development)

Once running, the server will be available at:

```
http://127.0.0.1:8000
```

---

## 📍 Available Endpoints

| Method | Endpoint | Description |
|--------|-----------|-------------|
| `GET` | `/` | Root endpoint — confirms the API is running |
| `GET` | `/health` | Health check — used to verify the service is alive |
| `GET` | `/project_info` | Returns metadata about the NourishPak project |

More endpoints (e.g. `/predict`) will be added as the ML model is integrated.

---

## 📦 Sample JSON Responses

**`GET /`**
```json
{
  "project": "NourishPak",
  "status": "API running successfully"
}
```

**`GET /health`**
```json
{
  "status": "healthy",
  "service": "NourishPak Prediction API"
}
```

**`GET /project_info`**
```json
{
  "project": "NourishPak",
  "description": "Child Malnutrition Risk Prediction System",
  "api_version": "1.0",
  "ml_enabled": true
}
```
**`GET /model_info`**
```json
{
    "model": "Random Forest",
    "task": "Child Malnutrition Risk Classification",
    "status": "trained",
    "classes": ["Low Risk", "High Risk"]
}
```

---

## 📖 Swagger UI (Interactive Docs)

FastAPI automatically generates interactive API documentation — no extra setup required.

Once the server is running, open:

```
http://127.0.0.1:8000/docs
```

From here you can:
- See every available endpoint and what it expects/returns
- Click **"Try it out"** → **"Execute"** to test endpoints live in the browser
- View request/response schemas without reading the source code

A simpler, read-only version is also available at:

```
http://127.0.0.1:8000/redoc
```

---

## 🔗 How This API Connects to the NourishPak ML Prediction Engine

This API currently exposes basic status and metadata endpoints, but it is designed to grow into the **central bridge** between the NourishPak ML model and the outside world.

**The plan:**

1. **Model integration** — The trained ML model (e.g., a classifier estimating malnutrition risk from child health indicators like age, weight, height, and other factors) will be loaded once when the server starts.
2. **New `/predict` endpoint** — A `POST /predict` endpoint will accept structured input data (validated automatically via a Pydantic schema) and return a risk prediction as JSON.
3. **Client applications** (mobile apps used by health workers, web dashboards, or partner NGO systems) will send data to this API and receive predictions — without needing to know anything about the underlying ML model, Python, or how it was trained.
4. **Scalability** — Because the API is decoupled from the model logic, the model can be retrained or improved over time without requiring changes to the applications that consume it — they'll keep calling the same endpoint.

In short: this API is the **doorway** through which any application — regardless of what language or platform it's built in — will be able to request a malnutrition risk prediction from NourishPak's ML engine.

---

## 🗂️ Project Structure (so far)

```
nourishpak-api/
│
├── main.py           # FastAPI app with defined endpoints
└── README.md          # Project documentation (this file)
```

---

## 🧭 Next Steps

- [ ] Add `/predict` endpoint
- [ ] Integrate trained ML model
- [ ] Add input validation schema (Pydantic model) for prediction data
- [ ] Add error handling for invalid/missing input
- [ ] Add authentication (if needed for production use)
- [ ] Deploy to a hosting platform (e.g., Render, Railway, or AWS)