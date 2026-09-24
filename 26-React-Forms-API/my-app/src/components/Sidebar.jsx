import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Baby,
  Brain,
  Stethoscope,
  Map,
  Users,
  FileText,
  LogOut,
  Leaf,
} from "lucide-react";

const menuItems = [
  { name: "Dashboard",      icon: LayoutDashboard, path: "/" },
  { name: "Children",       icon: Baby,            path: "/children" },
  { name: "Predictions",    icon: Brain,           path: "/predictions" },
  { name: "Health Workers", icon: Stethoscope,     path: "/health-workers" },
  { name: "Districts",      icon: Map,             path: "/districts" },
  { name: "Users",          icon: Users,           path: "/users" },
  { name: "Reports",        icon: FileText,        path: "/reports" },
];

const Sidebar = ({ isOpen = true, onClose }) => {
  return (
    <>
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/40 z-20 md:hidden"
          onClick={onClose}
        />
      )}

      <aside
        className={`
          fixed top-0 left-0 h-screen w-64 bg-slate-900 text-slate-100
          flex flex-col z-30 transform transition-transform duration-300
          ${isOpen ? "translate-x-0" : "-translate-x-full"}
          md:translate-x-0
        `}
      >
        {/* Brand */}
        <div className="px-6 py-5 border-b border-slate-700 flex items-center gap-2">
          <Leaf className="text-emerald-400" size={22} />
          <div>
            <h1 className="text-xl font-bold text-emerald-400">NourishPak</h1>
            <p className="text-xs text-slate-400">Admin Panel</p>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
          {menuItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.name}
                to={item.path}
                end={item.path === "/"}
                onClick={onClose}
                className={({ isActive }) =>
                  `
                  w-full flex items-center gap-3 px-4 py-2.5 rounded-lg
                  text-sm font-medium transition-colors duration-150
                  ${
                    isActive
                      ? "bg-emerald-600 text-white shadow-sm"
                      : "text-slate-300 hover:bg-slate-800 hover:text-white"
                  }
                `
                }
              >
                <Icon size={18} />
                <span>{item.name}</span>
              </NavLink>
            );
          })}
        </nav>

        {/* Logout */}
        <div className="px-3 py-4 border-t border-slate-700">
          <button
            className="
              w-full flex items-center gap-3 px-4 py-2.5 rounded-lg
              text-sm font-medium text-red-400
              hover:bg-red-500/10 hover:text-red-300
              transition-colors duration-150
            "
          >
            <LogOut size={18} />
            <span>Logout</span>
          </button>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;