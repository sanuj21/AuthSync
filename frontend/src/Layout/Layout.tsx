import React from "react";
import { Outlet } from "react-router-dom";
import Header from "../components/Header";
import Footer from "../components/Footer";

function Layout() {
  return (
    <div>
      <Header />
      <main className="h-lvh">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
}

export default Layout;
