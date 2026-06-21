import { NavLink, useLocation } from "react-router";
import {
  LayoutDashboard,
  ShoppingBag,
  Package,
  Users,
  BarChart3,
  Settings,
  Tag,
  Megaphone,
  ChevronRight,
  LogOut,
} from "lucide-react";

const navItems = [
  {
    label: "Обзор",
    icon: LayoutDashboard,
    to: "/",
  },
  {
    label: "Заказы",
    icon: ShoppingBag,
    to: "/orders",
  },
  {
    label: "Товары",
    icon: Package,
    to: "/products",
  },
  {
    label: "Категории",
    icon: Tag,
    to: "/categories",
  },
  {
    label: "Клиенты",
    icon: Users,
    to: "/customers",
  },
  {
    label: "Аналитика",
    icon: BarChart3,
    to: "/analytics",
  },
  {
    label: "Маркетинг",
    icon: Megaphone,
    to: "/marketing",
  },
  {
    label: "Настройки",
    icon: Settings,
    to: "/settings",
  },
];

export function Sidebar() {
  const location = useLocation();

  return (
    <aside className="fixed left-0 top-0 h-screen w-[240px] bg-black flex flex-col z-50">
      {/* Logo */}
      <div className="flex items-center justify-between px-6 py-6 border-b border-white/10">
        <div className="flex items-center gap-2">
          <svg width="36" height="20" viewBox="0 0 51.23 29.5612" fill="none">
            <path
              d="M35.8,0C30.1,0,25.6,4.2,25.6,9.6c0,3.3,1.7,6.2,4.3,8L25.6,22l-4.2-4.4c2.6-1.8,4.3-4.7,4.3-8 C25.7,4.2,21.2,0,15.5,0C9.8,0,5.3,4.2,5.3,9.6c0,5.4,4.5,9.6,10.2,9.6c1.7,0,3.3-0.4,4.7-1.1l5.4,5.7v5.7h2.9v-5.7l5.4-5.7 c1.4,0.7,3,1.1,4.7,1.1c5.7,0,10.2-4.2,10.2-9.6C46,4.2,41.5,0,35.8,0z M15.5,16.5c-4,0-7.2-3.1-7.2-6.9s3.2-6.9,7.2-6.9 s7.2,3.1,7.2,6.9S19.5,16.5,15.5,16.5z M35.8,16.5c-4,0-7.2-3.1-7.2-6.9s3.2-6.9,7.2-6.9s7.2,3.1,7.2,6.9S39.8,16.5,35.8,16.5z"
              fill="white"
            />
          </svg>
          <span className="text-white text-xs tracking-[0.2em] uppercase font-light">Admin</span>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-6 space-y-0.5 overflow-y-auto">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive =
            item.to === "/"
              ? location.pathname === "/"
              : location.pathname.startsWith(item.to);

          return (
            <NavLink
              key={item.to}
              to={item.to}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-150 group ${
                isActive
                  ? "bg-white text-black"
                  : "text-white/60 hover:text-white hover:bg-white/10"
              }`}
            >
              <Icon
                className={`w-4 h-4 shrink-0 ${isActive ? "text-black" : "text-white/60 group-hover:text-white"}`}
              />
              <span className="text-sm">{item.label}</span>
              {isActive && (
                <ChevronRight className="w-3 h-3 ml-auto text-black/40" />
              )}
            </NavLink>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="px-3 py-4 border-t border-white/10">
        <div className="flex items-center gap-3 px-3 py-2.5 rounded-lg">
          <div className="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center shrink-0">
            <span className="text-white text-xs">АД</span>
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-white text-sm truncate">Администратор</p>
            <p className="text-white/40 text-xs truncate">admin@qarstyle.kz</p>
          </div>
          <button className="text-white/40 hover:text-white transition-colors">
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </aside>
  );
}
