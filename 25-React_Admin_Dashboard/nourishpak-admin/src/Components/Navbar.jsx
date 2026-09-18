import React from 'react'
import { LogOut, User, Bell } from 'lucide-react'

export default function Navbar({ adminName = "Muhammad Ajwad", adminRole = "Administrator", onLogout }) {
  return (
    <header className="w-full bg-white border-b border-gray-200 px-6 py-3 flex justify-between items-center shadow-sm">
      {/* Brand Title */}
      <div className="flex items-center gap-3">
        <h1 className="text-xl font-bold text-emerald-600 tracking-wide">
          NourishPak <span className="text-xs font-semibold uppercase bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded-full ml-1">Admin Panel</span>
        </h1>
      </div>

      {/* Admin Profile & Actions */}
      <div className="flex items-center gap-6">
        {/* Notifications Icon (Optional) */}
        <button 
          className="relative p-2 text-gray-500 hover:text-emerald-600 hover:bg-gray-100 rounded-full transition-colors"
          aria-label="Notifications"
        >
          <Bell className="w-5 h-5" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-emerald-500 rounded-full"></span>
        </button>

        {/* Profile Info */}
        <div className="flex items-center gap-3 border-l border-gray-200 pl-6">
          <div className="w-9 h-9 rounded-full bg-emerald-500 text-white flex items-center justify-center font-semibold text-sm shadow-sm">
            <User className="w-5 h-5" />
          </div>
          
          <div className="flex flex-col">
            <span className="text-sm font-semibold text-gray-800 leading-tight">
              {adminName}
            </span>
            <span className="text-xs font-medium text-gray-500">
              {adminRole}
            </span>
          </div>
        </div>

        {/* Logout Button */}
        <button
          onClick={onLogout}
          className="flex items-center gap-2 px-3 py-1.5 text-sm font-medium text-red-600 bg-red-50 hover:bg-red-100 rounded-lg transition-colors border border-red-200"
        >
          <LogOut className="w-4 h-4" />
          <span>Logout</span>
        </button>
      </div>
    </header>
  )
}