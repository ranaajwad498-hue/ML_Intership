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

```

Nothing in the frontend invents a child ID or a prediction result — both
always come from the backend response.

## Project structure

```
src/
  api/
    api.js                Axios instance, JWT header, error normalization
  components/
    ChildForm.jsx          Form fields, state, client-side validation
    DashboardCard.jsx
    Navbar.jsx
    FormInput.jsx           Generic labeled input/select with error display
    PredictionResult.jsx    Renders the backend's prediction response
    Sidebar.jsx
  layout/
      AdminLayosut.jsx
  pages/
    AddChild.jsx            Orchestrates register -> predict -> display
    Dashboard.jsx
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

## Setup

```bash
npm install
cp .env.example .env   # adjust VITE_API_URL if your backend runs elsewhere
npm run dev
```

Tailwind is already configured (`tailwind.config.js`, `postcss.config.js`,
`src/index.css`) — no extra setup needed beyond `npm install` and
importing `./index.css` once in `main.jsx`. If Tailwind isn't already set
up elsewhere in your existing project, this brings it in cleanly.

Requires the FastAPI backend running (default `http://localhost:8000`)
with CORS configured to allow the Vite dev origin (default
`http://localhost:5173`).

## Authentication

The app expects a JWT already stored in `localStorage` under
`nourishpak_token` after a successful login (Day 20/24 login flow).
`api.js` attaches it as `Authorization: Bearer <token>` on every request
and clears it on a 401 response.

**Note on production hardening:** storing a long-lived token in
`localStorage` is convenient for this learning project but is readable by
any script running on the page. Production deployments typically issue
the JWT (or a session identifier) inside an `HttpOnly`, `Secure` cookie
instead, so client-side JavaScript never has direct access to it.

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