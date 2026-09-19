import { Menu, LogOut } from "lucide-react";

const Navbar = ({ onMenuClick }) => {
  const admin = {
    name: "Admin",
    role: "Admin",
    initials: "A",
  };

  return (
    <header className="sticky top-0 z-20 bg-white border-b border-slate-200 shadow-sm">
      <div className="flex items-center justify-between px-4 md:px-6 py-3">
        <div className="flex items-center gap-3">
          <button
            onClick={onMenuClick}
            className="md:hidden p-2 rounded-lg text-slate-600 hover:bg-slate-100 transition-colors"
            aria-label="Toggle sidebar"
          >
            <Menu size={22} />
          </button>

          <div>
            <h1 className="text-base md:text-lg font-semibold text-slate-800">
              NourishPak Admin Panel
            </h1>
            <p className="hidden sm:block text-xs text-slate-500">
              Child Nutrition Monitoring System
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 md:gap-4">
          <div className="hidden sm:block text-right leading-tight">
            <p className="text-sm font-medium text-slate-800">
              Welcome, {admin.name}
            </p>
            <p className="text-xs text-slate-500">
              Role:{" "}
              <span className="font-medium text-emerald-600">{admin.role}</span>
            </p>
          </div>

          <div className="w-9 h-9 md:w-10 md:h-10 rounded-full bg-emerald-600 text-white flex items-center justify-center font-semibold text-sm shadow-sm">
            {admin.initials}
          </div>

          <button
            className="
              flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium
              text-red-600 border border-red-200
              hover:bg-red-50 hover:border-red-300
              transition-colors duration-150
            "
          >
            <LogOut size={16} />
            <span className="hidden md:inline">Logout</span>
          </button>
        </div>
      </div>
    </header>
  );
};

export default Navbar;