import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { ArrowLeft, CheckCircle, Loader2, Sparkles, UserPlus } from "lucide-react";
import ChildForm from "../components/ChildForm";
import PredictionResult from "../components/PredictionResult";

/**
 * AddChild Page
 * -------------
 * Full flow:
 *  1. Admin/Health Worker fills ChildForm
 *  2. POST /children  →  child saved in PostgreSQL, ID returned
 *  3. Click "Generate Prediction"
 *  4. POST /children/{id}/predict  →  ML result
 *  5. PredictionResult component shows it
 */

// -------- TEMPORARY dummy data (replace with API later) --------
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
// ----------------------------------------------------------------

const AddChild = () => {
  const navigate = useNavigate();

  // Registered child info (returned by backend)
  const [childId, setChildId] = useState(null);
  const [childName, setChildName] = useState("");

  // Prediction result (returned by backend)
  const [prediction, setPrediction] = useState(null);

  // Loading + error states
  const [registering, setRegistering] = useState(false);
  const [predicting, setPredicting] = useState(false);
  const [error, setError] = useState("");
  const [successMsg, setSuccessMsg] = useState("");

  // -------- Step 9: POST /children --------
  const handleRegisterChild = async (formData) => {
    setError("");
    setSuccessMsg("");
    setPrediction(null);
    setRegistering(true);

    try {
      // TODO: replace with real Axios call
      // const res = await api.post("/children", formData);
      // const { id, name } = res.data;

      // ---- MOCK response for now ----
      await new Promise((r) => setTimeout(r, 800));
      const mockResponse = { id: 101, name: formData.name };
      // --------------------------------

      setChildId(mockResponse.id);
      setChildName(mockResponse.name);
      setSuccessMsg(
        `Child Registered Successfully. Child ID: ${mockResponse.id}`
      );
    } catch (err) {
      setError("Unable to register child. Please check the entered information.");
    } finally {
      setRegistering(false);
    }
  };

  // -------- Step 13: POST /children/{id}/predict --------
  const handleGeneratePrediction = async () => {
    if (!childId) return;

    setError("");
    setPredicting(true);

    try {
      // TODO: replace with real Axios call
      // const res = await api.post(`/children/${childId}/predict`);
      // setPrediction(res.data);

      // ---- MOCK response for now ----
      await new Promise((r) => setTimeout(r, 800));
      setPrediction({
        risk_score: 76,
        category: "High Risk",
        confidence: 76,
        advice: "Refer child for nutrition support and further assessment.",
      });
      // --------------------------------
    } catch (err) {
      setError("Unable to generate prediction. Please try again.");
    } finally {
      setPredicting(false);
    }
  };

  // -------- Bonus: Reset for another child --------
  const handleRegisterAnother = () => {
    setChildId(null);
    setChildName("");
    setPrediction(null);
    setError("");
    setSuccessMsg("");
    // Force ChildForm to re-mount with blank fields
    window.location.reload();
  };

  return (
    <div>
      {/* Header */}
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

      {/* Global error */}
      {error && (
        <div className="mb-5 px-4 py-3 rounded-lg bg-red-50 border border-red-200 text-sm text-red-700">
          {error}
        </div>
      )}

      {/* Success banner */}
      {successMsg && (
        <div className="mb-5 flex items-center gap-2 px-4 py-3 rounded-lg bg-emerald-50 border border-emerald-200 text-sm text-emerald-700">
          <CheckCircle size={16} />
          {successMsg}
        </div>
      )}

      {/* Form (only shows when no child registered yet) */}
      {!childId && (
        <ChildForm
          onSubmit={handleRegisterChild}
          loading={registering}
          districts={dummyDistricts}
          healthWorkers={dummyHealthWorkers}
        />
      )}

      {/* After successful registration → Prediction section */}
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

      {/* Prediction result */}
      {prediction && (
        <>
          <PredictionResult
            childName={childName}
            riskScore={prediction.risk_score}
            category={prediction.category}
            confidence={prediction.confidence}
            advice={prediction.advice}
          />

          {/* Bonus actions */}
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