import { useState } from "react";
import { Loader2, UserPlus, RotateCcw } from "lucide-react";
import FormInput from "./FormInput";

const emptyForm = {
  c_name: "",
  age_months: "",
  gender: "",
  weight_kg: "",
  height_cm: "",
  district_id: "",
  health_worker_id: "",
};

const ChildForm = ({
  onSubmit,
  loading = false,
  districts = [],
  healthWorkers = [],
  initialValues = emptyForm,
  submitLabel = "Register Child",
}) => {
  const [formData, setFormData] = useState(initialValues);
  const [errors, setErrors] = useState({});

  // -------- Handle input changes --------
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));

    // Clear error for this field as the user types
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: "" }));
    }
  };

  // -------- Validate the form --------
  const validate = () => {
    const newErrors = {};

    if (!formData.name.trim()) {
      newErrors.name = "Child name is required.";
    }

    if (formData.age_months === "" || Number(formData.age_months) < 0) {
      newErrors.age_months = "Age must be 0 or greater.";
    }

    if (!formData.gender) {
      newErrors.gender = "Please select a gender.";
    }

    if (formData.weight_kg === "" || Number(formData.weight_kg) <= 0) {
      newErrors.weight_kg = "Weight must be greater than 0.";
    }

    if (formData.height_cm === "" || Number(formData.height_cm) <= 0) {
      newErrors.height_cm = "Height must be greater than 0.";
    }

    if (!formData.district_id) {
      newErrors.district_id = "Please select a district.";
    }

    if (!formData.health_worker_id) {
      newErrors.health_worker_id = "Please select a health worker.";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // -------- Handle submit --------
  const handleSubmit = (e) => {
    e.preventDefault();
    if (loading) return; // prevent double submit

    if (!validate()) return;

    // Convert numeric fields to numbers before sending
    const payload = {
      ...formData,
      age_months: Number(formData.age_months),
      weight_kg: Number(formData.weight_kg),
      height_cm: Number(formData.height_cm),
      district_id: Number(formData.district_id),
      health_worker_id: Number(formData.health_worker_id),
    };

    onSubmit(payload);
  };

  // -------- Reset the form --------
  const handleReset = () => {
    setFormData(initialValues);
    setErrors({});
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 space-y-5"
      noValidate
    >
      {/* Grid: 2 columns on md+ screens */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {/* Name (full width) */}
        <div className="md:col-span-2">
          <FormInput
            label="Child Name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="e.g. Ahmed Ali"
            error={errors.name}
            required
          />
        </div>

        {/* Age */}
        <FormInput
          label="Age (Months)"
          name="age_months"
          type="number"
          value={formData.age_months}
          onChange={handleChange}
          placeholder="e.g. 18"
          error={errors.age_months}
          min={0}
          required
        />

        {/* Gender */}
        <FormInput
          label="Gender"
          name="gender"
          type="select"
          value={formData.gender}
          onChange={handleChange}
          error={errors.gender}
          required
          options={[
            { value: "", label: "Select Gender" },
            { value: "Male", label: "Male" },
            { value: "Female", label: "Female" },
          ]}
        />

        {/* Weight */}
        <FormInput
          label="Weight (KG)"
          name="weight_kg"
          type="number"
          step="0.1"
          value={formData.weight_kg}
          onChange={handleChange}
          placeholder="e.g. 7.8"
          error={errors.weight_kg}
          min={0}
          required
        />

        {/* Height */}
        <FormInput
          label="Height (CM)"
          name="height_cm"
          type="number"
          step="0.1"
          value={formData.height_cm}
          onChange={handleChange}
          placeholder="e.g. 74"
          error={errors.height_cm}
          min={0}
          required
        />

        {/* District */}
        <FormInput
          label="District"
          name="district_id"
          type="select"
          value={formData.district_id}
          onChange={handleChange}
          error={errors.district_id}
          required
          options={[
            { value: "", label: "Select District" },
            ...districts.map((d) => ({ value: d.id, label: d.name })),
          ]}
        />

        {/* Health Worker */}
        <FormInput
          label="Health Worker"
          name="health_worker_id"
          type="select"
          value={formData.health_worker_id}
          onChange={handleChange}
          error={errors.health_worker_id}
          required
          options={[
            { value: "", label: "Select Health Worker" },
            ...healthWorkers.map((w) => ({ value: w.id, label: w.name })),
          ]}
        />
      </div>

      {/* Action buttons */}
      <div className="flex flex-col sm:flex-row justify-end gap-3 pt-2 border-t border-slate-100">
        <button
          type="button"
          onClick={handleReset}
          disabled={loading}
          className="
            flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg
            text-sm font-medium text-slate-700 border border-slate-300
            hover:bg-slate-50 transition-colors
            disabled:opacity-50 disabled:cursor-not-allowed
          "
        >
          <RotateCcw size={16} />
          Reset
        </button>

        <button
          type="submit"
          disabled={loading}
          className="
            flex items-center justify-center gap-2 px-5 py-2.5 rounded-lg
            text-sm font-medium text-white bg-emerald-600
            hover:bg-emerald-700 transition-colors shadow-sm
            disabled:opacity-60 disabled:cursor-not-allowed
          "
        >
          {loading ? (
            <>
              <Loader2 size={16} className="animate-spin" />
              Registering...
            </>
          ) : (
            <>
              <UserPlus size={16} />
              {submitLabel}
            </>
          )}
        </button>
      </div>
    </form>
  );
};

export default ChildForm;