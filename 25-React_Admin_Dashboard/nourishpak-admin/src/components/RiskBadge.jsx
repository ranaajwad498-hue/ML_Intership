import { TriangleAlert, CircleAlert, CircleCheck } from "lucide-react";
const riskStyles = {
  "High Risk": {
    classes: "bg-red-100 text-red-700 border-red-200",
    Icon: TriangleAlert,
  },
  "Medium Risk": {
    classes: "bg-amber-100 text-amber-700 border-amber-200",
    Icon: CircleAlert,
  },
  "Low Risk": {
    classes: "bg-emerald-100 text-emerald-700 border-emerald-200",
    Icon: CircleCheck,
  },
};

const RiskBadge = ({ level = "Low Risk" }) => {
  const style = riskStyles[level] || riskStyles["Low Risk"];
  const { Icon } = style;

  return (
    <span
      className={`
        inline-flex items-center gap-1.5
        px-2.5 py-1 rounded-full
        text-xs font-medium border
        ${style.classes}
      `}
    >
      <Icon size={13} />
      {level}
    </span>
  );
};

export default RiskBadge;