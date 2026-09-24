import { TriangleAlert, CircleAlert, CircleCheck, Lightbulb } from "lucide-react";

/**
 * PredictionResult Component
 * --------------------------
 * Displays the ML prediction result for a child.
 *
 * Props:
 *  - childName   (string) : Name of the child
 *  - riskScore   (number) : 0–100 risk score from backend
 *  - category    (string) : "High Risk" | "Medium Risk" | "Low Risk"
 *  - confidence  (number) : 0–100 confidence percentage
 *  - advice      (string) : Recommendation text from backend
 */
const categoryStyles = {
  "High Risk": {
    classes: "bg-red-50 border-red-200 text-red-700",
    badge: "bg-red-100 text-red-700",
    bar: "bg-red-500",
    Icon: TriangleAlert,
  },
  "Medium Risk": {
    classes: "bg-amber-50 border-amber-200 text-amber-700",
    badge: "bg-amber-100 text-amber-700",
    bar: "bg-amber-500",
    Icon: CircleAlert,
  },
  "Low Risk": {
    classes: "bg-emerald-50 border-emerald-200 text-emerald-700",
    badge: "bg-emerald-100 text-emerald-700",
    bar: "bg-emerald-500",
    Icon: CircleCheck,
  },
};

const PredictionResult = ({
  childName = "Child",
  riskScore = 0,
  category = "Low Risk",
  confidence = 0,
  advice = "",
}) => {
  const style = categoryStyles[category] || categoryStyles["Low Risk"];
  const { Icon } = style;

  return (
    <section
      className={`
        mt-6 rounded-xl border p-5 shadow-sm
        ${style.classes}
      `}
    >
      {/* Header */}
      <div className="flex items-center gap-2 mb-4">
        <Icon size={20} />
        <h2 className="text-base font-semibold">
          Nutrition Risk Assessment
        </h2>
      </div>

      {/* Child name */}
      <p className="text-sm mb-4">
        <span className="font-medium">Child:</span> {childName}
      </p>

      {/* Risk score + progress bar */}
      <div className="mb-4">
        <div className="flex items-center justify-between mb-1.5">
          <span className="text-sm font-medium">Risk Score</span>
          <span className="text-sm font-bold">{riskScore}/100</span>
        </div>
        <div className="w-full h-2 bg-white/60 rounded-full overflow-hidden">
          <div
            className={`h-full ${style.bar} transition-all duration-500`}
            style={{ width: `${Math.min(Math.max(riskScore, 0), 100)}%` }}
          />
        </div>
      </div>

      {/* Category + Confidence */}
      <div className="flex flex-wrap items-center gap-3 mb-4">
        <span
          className={`
            inline-flex items-center gap-1.5
            px-3 py-1 rounded-full text-xs font-semibold
            ${style.badge}
          `}
        >
          <Icon size={13} />
          {category}
        </span>

        <span className="text-xs font-medium">
          Confidence: {confidence}%
        </span>
      </div>

      {/* Advice */}
      {advice && (
        <div className="flex items-start gap-2 pt-4 border-t border-current/20">
          <Lightbulb size={16} className="mt-0.5 flex-shrink-0" />
          <div>
            <p className="text-xs font-semibold uppercase tracking-wide mb-1">
              Advice
            </p>
            <p className="text-sm leading-relaxed">{advice}</p>
          </div>
        </div>
      )}
    </section>
  );
};

export default PredictionResult;