import { Routes, Route, Navigate } from "react-router-dom";
import AdminLayout from "./layout/AdminLayout";
import Dashboard from "./pages/Dashboard";
import AddChild from "./pages/AddChild";
import PredictionResult from "./components/PredictionResult";

function App() {
  return (
    <Routes>
      <Route path="/" element={<AdminLayout />}>
        <Route index element={<Dashboard />} />
        <Route path="children" element={<AddChild />} />
        <Route path="predictions" element={<PredictionResult />} />
      </Route>
    </Routes>
  );
}

export default App;