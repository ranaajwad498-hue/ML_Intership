import { Home } from 'lucide-react'
import './App.css'
import Sidebar, { SidebarItem } from './Components/Sidebar'
import Layout from './layouts/AdminLayout'

function App() {
  
  return (
    <>
     <Sidebar>
          <SidebarItem text="NourishPak"/>
          <SidebarItem text="Dashboard"/>
          <SidebarItem text="Children"/>
          <SidebarItem text="Predictions"/>
          <SidebarItem text="Health Workers"/>
          <SidebarItem text="Districrs"/>
          <SidebarItem text="Users"/>
          <SidebarItem text="Reports"/>
          <SidebarItem text="Logout"/>
     </Sidebar>
     <Layout />
    </>
  )
}

export default App
