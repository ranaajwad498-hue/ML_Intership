import { useState } from "react";
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
  { name: "Dashboard",      icon: LayoutDashboard },
  { name: "Children",       icon: Baby },
  { name: "Predictions",    icon: Brain },
  { name: "Health Workers", icon: Stethoscope },
  { name: "Districts",      icon: Map },
  { name: "Users",          icon: Users },
  { name: "Reports",        icon: FileText },
];

const Sidebar = ({ isOpen = true, onClose }) => {
  const [activeItem, setActiveItem] = useState("Dashboard");

  const handleItemClick = (name) => {
    setActiveItem(name);
    if (onClose) onClose();
  };

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
          md:translate-x-0 md:static md:flex
        `}
      >
        <div className="px-6 py-5 border-b border-slate-700 flex items-center gap-2">
          <Leaf className="text-emerald-400" size={22} />
          <div>
            <h1 className="text-xl font-bold text-emerald-400">NourishPak</h1>
            <p className="text-xs text-slate-400">Admin Panel</p>
          </div>
        </div>

        <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeItem === item.name;
            return (
              <button
                key={item.name}
                onClick={() => handleItemClick(item.name)}
                className={`
                  w-full flex items-center gap-3 px-4 py-2.5 rounded-lg
                  text-sm font-medium transition-colors duration-150
                  ${
                    isActive
                      ? "bg-emerald-600 text-white shadow-sm"
                      : "text-slate-300 hover:bg-slate-800 hover:text-white"
                  }
                `}
              >
                <Icon size={18} />
                <span>{item.name}</span>
              </button>
            );
          })}
        </nav>

    
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