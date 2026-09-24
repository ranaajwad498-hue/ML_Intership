import { AlertCircle } from "lucide-react";

/**
 * FormInput Component
 * -------------------
 * Reusable input/select field with label + error message.
 *
 * Props:
 *  - label       (string)  : Field label
 *  - name        (string)  : Field name (used by parent onChange)
 *  - value       (any)     : Current value
 *  - onChange    (function): Change handler
 *  - type        (string)  : "text" | "number" | "email" | "select" | ...
 *  - placeholder (string)  : Placeholder text
 *  - error       (string)  : Error message (if any)
 *  - required    (boolean) : Show red asterisk
 *  - options     (array)   : For type="select" — [{ value, label }]
 *  - min, max, step        : Passed through to native input
 */
const FormInput = ({
  label,
  name,
  value,
  onChange,
  type = "text",
  placeholder = "",
  error = "",
  required = false,
  options = [],
  min,
  max,
  step,
}) => {
  const baseClasses = `
    w-full px-3.5 py-2.5 rounded-lg text-sm
    bg-white border transition-colors
    focus:outline-none focus:ring-2
    ${
      error
        ? "border-red-300 focus:border-red-500 focus:ring-red-100"
        : "border-slate-300 focus:border-emerald-500 focus:ring-emerald-100"
    }
  `;

  return (
    <div className="flex flex-col gap-1.5">
      {/* Label */}
      {label && (
        <label
          htmlFor={name}
          className="text-sm font-medium text-slate-700"
        >
          {label}
          {required && <span className="text-red-500 ml-0.5">*</span>}
        </label>
      )}

      {/* Input OR Select */}
      {type === "select" ? (
        <select
          id={name}
          name={name}
          value={value}
          onChange={onChange}
          className={baseClasses}
        >
          {options.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      ) : (
        <input
          id={name}
          name={name}
          type={type}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          min={min}
          max={max}
          step={step}
          className={baseClasses}
        />
      )}

      {/* Error message */}
      {error && (
        <p className="flex items-center gap-1 text-xs text-red-600">
          <AlertCircle size={13} />
          {error}
        </p>
      )}
    </div>
  );
};

export default FormInput;