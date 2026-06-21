import { useState } from "react";
import { Header } from "./Header";
import { Search, UserPlus, Mail, Phone, MoreHorizontal, TrendingUp } from "lucide-react";

const customers = [
  {
    id: 1,
    name: "Айгерим Бекова",
    email: "aigerim@mail.ru",
    phone: "+7 777 123 45 67",
    city: "Алматы",
    orders: 12,
    totalSpent: "4 820 000 ₸",
    lastOrder: "11 мая 2026",
    status: "Активный",
    tier: "VIP",
  },
  {
    id: 2,
    name: "Данияр Сейтов",
    email: "daniyar@gmail.com",
    phone: "+7 701 234 56 78",
    city: "Астана",
    orders: 8,
    totalSpent: "2 960 000 ₸",
    lastOrder: "11 мая 2026",
    status: "Активный",
    tier: "Постоянный",
  },
  {
    id: 3,
    name: "Мадина Жакупова",
    email: "madina@inbox.kz",
    phone: "+7 747 345 67 89",
    city: "Шымкент",
    orders: 5,
    totalSpent: "1 850 000 ₸",
    lastOrder: "10 мая 2026",
    status: "Активный",
    tier: "Обычный",
  },
  {
    id: 4,
    name: "Арман Нуров",
    email: "arman.n@mail.ru",
    phone: "+7 705 456 78 90",
    city: "Алматы",
    orders: 15,
    totalSpent: "6 200 000 ₸",
    lastOrder: "10 мая 2026",
    status: "Активный",
    tier: "VIP",
  },
  {
    id: 5,
    name: "Зарина Абдрахман",
    email: "zarina@gmail.com",
    phone: "+7 776 567 89 01",
    city: "Алматы",
    orders: 2,
    totalSpent: "820 000 ₸",
    lastOrder: "9 мая 2026",
    status: "Неактивный",
    tier: "Новый",
  },
  {
    id: 6,
    name: "Нурлан Касымов",
    email: "nurlan@mail.ru",
    phone: "+7 778 678 90 12",
    city: "Астана",
    orders: 9,
    totalSpent: "3 180 000 ₸",
    lastOrder: "9 мая 2026",
    status: "Активный",
    tier: "Постоянный",
  },
  {
    id: 7,
    name: "Динара Ахметова",
    email: "dinara@inbox.kz",
    phone: "+7 700 789 01 23",
    city: "Алматы",
    orders: 7,
    totalSpent: "2 450 000 ₸",
    lastOrder: "8 мая 2026",
    status: "Активный",
    tier: "Постоянный",
  },
  {
    id: 8,
    name: "Болат Джаксыбеков",
    email: "bolat@gmail.com",
    phone: "+7 702 890 12 34",
    city: "Актобе",
    orders: 3,
    totalSpent: "1 020 000 ₸",
    lastOrder: "8 мая 2026",
    status: "Активный",
    tier: "Обычный",
  },
];

const tierColors: Record<string, string> = {
  VIP: "bg-black text-white",
  Постоянный: "bg-black/10 text-black",
  Обычный: "bg-black/5 text-black/60",
  Новый: "bg-blue-50 text-blue-600",
};

const tierStats = [
  { label: "VIP клиенты", count: 127, color: "text-black" },
  { label: "Постоянные", count: 489, color: "text-black/60" },
  { label: "Обычные", count: 831, color: "text-black/40" },
  { label: "Новые", count: 400, color: "text-blue-500" },
];

export function Customers() {
  const [search, setSearch] = useState("");
  const [tier, setTier] = useState("Все");

  const tiers = ["Все", "VIP", "Постоянный", "Обычный", "Новый"];

  const filtered = customers.filter((c) => {
    const matchSearch =
      c.name.toLowerCase().includes(search.toLowerCase()) ||
      c.email.toLowerCase().includes(search.toLowerCase());
    const matchTier = tier === "Все" || c.tier === tier;
    return matchSearch && matchTier;
  });

  return (
    <div className="flex-1 flex flex-col min-h-screen bg-[#f8f8f8]">
      <Header title="Клиенты" subtitle="База клиентов магазина QarStyle" />

      <main className="flex-1 p-8 space-y-6">
        {/* KPI */}
        <div className="grid grid-cols-4 gap-4">
          <div className="bg-white rounded-2xl p-6 border border-black/5 col-span-1">
            <p className="text-xs text-black/40 mb-1">Всего клиентов</p>
            <p className="text-3xl text-black mb-3">1 847</p>
            <div className="flex items-center gap-1 text-xs text-emerald-600">
              <TrendingUp className="w-3 h-3" />
              <span>+5.3% в этом месяце</span>
            </div>
          </div>
          {tierStats.map((s) => (
            <div key={s.label} className="bg-white rounded-2xl p-6 border border-black/5">
              <p className="text-xs text-black/40 mb-1">{s.label}</p>
              <p className={`text-3xl ${s.color}`}>{s.count}</p>
            </div>
          ))}
        </div>

        {/* Customers Table */}
        <div className="bg-white rounded-2xl border border-black/5">
          <div className="flex items-center gap-3 p-5 border-b border-black/5">
            <div className="flex items-center gap-2 bg-black/5 rounded-full px-4 py-2 flex-1 max-w-xs">
              <Search className="w-3.5 h-3.5 text-black/40 shrink-0" />
              <input
                type="text"
                placeholder="Поиск клиента..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="bg-transparent text-sm text-black placeholder:text-black/40 outline-none w-full"
              />
            </div>

            <div className="flex gap-1">
              {tiers.map((t) => (
                <button
                  key={t}
                  onClick={() => setTier(t)}
                  className={`px-3 py-1.5 rounded-full text-xs transition-colors ${
                    tier === t
                      ? "bg-black text-white"
                      : "bg-black/5 text-black/50 hover:bg-black/10"
                  }`}
                >
                  {t}
                </button>
              ))}
            </div>

            <button className="ml-auto flex items-center gap-1.5 px-4 py-1.5 rounded-full text-xs bg-black text-white hover:bg-black/80 transition-colors">
              <UserPlus className="w-3 h-3" />
              Добавить
            </button>
          </div>

          <table className="w-full">
            <thead>
              <tr className="border-b border-black/5">
                <th className="text-left text-xs text-black/30 font-normal px-5 py-3">Клиент</th>
                <th className="text-left text-xs text-black/30 font-normal px-3 py-3">Контакты</th>
                <th className="text-left text-xs text-black/30 font-normal px-3 py-3">Город</th>
                <th className="text-left text-xs text-black/30 font-normal px-3 py-3">Уровень</th>
                <th className="text-left text-xs text-black/30 font-normal px-3 py-3">Заказы</th>
                <th className="text-left text-xs text-black/30 font-normal px-3 py-3">Последний</th>
                <th className="text-right text-xs text-black/30 font-normal px-5 py-3">Сумма</th>
                <th className="px-5 py-3" />
              </tr>
            </thead>
            <tbody className="divide-y divide-black/5">
              {filtered.map((customer) => (
                <tr
                  key={customer.id}
                  className="hover:bg-black/[0.02] transition-colors group"
                >
                  <td className="px-5 py-3.5">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-full bg-black flex items-center justify-center shrink-0">
                        <span className="text-white text-xs">
                          {customer.name
                            .split(" ")
                            .map((n) => n[0])
                            .join("")
                            .slice(0, 2)}
                        </span>
                      </div>
                      <div>
                        <p className="text-sm text-black">{customer.name}</p>
                        <p className="text-xs text-black/30">{customer.status}</p>
                      </div>
                    </div>
                  </td>
                  <td className="px-3 py-3.5">
                    <div className="flex flex-col gap-0.5">
                      <div className="flex items-center gap-1.5">
                        <Mail className="w-3 h-3 text-black/30" />
                        <span className="text-xs text-black/50">{customer.email}</span>
                      </div>
                      <div className="flex items-center gap-1.5">
                        <Phone className="w-3 h-3 text-black/30" />
                        <span className="text-xs text-black/50">{customer.phone}</span>
                      </div>
                    </div>
                  </td>
                  <td className="px-3 py-3.5">
                    <span className="text-sm text-black/60">{customer.city}</span>
                  </td>
                  <td className="px-3 py-3.5">
                    <span
                      className={`text-xs px-2.5 py-1 rounded-full ${tierColors[customer.tier]}`}
                    >
                      {customer.tier}
                    </span>
                  </td>
                  <td className="px-3 py-3.5">
                    <span className="text-sm text-black">{customer.orders}</span>
                  </td>
                  <td className="px-3 py-3.5">
                    <span className="text-xs text-black/40">{customer.lastOrder}</span>
                  </td>
                  <td className="px-5 py-3.5 text-right">
                    <span className="text-sm text-black">{customer.totalSpent}</span>
                  </td>
                  <td className="px-5 py-3.5">
                    <button className="opacity-0 group-hover:opacity-100 transition-opacity w-7 h-7 rounded-full bg-black/5 hover:bg-black/10 flex items-center justify-center ml-auto">
                      <MoreHorizontal className="w-3.5 h-3.5 text-black/40" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          <div className="flex items-center justify-between px-5 py-4 border-t border-black/5">
            <span className="text-xs text-black/30">
              Показано {filtered.length} из 1 847 клиентов
            </span>
            <div className="flex gap-1">
              {[1, 2, 3, "...", 231].map((p, i) => (
                <button
                  key={i}
                  className={`w-7 h-7 rounded-full text-xs transition-colors ${
                    p === 1 ? "bg-black text-white" : "text-black/40 hover:bg-black/5"
                  }`}
                >
                  {p}
                </button>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
