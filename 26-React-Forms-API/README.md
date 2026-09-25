# task-24-react-forms-api — Child Registration Form

React frontend for the NourishPak Child Registration flow, connected to
the FastAPI + PostgreSQL backend and the ML risk-prediction endpoint
built in earlier tasks.

## Flow

```
React Form (ChildForm.jsx)
   |  Axios (api/api.js) — Authorization: Bearer <JWT>
   v
FastAPI  POST /children
   v
PostgreSQL (child row created, id returned)
   |
   v
React stores child_id in state (AddChild.jsx)
   |  user clicks "Generate Prediction"
   v
FastAPI  POST /children/{child_id}/predict
   v
ML model runs on the stored child data, risk score is computed and saved
   v
Prediction JSON returned to React
   v
PredictionResult.jsx renders risk_score / risk_category / confidence / advice
```

Nothing in the frontend invents a child ID or a prediction result — both
always come from the backend response.

## How it works

### React form structure

The registration UI is split into three layers, each with one job:

- **`FormInput.jsx`** — a "dumb" presentational field. It renders either
  an `<input>` or a `<select>` (when an `options` array is passed), shows
  a label, and shows an inline error string if one is passed in. It holds
  no state of its own — it only reflects the `value` prop and calls
  `onChange` upward.
- **`ChildForm.jsx`** — owns the seven form fields (name, age, gender,
  weight, height, district, health worker), runs client-side validation,
  and loads district / health-worker dropdown options. It calls the
  `onSubmit` prop with a clean, typed payload once validation passes. It
  does **not** know how to talk to the backend.
- **`AddChild.jsx`** (the page) — owns the network calls. It passes
  `handleRegister` into `ChildForm` as `onSubmit`, and separately renders
  `PredictionResult` once a prediction comes back.

This separation means `ChildForm` can be reused later (e.g. an "Edit
Child" page) without dragging along the registration/prediction network
logic, and the network logic in `AddChild.jsx` can be tested or modified
without touching field markup.

### `useState()`

Every piece of UI state is a separate `useState` call rather than one
giant object, so a change in one thing doesn't force unrelated re-renders
or make bugs harder to trace:

```js
// ChildForm.jsx — the fields themselves
const [formData, setFormData] = useState(EMPTY_FORM); // { name, age_months, gender, ... }
const [errors, setErrors] = useState({});               // { name: "Child name is required." }
const [districts, setDistricts] = useState(FALLBACK_DISTRICTS);

// AddChild.jsx — everything about the request lifecycle
const [registeredChild, setRegisteredChild] = useState(null); // { id, name } from the backend
const [prediction, setPrediction] = useState(null);            // backend prediction JSON
const [registering, setRegistering] = useState(false);         // loading flag
const [registerError, setRegisterError] = useState("");        // user-facing error text
```

`formData` is a single object (not one `useState` per field) because the
fields are updated the same way and submitted together:

```js
function handleChange(event) {
  const { name, value } = event.target;
  setFormData((prev) => ({ ...prev, [name]: value })); // spread + overwrite one key
}
```

Every `<input>`/`<select>` shares this one `handleChange`, matched to the
right key in `formData` via its `name` attribute — that's why `name="age_months"`
on the JSX element has to exactly match the key in `formData`/the backend
payload.

### Form validation

`validate(formData)` in `ChildForm.jsx` is a plain function — not a
library — that returns an `errors` object:

```js
function validate(formData) {
  const errors = {};
  if (!formData.name.trim()) errors.name = "Child name is required.";
  if (formData.age_months === "" || Number(formData.age_months) < 0)
    errors.age_months = "Age in months cannot be negative.";
  if (formData.weight_kg === "" || Number(formData.weight_kg) <= 0)
    errors.weight_kg = "Weight must be greater than 0.";
  // ...height, gender, district, health_worker follow the same pattern
  return errors;
}
```

`handleSubmit` runs it before calling `onSubmit`, and bails out if
anything failed:

```js
const validationErrors = validate(formData);
setErrors(validationErrors);
if (Object.keys(validationErrors).length > 0) return; // no request is sent
```

Each `FormInput` receives its own `errors.<fieldName>` and renders it
directly under that field, so the user sees exactly which field is wrong
rather than one generic banner. Editing a field clears only *that*
field's error (`setErrors((prev) => ({ ...prev, [name]: undefined }))`),
so fixing one mistake doesn't hide the others.

**This validation is a UX convenience only.** It stops obviously-bad
requests from leaving the browser, but the FastAPI backend must repeat
the same checks (via Pydantic models / DB constraints), because a
malicious or buggy client can always send a raw HTTP request that skips
the React form entirely.

### Axios configuration

All backend calls go through one shared instance in `src/api/api.js`
instead of every component calling `axios.get(...)` with a hardcoded
URL:

```js
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
  headers: { "Content-Type": "application/json" },
});
```

Two interceptors run around every request:

- **Request interceptor** — reads the JWT from `localStorage` and adds
  `Authorization: Bearer <token>` to every outgoing request automatically,
  so `ChildForm`/`AddChild` never have to think about auth headers.
- **Response interceptor** — inspects failures and attaches a
  `err.friendlyMessage` string (network failure, 401, 404, 5xx, or
  validation) so every component can show the same wording without
  re-implementing the same `if/else` chain.

Components then just do `api.post("/children", payload)` — the base URL,
content type, and auth header are all handled in one place.

### Environment variables

The backend URL is **not** hardcoded in components. Vite exposes any
variable prefixed `VITE_` on `import.meta.env`:

```
# .env.example → copy to .env
VITE_API_URL=http://localhost:8000
```

```js
// api.js
const baseURL = import.meta.env.VITE_API_URL || "http://localhost:8000";
```

This means switching between local dev, staging, and production only
requires a different `.env` file (or CI-injected variable) — never a
code change. `.env` itself is git-ignored; only `.env.example`
(no secrets, just the variable name) is committed.

### JWT authentication

Flow: **Login → JWT issued by FastAPI → stored in `localStorage` as
`nourishpak_token` → Axios request interceptor reads it → sent as
`Authorization: Bearer <token>` → FastAPI verifies it on protected
routes.**

```js
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("nourishpak_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
```

If the backend responds `401 Unauthorized` (missing/expired token), the
response interceptor clears the stored token and sets a friendly
"Session expired. Please login again." message, rather than leaving a
dead token in storage.

**Why not just leave it there permanently?** Storing a long-lived JWT in
`localStorage` is simple for a learning project, but it's readable by
any JavaScript running on the page — including a malicious script
injected via an XSS bug. Production apps commonly avoid this by having
the backend set the token inside an `HttpOnly`, `Secure` cookie instead:
the browser still sends it automatically with each request, but no
client-side JS (including a compromised third-party script) can ever
read or exfiltrate it.

### CORS

React (`http://localhost:5173`, Vite's default) and FastAPI
(`http://localhost:8000`) are different origins, so the browser blocks
the request unless FastAPI explicitly allows it. On the backend:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # add your deployed frontend URL too
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Only list the origins you actually need (dev URL, and later your real
frontend domain) — `allow_origins=["*"]` is convenient locally but should
never ship to production, since it lets *any* website make authenticated
requests to your API.

### Child registration API

Triggered from `handleRegister` in `AddChild.jsx` when `ChildForm` calls
`onSubmit` with a validated, typed payload:

```js
const response = await api.post("/children", childPayload);
setRegisteredChild({ id: response.data.id, name: childPayload.name });
```

The child's `id` is **only** ever taken from `response.data.id` — React
never invents or increments an ID itself. That returned ID is what gets
used in the next step (the predict call) and in the "View Child Profile"
link.

### Prediction API

Only enabled once a child is registered (`registeredChild` is set).
Clicking **Generate Prediction** calls:

```js
const response = await api.post(`/children/${registeredChild.id}/predict`);
setPrediction(response.data);
```

`PredictionResult.jsx` then renders whatever comes back
(`risk_score`, `risk_category`, `confidence`, `advice`) — the component
returns `null` if `prediction` hasn't arrived yet, and it never
hardcodes a score or category string.

### Loading state

Two independent boolean flags track "is a request in flight" —
`registering` for the registration call, `predicting` for the prediction
call:

```js
async function handleRegister(childPayload) {
  if (registering) return;      // ← blocks a second click while one is pending
  setRegistering(true);
  try {
    // ...
  } finally {
    setRegistering(false);      // always resets, success or failure
  }
}
```

The button reflects this directly:

```jsx
<button disabled={registering}>
  {registering ? "Registering..." : "Register Child"}
</button>
```

The `if (registering) return;` guard is what actually prevents a
double-click from firing two requests — `disabled` alone only prevents
it once React has re-rendered, which isn't always fast enough for a very
quick double click.

### Error handling

Errors are handled at two levels:

1. **Axios response interceptor** (`api.js`) turns raw HTTP/network
   failures into one `err.friendlyMessage` string per case (network
   unreachable, 401, 404, 5xx, validation/4xx) — see the CORS/JWT
   sections above.
2. **Component-level `catch` blocks** (`AddChild.jsx`) store that message
   in state and render it in a banner:

```js
try {
  const response = await api.post("/children", childPayload);
  // ...
} catch (err) {
  setRegisterError(
    err.friendlyMessage || "Unable to register child. Please check the entered information."
  );
}
```

The raw Axios error (stack trace, backend internals) is never rendered —
only the short, friendly string. This keeps the UI helpful without
leaking implementation details to the end user.

### Sample request / response

**Register a child**

```
POST /children
Authorization: Bearer <jwt>
Content-Type: application/json

{
  "name": "Ahmed Ali",
  "age_months": 18,
  "gender": "Male",
  "weight_kg": 7.8,
  "height_cm": 74,
  "district_id": 1,
  "health_worker_id": 2
}
```

```json
HTTP/1.1 201 Created

{
  "id": 101,
  "name": "Ahmed Ali",
  "age_months": 18,
  "gender": "Male",
  "weight_kg": 7.8,
  "height_cm": 74,
  "district_id": 1,
  "health_worker_id": 2
}
```

**Generate a prediction**

```
POST /children/101/predict
Authorization: Bearer <jwt>
```

```json
HTTP/1.1 200 OK

{
  "child_id": 101,
  "risk_score": 76,
  "risk_category": "High Risk",
  "confidence": 76,
  "advice": "Refer child for nutrition support and further assessment."
}
```

**Validation failure example**

```json
HTTP/1.1 422 Unprocessable Entity

{
  "detail": [
    { "loc": ["body", "weight_kg"], "msg": "ensure this value is greater than 0" }
  ]
}
```

The React side reads `error.response.data.detail` (via `err.friendlyMessage`)
and shows it as a banner rather than the raw array shown above.

### Complete frontend-to-backend flow

```
1. User logs in                → FastAPI issues JWT      → stored in localStorage
2. User opens Add Child        → ChildForm loads district/health-worker options
3. User fills form, submits    → validate() runs in the browser
4. If valid → Axios POST /children, with Authorization: Bearer <jwt>
5. FastAPI validates again (Pydantic), inserts a row in PostgreSQL
6. PostgreSQL returns the new row's id → FastAPI responds 201 with it
7. React stores { id, name } in `registeredChild` state
8. User clicks "Generate Prediction" → Axios POST /children/{id}/predict
9. FastAPI loads the child row, builds ML features, runs the model
10. FastAPI saves the prediction row, responds with risk_score/category/confidence/advice
11. React stores the response in `prediction` state
12. PredictionResult renders it — nothing here is hardcoded
13. User can click "Register Another Child" (resets all state) or
    "View Child Profile" (navigates to /children/{id})
```

Every arrow above is a real HTTP call or a real state update — there's no
step where React fabricates data that should have come from the backend.

### How to run React and FastAPI together

1. **Start PostgreSQL** (however your existing setup runs it, e.g.
   `docker compose up db` or a local service).
2. **Start FastAPI**, from the backend project:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   Confirm CORS is configured for `http://localhost:5173` (see the CORS
   section above) and that `/children`, `/children/{id}/predict`, and
   ideally `/districts` / `/health-workers` are reachable at
   `http://localhost:8000`.
3. **Start React**, from this project:
   ```bash
   npm install
   cp .env.example .env      # confirm VITE_API_URL=http://localhost:8000
   npm run dev
   ```
   Vite serves the app at `http://localhost:5173`.
4. **Log in** through your existing auth flow so a JWT lands in
   `localStorage` under `nourishpak_token` — the Add Child page requires
   it for every request.
5. **Open Add Child**, fill the form, and register a child; the browser's
   Network tab should show the `Authorization` header on the
   `POST /children` request, and a `POST /children/{id}/predict` request
   once you click Generate Prediction.

If step 5 fails with a CORS error in the browser console, double-check
step 2's `allow_origins` list matches the exact origin shown in the
error. If it fails with a connection error, confirm FastAPI is actually
running on the port `VITE_API_URL` points at.

## Project structure

```
src/
  api/
    api.js                Axios instance, JWT header, error normalization
  components/
    ChildForm.jsx          Form fields, state, client-side validation
    FormInput.jsx           Generic labeled input/select with error display
    PredictionResult.jsx    Renders the backend's prediction response
  pages/
    AddChild.jsx            Orchestrates register -> predict -> display
  index.css                 Tailwind directives (imported once in main.jsx)
tailwind.config.js
postcss.config.js
```

Styling uses Tailwind utility classes directly in JSX — there are no
per-component `.css` files. Make sure `src/index.css` is imported once in
your `main.jsx`:

```js
import "./index.css";
```

`ChildForm` is intentionally decoupled from the register/predict network
calls, which live in `AddChild.jsx`. That keeps the form reusable for a
future "edit child" screen that has no prediction step.

Tailwind is already configured (`tailwind.config.js`, `postcss.config.js`,
`src/index.css`) — no extra setup needed beyond `npm install` and
importing `./index.css` once in `main.jsx`. See "How to run React and
FastAPI together" above for the full setup sequence, and "JWT
authentication" above for how the login token is stored and used.

## Districts and health workers

- If the backend exposes `GET /districts` (and `GET /health-workers`),
  the form fetches and displays them in the dropdowns.
- If those endpoints are not live yet, the form falls back to a small
  hardcoded list (clearly labeled `(temporary)` in the UI and with a
  `TODO` comment in `ChildForm.jsx`) so the rest of the flow can still be
  tested end to end. Replace these once the endpoints exist.

## Manual test checklist

**Happy path**
1. Start PostgreSQL, FastAPI, then `npm run dev`.
2. Log in and confirm a JWT is stored.
3. Open Add Child, fill in valid data, click **Register Child**.
4. Confirm the "Child Registered Successfully — Child ID: N" banner.
5. Click **Generate Prediction** and confirm the risk score/category/
   confidence/advice render from the backend response.
6. Confirm the child and prediction rows exist in PostgreSQL.

**Failure cases**
| Case | Action | Expected |
|---|---|---|
| 1 | Submit with empty name | Inline validation error, no request sent |
| 2 | Submit with weight = -5 | Inline validation error, no request sent |
| 3 | Clear the JWT, then submit | Backend returns 401 → "Session expired. Please login again." |
| 4 | Call predict on a non-existent child id | Backend returns 404 → friendly "not found" message |
| 5 | Stop the FastAPI server, then submit | "Unable to reach the server..." message, no crash |
| 6 | Double-click **Register Child** | Button disables immediately; only one POST is sent |

## Not included in this task

- `Sidebar.jsx` / `Navbar.jsx` / `AdminLayout.jsx` / `Dashboard.jsx` wiring
  — this deliverable focuses on the child registration + prediction
  slice. Add the `Children → Add Child` sidebar link in your existing
  `Sidebar.jsx` pointing at the `AddChild` route.
- `/children/:id` profile page — the "View Child Profile" link in
  `AddChild.jsx` points at that route for you to implement next.