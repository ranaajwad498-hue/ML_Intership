import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { ArrowLeft, CheckCircle, Loader2, Sparkles, UserPlus } from "lucide-react";
import ChildForm from "../components/ChildForm";
import PredictionResult from "../components/PredictionResult";
import api from "../api/api";

const dummyDistricts = [
  { id: 1, name: "Mardan" },
  { id: 2, name: "Peshawar" },
  { id: 3, name: "Swabi" },
];

const dummyHealthWorkers = [
  { id: 1, name: "Dr. Sara Khan" },
  { id: 2, name: "Mr. Imran Ali" },
  { id: 3, name: "Ms. Hina Yousaf" },
];

const AddChild = () => {
  const navigate = useNavigate();

  const [childId, setChildId] = useState(null);
  const [childName, setChildName] = useState("");

  const [prediction, setPrediction] = useState(null);

  const [registering, setRegistering] = useState(false);
  const [predicting, setPredicting] = useState(false);
  const [error, setError] = useState("");
  const [successMsg, setSuccessMsg] = useState("");

const handleRegisterChild = async (formData) => {
  setError("");
  setSuccessMsg("");
  setPrediction(null);
  setRegistering(true);

  try {
    const res = await api.post("/add_child", formData);

    const savedChild = res.data;

    setChildId(savedChild.id);
    setChildName(savedChild.name);
    setSuccessMsg(
      `Child Registered Successfully. Child ID: ${savedChild.id}`
    );
  } catch (err) {
    console.error("Register error:", err);

    if (!err.response) {
      setError("Cannot reach server. Please check your connection.");
    } else if (err.response.status === 401) {
      setError("Session expired. Please login again.");
    } else if (err.response.status === 422) {
      setError("Please check the entered information.");
    } else {
      setError("Unable to register child. Please try again.");
    }
  } finally {
    setRegistering(false);
  }
};

const handleGeneratePrediction = async () => {
  if (!childId) return;

  setError("");
  setPredicting(true);

  try {
    const res = await api.post(`/children/${childId}/predict`);
    setPrediction(res.data);
  } catch (err) {
    console.error("Predict error:", err);

    if (!err.response) {
      setError("Cannot reach server. Please check your connection.");
    } else if (err.response.status === 404) {
      setError("Child not found.");
    } else {
      setError("Unable to generate prediction. Please try again.");
    }
  } finally {
    setPredicting(false);
  }
};
  const handleRegisterAnother = () => {
    setChildId(null);
    setChildName("");
    setPrediction(null);
    setError("");
    setSuccessMsg("");
    window.location.reload();
  };

  return (
    <div>
      <div className="mb-6 flex items-start gap-3">
        <button
          onClick={() => navigate(-1)}
          className="p-2 rounded-lg text-slate-600 hover:bg-slate-200 transition-colors"
          aria-label="Back"
        >
          <ArrowLeft size={18} />
        </button>
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Add Child</h1>
          <p className="text-sm text-slate-500 mt-1">
            Register a new child and generate a nutrition risk prediction.
          </p>
        </div>
      </div>


      {error && (
        <div className="mb-5 px-4 py-3 rounded-lg bg-red-50 border border-red-200 text-sm text-red-700">
          {error}
        </div>
      )}

      {successMsg && (
        <div className="mb-5 flex items-center gap-2 px-4 py-3 rounded-lg bg-emerald-50 border border-emerald-200 text-sm text-emerald-700">
          <CheckCircle size={16} />
          {successMsg}
        </div>
      )}
      {!childId && (
        <ChildForm
          onSubmit={handleRegisterChild}
          loading={registering}
          districts={dummyDistricts}
          healthWorkers={dummyHealthWorkers}
        />
      )}
      {childId && (
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <div className="flex items-center gap-2 mb-4">
            <UserPlus size={18} className="text-emerald-600" />
            <h2 className="text-base font-semibold text-slate-800">
              Child Registered — ID {childId}
            </h2>
          </div>

          {!prediction && (
            <button
              onClick={handleGeneratePrediction}
              disabled={predicting}
              className="
                inline-flex items-center gap-2 px-5 py-2.5 rounded-lg
                text-sm font-medium text-white bg-violet-600
                hover:bg-violet-700 transition-colors shadow-sm
                disabled:opacity-60 disabled:cursor-not-allowed
              "
            >
              {predicting ? (
                <>
                  <Loader2 size={16} className="animate-spin" />
                  Generating Prediction...
                </>
              ) : (
                <>
                  <Sparkles size={16} />
                  Generate Prediction
                </>
              )}
            </button>
          )}
        </div>
      )}

      {prediction && (
        <>
          <PredictionResult
            childName={childName}
            riskScore={prediction.risk_score}
            category={prediction.category}
            confidence={prediction.confidence}
            advice={prediction.advice}
          />

      
          <div className="flex flex-col sm:flex-row gap-3 mt-6">
            <button
              onClick={handleRegisterAnother}
              className="
                inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg
                text-sm font-medium text-slate-700 bg-white border border-slate-300
                hover:bg-slate-50 transition-colors
              "
            >
              Register Another Child
            </button>

            <button
              onClick={() => navigate(`/children/${childId}`)}
              className="
                inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg
                text-sm font-medium text-white bg-emerald-600 hover:bg-emerald-700
                transition-colors shadow-sm
              "
            >
              View Child Profile
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default AddChild;