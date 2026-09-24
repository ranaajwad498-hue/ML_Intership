/**
 * DashboardCard Component
 * -----------------------
 * A reusable statistic card.
 *
 * Props:
 *  - title       (string)         : Card heading
 *  - value       (string|number)  : Main metric
 *  - description (string)         : Optional helper text
 *  - icon        (ReactComponent) : Lucide icon component (e.g. Baby)
 *  - color       (string)         : "emerald" | "red" | "amber" | "sky" | "slate"
 */
const colorMap = {
  emerald: {
    iconBg: "bg-emerald-100",
    iconText: "text-emerald-700",
    accent: "border-emerald-500",
    value: "text-emerald-700",
  },
  red: {
    iconBg: "bg-red-100",
    iconText: "text-red-700",
    accent: "border-red-500",
    value: "text-red-700",
  },
  amber: {
    iconBg: "bg-amber-100",
    iconText: "text-amber-700",
    accent: "border-amber-500",
    value: "text-amber-700",
  },
  sky: {
    iconBg: "bg-sky-100",
    iconText: "text-sky-700",
    accent: "border-sky-500",
    value: "text-sky-700",
  },
  slate: {
    iconBg: "bg-slate-100",
    iconText: "text-slate-700",
    accent: "border-slate-500",
    value: "text-slate-800",
  },
};

const DashboardCard = ({
  title = "Untitled",
  value = 0,
  description = "",
  icon: Icon,
  color = "slate",
}) => {
  const theme = colorMap[color] || colorMap.slate;

  return (
    <div
      className={`
        bg-white rounded-xl shadow-sm border border-slate-200
        border-l-4 ${theme.accent}
        p-5 flex flex-col gap-3
        hover:shadow-md transition-shadow duration-200
      `}
    >
      <div className="flex items-center gap-3">
        <div
          className={`
            w-10 h-10 rounded-lg flex items-center justify-center
            ${theme.iconBg} ${theme.iconText}
          `}
        >
          {Icon && <Icon size={20} />}
        </div>
        <h3 className="text-sm font-medium text-slate-600">{title}</h3>
      </div>

      <div className={`text-3xl font-bold ${theme.value}`}>{value}</div>

      {description && (
        <p className="text-xs text-slate-500 leading-relaxed">{description}</p>
      )}
    </div>
  );
};

export default DashboardCard;