import { useState } from "react";
import { Outlet } from "react-router-dom";
import SideBar from "../components/SideBar.jsx";
import Footer from "../components/Footer.jsx";
import NavBar from "../components/NavBar.jsx";

const AppLayout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen flex flex-col bg-gray-200 font-roboto">
      <div className="flex flex-1 ">
        <aside className={`fixed md:static inset-y-0 left-0 z-40  bg-[#009485] text-white transform transition-transform duration-300 ${sidebarOpen ? "translate-x-0" : "-translate-x-full"} md:translate-x-0`}>
          <SideBar closeSidebar={()=>setSidebarOpen(false)} />
        </aside>

        {sidebarOpen && (
          <div onClick={()=>setSidebarOpen(false)} className="fixed inset-0 bg-black/40 z-30 md:hidden"/>
        )}
        <main className="flex-1 min-h-screen w-screen overflow-x-auto">
          <NavBar toggleSidebar={()=>setSidebarOpen(true)} />
          <Outlet />
        </main>
      </div>
      <Footer />
    </div>
  );
};

export default AppLayout;
