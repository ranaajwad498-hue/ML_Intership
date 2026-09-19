# NourishPak Admin Dashboard

A React-based admin dashboard for the NourishPak child nutrition monitoring system.

This version is **frontend only**. It uses static sample data and does not connect to the FastAPI backend yet. The goal is to understand React components, props, state, and layout structure before wiring up real APIs.

---

## Table of Contents

1. [What React Is](#1-what-react-is)
2. [Project Setup](#2-project-setup)
3. [Component Structure](#3-component-structure)
4. [Sidebar Component](#4-sidebar-component)
5. [Navbar Component](#5-navbar-component)
6. [DashboardCard Component](#6-dashboardcard-component)
7. [Props](#7-props)
8. [State](#8-state)
9. [Admin Layout](#9-admin-layout)
10. [Dashboard Page](#10-dashboard-page)
11. [Static Sample Data](#11-static-sample-data)
12. [Responsive Design](#12-responsive-design)
13. [How to Run the Application](#13-how-to-run-the-application)

---

## 1. What React Is

React is a JavaScript library for building user interfaces. Instead of writing one long HTML page and manually updating it with DOM code, you describe the UI as a set of **components**, and React updates the screen whenever the underlying data changes.

Three ideas matter most for this project:

**Components.** A component is a JavaScript function that returns markup. It is a reusable piece of UI, like a button, a card, or an entire page.

```jsx
function DashboardCard() {
  return <div>Total Children: 120</div>;
}
```

**JSX.** The HTML-looking syntax above is JSX. It is not HTML — it compiles down to JavaScript function calls. A few differences to remember:

- `class` becomes `className`
- attributes use camelCase: `onclick` becomes `onClick`
- every expression goes inside curly braces: `{value}`
- a component must return one root element (or a `<>...</>` fragment)

**Declarative rendering.** You do not tell React *how* to update the page. You describe what the page should look like for the current data, and React works out the minimum set of DOM changes needed. When data changes, the affected components re-render automatically.

React also uses a **one-way data flow**: data travels from parent components down to children through props. A child never reaches up and modifies its parent directly.

---

## 2. Project Setup

The project uses **Vite**, a fast build tool, plus **Tailwind CSS** for styling.

### Create the project

```bash
npm create vite@latest nourishpak-admin -- --template react
cd nourishpak-admin
npm install
```

### Install Tailwind CSS

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

This creates `tailwind.config.js` and `postcss.config.js`.

### Configure Tailwind

In `tailwind.config.js`, tell Tailwind which files to scan for class names:

```js
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
```

In `src/index.css`, replace everything with the Tailwind directives:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

> **Note on Tailwind v4:** if `npm install -D tailwindcss` pulls version 4, the setup differs — you install `@tailwindcss/vite`, add it as a Vite plugin, and use a single `@import "tailwindcss";` line in your CSS instead of the three directives. Check which version installed with `npx tailwindcss --help` before following either path, and match the official docs for that version.

### Verify

```bash
npm run dev
```

Open the printed local URL. Add `className="text-3xl font-bold text-blue-600"` to something in `App.jsx` — if it styles, Tailwind is working.

---

## 3. Component Structure

Keeping components in separate files is the point of this exercise. Nothing beyond routing and layout assembly should live in `App.jsx`.

```
nourishpak-admin/
├── index.html
├── package.json
├── tailwind.config.js
├── vite.config.js
└── src/
    ├── components/
    │   ├── Sidebar.jsx
    │   ├── Navbar.jsx
    │   ├── DashboardCard.jsx
    │   ├── RiskBadge.jsx
    │   └── SummarySection.jsx
    ├── layouts/
    │   └── AdminLayout.jsx
    ├── pages/
    │   └── Dashboard.jsx
    ├── data/
    │   └── sampleData.js
    ├── App.jsx
    ├── main.jsx
    └── index.css
```

**Why the split matters**

| Folder | Holds | Rule of thumb |
| --- | --- | --- |
| `components/` | Small, reusable pieces | Used in more than one place, or could be |
| `layouts/` | Page shells (sidebar + navbar + slot for content) | Wraps pages, doesn't know what's inside |
| `pages/` | Full screens | One per route |
| `data/` | Static sample data | Will be replaced by API calls later |

**How they nest:**

```
App
└── AdminLayout
    ├── Sidebar
    ├── Navbar
    └── Dashboard (page)
        ├── DashboardCard × 4
        ├── Quick Actions
        ├── Assessments table
        │   └── RiskBadge (per row)
        └── SummarySection
```

---

## 4. Sidebar Component

**File:** `src/components/Sidebar.jsx`

The sidebar holds the app brand and the navigation menu:

- NourishPak (brand)
- Dashboard
- Children
- Predictions
- Health Workers
- Districts
- Users
- Reports
- Logout

**Key technique — render the menu from an array, not by copy-pasting eight `<a>` tags.**

```jsx
const menuItems = [
  "Dashboard",
  "Children",
  "Predictions",
  "Health Workers",
  "Districts",
  "Users",
  "Reports",
];

function Sidebar({ isOpen, activeItem }) {
  return (
    <aside className={`... ${isOpen ? "translate-x-0" : "-translate-x-full"}`}>
      <h1>NourishPak</h1>
      <nav>
        {menuItems.map((item) => (
          <a
            key={item}
            href="#"
            className={item === activeItem ? "bg-blue-600 text-white" : "text-gray-600"}
          >
            {item}
          </a>
        ))}
      </nav>
      <button>Logout</button>
    </aside>
  );
}
```

Two things to notice:

- **`.map()` renders lists.** Any array can become JSX by mapping over it.
- **The `key` prop.** React needs a stable, unique `key` on each item in a list so it can track which element is which between renders. Leaving it out produces a console warning and can cause subtle bugs.

The **active item** is styled differently using a conditional `className`. For now `activeItem` can be a hardcoded string like `"Dashboard"`. When React Router is added later, it will come from the current route instead.

---

## 5. Navbar Component

**File:** `src/components/Navbar.jsx`

The navbar sits at the top of the main content area — not above the sidebar — so the sidebar runs the full height of the screen.

It shows:

- The title: **NourishPak Admin Panel**
- A greeting: **Welcome, Admin**
- The role: **Role: Admin**
- A logout button or profile section
- On mobile: a hamburger button that toggles the sidebar

```jsx
function Navbar({ onMenuClick, adminName, adminRole }) {
  return (
    <header className="flex items-center justify-between bg-white px-6 py-4 shadow">
      <div className="flex items-center gap-3">
        <button onClick={onMenuClick} className="md:hidden">☰</button>
        <h2>NourishPak Admin Panel</h2>
      </div>
      <div>
        <p>Welcome, {adminName}</p>
        <p>Role: {adminRole}</p>
      </div>
    </header>
  );
}
```

The `md:hidden` class hides the hamburger on medium screens and up, because the sidebar is always visible there.

`onMenuClick` is a **function passed down as a prop**. The navbar doesn't know or care what happens when the button is clicked — it just calls what it was given. This is how a child communicates back up to its parent.

---

## 6. DashboardCard Component

**File:** `src/components/DashboardCard.jsx`

One reusable component renders all four statistic cards. Do not write `TotalChildrenCard`, `HighRiskCard`, and so on — that defeats the purpose.

```jsx
function DashboardCard({ title, value, description }) {
  return (
    <div className="rounded-lg bg-white p-6 shadow">
      <p className="text-sm text-gray-500">{title}</p>
      <p className="mt-2 text-3xl font-bold">{value}</p>
      {description && <p className="mt-1 text-xs text-gray-400">{description}</p>}
    </div>
  );
}

export default DashboardCard;
```

Used like this:

```jsx
<DashboardCard title="Total Children" value={120} />
<DashboardCard title="High Risk" value={35} description="Needs urgent attention" />
```

`{description && <p>...</p>}` is **conditional rendering**. If `description` is undefined, nothing renders. This is how you make a prop optional.

### RiskBadge component

**File:** `src/components/RiskBadge.jsx`

Same principle, applied to the table. One component, driven by its prop:

```jsx
const styles = {
  "High Risk":   "bg-red-100 text-red-700",
  "Medium Risk": "bg-yellow-100 text-yellow-700",
  "Low Risk":    "bg-green-100 text-green-700",
};

function RiskBadge({ level }) {
  return (
    <span className={`rounded-full px-3 py-1 text-xs font-medium ${styles[level]}`}>
      {level}
    </span>
  );
}
```

Looking the style up from an object keeps the component short and makes adding a fourth risk level a one-line change.

---

## 7. Props

**Props** (short for properties) are the inputs to a component. The parent passes them in; the child reads them.

```jsx
// Parent passes
<DashboardCard title="High Risk" value={35} />

// Child receives
function DashboardCard({ title, value }) { ... }
```

Rules worth internalising:

**Props flow one direction — down.** A parent can send data to a child. A child cannot change the parent's data directly.

**Props are read-only.** Never do `props.value = 200` inside a component. If a value needs to change, it belongs in state in the parent, which then passes the new value down.

**Strings use quotes, everything else uses braces.**

```jsx
<DashboardCard
  title="Total Children"     {/* string */}
  value={120}                {/* number */}
  isActive={true}            {/* boolean */}
  data={childrenArray}       {/* array */}
  onClick={handleClick}      {/* function */}
/>
```

**Destructuring is the readable form.** These are equivalent, but the second is standard:

```jsx
function Card(props) { return <p>{props.title}</p>; }
function Card({ title }) { return <p>{title}</p>; }
```

**Functions can be props too.** Passing `onMenuClick` to the Navbar lets the child trigger behaviour that the parent controls. This pattern — data down, events up — is the backbone of React.

---

## 8. State

**Props come from outside a component. State lives inside it.** State is data the component owns and can change; when it changes, React re-renders that component.

This project uses state for the mobile sidebar toggle.

```jsx
import { useState } from "react";

function AdminLayout({ children }) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  return (
    <div className="flex">
      <Sidebar isOpen={isSidebarOpen} />
      <div className="flex-1">
        <Navbar onMenuClick={() => setIsSidebarOpen(!isSidebarOpen)} />
        <main>{children}</main>
      </div>
    </div>
  );
}
```

Breaking down `useState`:

```js
const [isSidebarOpen, setIsSidebarOpen] = useState(false);
//     current value    updater function     initial value
```

- `useState(false)` returns a pair: the current value and a function to change it.
- Array destructuring names them. The convention is `x` and `setX`.
- Calling `setIsSidebarOpen(true)` tells React the value changed and the component should re-render.

**Never mutate state directly.** `isSidebarOpen = true` does nothing — React doesn't know about it and won't re-render. Always go through the setter.

**When state changes, children re-render too.** Setting `isSidebarOpen` re-renders `AdminLayout`, which passes a new `isOpen` prop down to `Sidebar`, which slides into view. That is the full loop.

**Where to put state:** in the closest common parent of every component that needs it. Both `Sidebar` (to know if it's open) and `Navbar` (to toggle it) need this value, so it lives in `AdminLayout`, their shared parent. This is called *lifting state up*.

### Props vs state at a glance

| | Props | State |
| --- | --- | --- |
| Comes from | The parent component | Inside the component |
| Can be changed by the component | No | Yes, via the setter |
| Triggers a re-render when changed | Yes (when the parent changes it) | Yes |
| Typical use here | Card title, value, risk level | Sidebar open/closed |

---

## 9. Admin Layout

**File:** `src/layouts/AdminLayout.jsx`

A layout is the reusable shell every admin page sits inside. It owns the sidebar and navbar so each page doesn't have to repeat them.

```
┌──────────┬──────────────────────────────┐
│          │  Navbar                      │
│ Sidebar  ├──────────────────────────────┤
│          │                              │
│          │  Main content (children)     │
│          │                              │
└──────────┴──────────────────────────────┘
```

```jsx
function AdminLayout({ children }) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  return (
    <div className="flex min-h-screen bg-gray-100">
      <Sidebar isOpen={isSidebarOpen} activeItem="Dashboard" />
      <div className="flex flex-1 flex-col">
        <Navbar
          adminName="Admin"
          adminRole="Admin"
          onMenuClick={() => setIsSidebarOpen(!isSidebarOpen)}
        />
        <main className="flex-1 p-6">{children}</main>
      </div>
    </div>
  );
}
```

**`children` is a special prop.** Whatever you nest between a component's opening and closing tags arrives as `children`:

```jsx
// App.jsx
<AdminLayout>
  <Dashboard />   {/* this becomes `children` */}
</AdminLayout>
```

This is what makes the layout reusable. Tomorrow you can wrap `<Children />` or `<Reports />` in the same layout without touching `AdminLayout.jsx`.

---

## 10. Dashboard Page

**File:** `src/pages/Dashboard.jsx`

The page composes everything, top to bottom:

**1. Header**

> **Dashboard**
> Overview of NourishPak child nutrition monitoring system.

**2. Statistic cards** — four `DashboardCard` instances in a responsive grid.

**3. Quick Actions** — Add Child, View Children, Generate Prediction, View Reports. Buttons only; no API calls yet.

**4. Recent Child Assessments** — a table with Child ID, Child Name, Age, District, Risk Category, Assessment Date. The risk column renders a `RiskBadge`.

**5. SummarySection** (bonus) — Total Health Workers: 12, Total Districts: 8, Predictions Today: 18.

**6. Risk Distribution Chart placeholder** — an empty bordered box with a label. No chart library needed yet.

The cards and table rows both come from arrays via `.map()`:

```jsx
{stats.map((stat) => (
  <DashboardCard key={stat.title} title={stat.title} value={stat.value} />
))}
```

```jsx
{assessments.map((child) => (
  <tr key={child.id}>
    <td>{child.id}</td>
    <td>{child.name}</td>
    <td>{child.age}</td>
    <td>{child.district}</td>
    <td><RiskBadge level={child.risk} /></td>
    <td>{child.date}</td>
  </tr>
))}
```

---

## 11. Static Sample Data

**File:** `src/data/sampleData.js`

Keeping sample data in its own file is deliberate: when the backend is ready, you swap this import for an API call and the components don't change at all.

```js
export const stats = [
  { title: "Total Children", value: 120 },
  { title: "High Risk",      value: 35  },
  { title: "Medium Risk",    value: 50  },
  { title: "Low Risk",       value: 35  },
];

export const assessments = [
  { id: 101, name: "Ahmed",  age: "18 Months", district: "Mardan",   risk: "High Risk",   date: "10-09-2026" },
  { id: 102, name: "Ayesha", age: "24 Months", district: "Peshawar", risk: "Low Risk",    date: "10-09-2026" },
  { id: 103, name: "Bilal",  age: "30 Months", district: "Swabi",    risk: "Medium Risk", date: "09-09-2026" },
];

export const summary = {
  healthWorkers: 12,
  districts: 8,
  predictionsToday: 18,
};
```

Note that the numbers are internally consistent: 35 + 50 + 35 = 120. Worth keeping that way so the dashboard doesn't look obviously fake during a demo.

All of this data is fictional and used for UI practice only.

---

## 12. Responsive Design

Tailwind is mobile-first: an unprefixed class applies at every size, and a prefixed class like `md:` applies at that breakpoint **and above**.

| Prefix | Applies from |
| --- | --- |
| *(none)* | all sizes |
| `sm:` | 640px |
| `md:` | 768px |
| `lg:` | 1024px |
| `xl:` | 1280px |

### Cards: fewer columns on smaller screens

```jsx
<div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
```

One column on mobile, two on tablet, four on desktop.

### Sidebar: collapses on mobile

```jsx
<aside className={`
  fixed inset-y-0 left-0 z-30 w-64 transform transition-transform
  md:static md:translate-x-0
  ${isOpen ? "translate-x-0" : "-translate-x-full"}
`}>
```

Below `md`, the sidebar is fixed-position and slides off-screen unless `isOpen` is true. At `md` and above, `md:static md:translate-x-0` pins it permanently in the flow and the toggle stops mattering.

### Table: scrolls horizontally instead of squashing

```jsx
<div className="overflow-x-auto">
  <table className="min-w-full">...</table>
</div>
```

`min-w-full` keeps columns at a readable width and the wrapper scrolls sideways rather than cramming six columns into 360px.

Test by resizing the browser window or using the device toolbar in DevTools. Perfect mobile polish is not the goal here — understanding how the pieces reflow is.

---

## 13. How to Run the Application

### Requirements

- Node.js 18 or newer — check with `node -v`
- npm (ships with Node)

### Install and start

```bash
cd nourishpak-admin
npm install
npm run dev
```

Vite prints a local URL, usually `http://localhost:5173`. Open it in a browser. Saving a file refreshes the page automatically.

### Available commands

| Command | What it does |
| --- | --- |
| `npm install` | Installs dependencies from `package.json` |
| `npm run dev` | Starts the dev server with hot reload |
| `npm run build` | Builds the production bundle into `dist/` |
| `npm run preview` | Serves the built `dist/` folder locally |

### Common problems

**Tailwind classes have no effect.** Check the `content` array in `tailwind.config.js` covers `./src/**/*.{js,jsx}`, that `index.css` has the Tailwind directives, and that `main.jsx` imports `./index.css`. Restart the dev server after editing the config.

**Port 5173 already in use.** Vite will pick the next free port automatically; read the URL it prints. Or run `npm run dev -- --port 3000`.

**`Failed to resolve import`.** Check the path and the file extension in your import — `./components/Sidebar` must match the actual filename, including capitalisation. This bites on Linux and in CI even when it works on Windows or macOS.

**Blank page, error in console.** Nearly always a missing `export default` at the bottom of a component file.

---

## What Comes Next

- **React Router** to make the sidebar links navigate between real pages
- **Replace static data with FastAPI calls** using `fetch` or `axios` inside `useEffect`
- **Loading and error states** for each request
- **Authentication** so the admin name and role come from a real session
- **A chart library** (Recharts or Chart.js) to fill the Risk Distribution placeholder