import React from 'react'
import logo from '../assets/adminlogo.avif'
import profile from '../assets/profile.jpg'
import { ChevronFirst, MoreVertical } from "lucide-react"

export default function Sidebar({ children }) {
    return (
        <>
            <aside className="h-screen w-54">
                <nav className="h-full flex flex-col bg-white border-r shadow-sm">
                    <div className="p-4 pb-2 flex justify-between items-center">
                        <img src={logo} className="w-32" />
                        <button className="p-1.5 rounded-lg bg-gray-50 hover:bg-gray-100">
                            <ChevronFirst />
                        </button>
                    </div>

                    <ul className="flex-1 px-3">{children}</ul>

                    <div className="border-t flex p-3">
                        <img src={profile} className="w-10 h-10 rounded-md" />
                        <div className="flex justify-between items-center overflow-hidden">
                            <div className="leading-4">
                                <h4 className="font-semibold">Rana Ajwad</h4>
                                <span className="text-xs text-gray-600">ajwadrana@gmail.com</span>
                            </div>
                            <MoreVertical size={20} />
                        </div>
                    </div>

                </nav>
            </aside>
        </>
    )
}


export function SidebarItem({icon, text, active, alert}){
    return(
   <li>
         {icon}
        <span>{text}</span>
   </li>
    )
}