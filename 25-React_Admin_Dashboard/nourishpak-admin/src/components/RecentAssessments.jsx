import { Calendar } from "lucide-react";
import RiskBadge from "./RiskBadge";

const assessments = [
  {
    id: 101,
    name: "Ahmed",
    age: "18 Months",
    district: "Mardan",
    risk: "High Risk",
    date: "10-09-2026",
  },
  {
    id: 102,
    name: "Ayesha",
    age: "24 Months",
    district: "Peshawar",
    risk: "Low Risk",
    date: "10-09-2026",
  },
  {
    id: 103,
    name: "Bilal",
    age: "30 Months",
    district: "Swabi",
    risk: "Medium Risk",
    date: "09-09-2026",
  },
];

const RecentAssessments = () => {
  return (
    <section className="mt-8 bg-white rounded-xl shadow-sm border border-slate-200">
      {/* Section header */}
      <div className="flex items-center justify-between px-5 py-4 border-b border-slate-200">
        <div className="flex items-center gap-2">
          <Calendar size={18} className="text-emerald-600" />
          <h2 className="text-base font-semibold text-slate-800">
            Recent Child Assessments
          </h2>
        </div>
        <button className="text-xs font-medium text-emerald-600 hover:text-emerald-700 hover:underline">
          View All
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead className="bg-slate-50 text-slate-600">
            <tr>
              <th className="text-left font-medium px-5 py-3 whitespace-nowrap">Child ID</th>
              <th className="text-left font-medium px-5 py-3 whitespace-nowrap">Child Name</th>
              <th className="text-left font-medium px-5 py-3 whitespace-nowrap">Age</th>
              <th className="text-left font-medium px-5 py-3 whitespace-nowrap">District</th>
              <th className="text-left font-medium px-5 py-3 whitespace-nowrap">Risk Category</th>
              <th className="text-left font-medium px-5 py-3 whitespace-nowrap">Assessment Date</th>
            </tr>
          </thead>

          <tbody className="divide-y divide-slate-100">
            {assessments.map((child) => (
              <tr key={child.id} className="hover:bg-slate-50 transition-colors">
                <td className="px-5 py-3 text-slate-700 font-medium">
                  {child.id}
                </td>
                <td className="px-5 py-3 text-slate-800">{child.name}</td>
                <td className="px-5 py-3 text-slate-600">{child.age}</td>
                <td className="px-5 py-3 text-slate-600">{child.district}</td>
                <td className="px-5 py-3">
                  <RiskBadge level={child.risk} />
                </td>
                <td className="px-5 py-3 text-slate-500 whitespace-nowrap">
                  {child.date}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
};

export default RecentAssessments;