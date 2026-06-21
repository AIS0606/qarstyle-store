import { createBrowserRouter, Outlet } from "react-router";
import { Sidebar } from "./components/admin/Sidebar";
import { Dashboard } from "./components/admin/Dashboard";
import { Orders } from "./components/admin/Orders";
import { Products } from "./components/admin/Products";
import { Categories } from "./components/admin/Categories";
import { Customers } from "./components/admin/Customers";
import { Analytics } from "./components/admin/Analytics";
import { Marketing } from "./components/admin/Marketing";
import { Settings } from "./components/admin/Settings";

function AdminLayout() {
  return (
    <div className="flex min-h-screen bg-[#f8f8f8]">
      <Sidebar />
      <div className="flex-1 ml-[240px] flex flex-col">
        <Outlet />
      </div>
    </div>
  );
}

export const router = createBrowserRouter([
  {
    path: "/",
    Component: AdminLayout,
    children: [
      { index: true, Component: Dashboard },
      { path: "orders", Component: Orders },
      { path: "products", Component: Products },
      { path: "categories", Component: Categories },
      { path: "customers", Component: Customers },
      { path: "analytics", Component: Analytics },
      { path: "marketing", Component: Marketing },
      { path: "settings", Component: Settings },
    ],
  },
]);
