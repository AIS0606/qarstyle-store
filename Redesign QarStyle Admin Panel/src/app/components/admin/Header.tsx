import { Bell, Search } from "lucide-react";

interface HeaderProps {
  title: string;
  subtitle?: string;
}

export function Header({ title, subtitle }: HeaderProps) {
  return (
    <header className="h-16 bg-white border-b border-black/10 flex items-center justify-between px-8 sticky top-0 z-40">
      <div>
        <h1 className="text-black">{title}</h1>
        {subtitle && <p className="text-xs text-black/40 mt-0.5">{subtitle}</p>}
      </div>
      <div className="flex items-center gap-3">
        {/* Search */}
        <div className="flex items-center gap-2 bg-black/5 rounded-full px-4 py-2 w-56">
          <Search className="w-3.5 h-3.5 text-black/40" />
          <input
            type="text"
            placeholder="Поиск..."
            className="bg-transparent text-sm text-black placeholder:text-black/40 outline-none w-full"
          />
        </div>

        {/* Notifications */}
        <button className="relative w-9 h-9 rounded-full bg-black/5 flex items-center justify-center hover:bg-black/10 transition-colors">
          <Bell className="w-4 h-4 text-black/60" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-black rounded-full" />
        </button>

        {/* Date */}
        <div className="text-xs text-black/40 pl-2 border-l border-black/10">
          {new Date().toLocaleDateString("ru-RU", {
            day: "numeric",
            month: "long",
            year: "numeric",
          })}
        </div>
      </div>
    </header>
  );
}
