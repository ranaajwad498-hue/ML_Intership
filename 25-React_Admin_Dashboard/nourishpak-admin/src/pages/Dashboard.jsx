import { Baby, TriangleAlert, CircleAlert, CircleCheck } from "lucide-react";
import DashboardCard from "../components/DashboardCard";
import RecentAssessments from "../components/RecentAssessments";

const Dashboard = () => {
  const stats = [
    {
      title: "Total Children",
      value: 120,
      description: "Registered in the monitoring system",
      icon: Baby,
      color: "emerald",
    },
    {
      title: "High Risk",
      value: 35,
      description: "Requires immediate attention",
      icon: TriangleAlert,
      color: "red",
    },
    {
      title: "Medium Risk",
      value: 50,
      description: "Needs regular monitoring",
      icon: CircleAlert,
      color: "amber",
    },
    {
      title: "Low Risk",
      value: 35,
      description: "Healthy nutrition status",
      icon: CircleCheck,
      color: "sky",
    },
  ];

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-800">Dashboard</h1>
        <p className="text-sm text-slate-500 mt-1">
          Overview of NourishPak child nutrition monitoring system.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat) => (
          <DashboardCard
            key={stat.title}
            title={stat.title}
            value={stat.value}
            description={stat.description}
            icon={stat.icon}
            color={stat.color}
          />
        ))}
      </div>
      <RecentAssessments />
    </div>
  );
};

export default Dashboard;