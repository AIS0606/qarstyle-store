import { useState } from "react";
import { Header } from "./Header";
import { Search, Filter, Download, Eye, ChevronDown, Package } from "lucide-react";

const orders = [
  {
    id: "QS-2847",
    customer: "Айгерим Бекова",
    email: "aigеrim@mail.ru",
    product: "Rainforest Next Summer Anorak Jacket",
    category: "Мужской",
    status: "Доставлен",
    amount: "455 000 ₸",
    date: "11 мая 2026",
    city: "Алматы",
    items: 1,
  },
  {
    id: "QS-2846",
    customer: "Данияр Сейтов",
    email: "daniyar@gmail.com",
    product: "Traveler Jacket Blue Academy",
    category: "Мужской",
    status: "В пути",
    amount: "320 000 ₸",
    date: "11 мая 2026",
    city: "Астана",
    items: 1,
  },
  {
    id: "QS-2845",
    customer: "Мадина Жакупова",
    email: "madina@inbox.kz",
    product: "Raincape Anorak Jacket Beige",
    category: "Женский",
    status: "Обработка",
    amount: "393 000 ₸",
    date: "10 мая 2026",
    city: "Шымкент",
    items: 2,
  },
  {
    id: "QS-2844",
    customer: "Арман Нуров",
    email: "arman.n@mail.ru",
    product: "Rainforest Dune Anorak Beige",
    category: "Мужской",
    status: "Доставлен",
    amount: "360 000 ₸",
    date: "10 мая 2026",
    city: "Алматы",
    items: 1,
  },
  {
    id: "QS-2843",
    customer: "Зарина Абдрахман",
    email: "zarina@gmail.com",
    product: "Rainforest Next Summer Anorak",
    category: "Женский",
    status: "Отменён",
    amount: "455 000 ₸",
    date: "9 мая 2026",
    city: "Алматы",
    items: 1,
  },
  {
    id: "QS-2842",
    customer: "Нурлан Касымов",
    email: "nurlan@mail.ru",
    product: "Traveler Jacket Blue Academy",
    category: "Мужской",
    status: "Доставлен",
    amount: "320 000 ₸",
    date: "9 мая 2026",
    city: "Астана",
    items: 1,
  },
  {
    id: "QS-2841",
    customer: "Динара Ахметова",
    email: "dinara@inbox.kz",
    product: "Raincape Anorak Jacket",
    category: "Женский",
    status: "Доставлен",
    amount: "393 000 ₸",
    date: "8 мая 2026",
    city: "Алматы",
    items: 1,
  },
  {
    id: "QS-2840",
    customer: "Болат Джаксыбеков",
    email: "bolat@gmail.com",
    product: "Rainforest Dune Anorak",
    category: "Мужской",
    status: "В пути",
    amount: "360 000 ₸",
    date: "8 мая 2026",
    city: "Актобе",
    items: 2,
  },
];

const statusColors: Record<string, string> = {
  Доставлен: "bg-black text-white",
  "В пути": "bg-black/10 text-black",
  Обработка: "bg-amber-50 text-amber-700",
  Отменён: "bg-red-50 text-red-500",
};

const statuses = ["Все", "Доставлен", "В пути", "Обработка", "Отменён"];

const statusStats = [
  { label: "Всего", count: 128, color: "bg-black" },
  { label: "Доставлено", count: 94, color: "bg-emerald-500" },
  { label: "В пути", count: 18, color: "bg-black/30" },
  { label: "Обработка", count: 12, color: "bg-amber-400" },
  { label: "Отменено", count: 4, color: "bg-red-400" },
];

export function Orders() {
  const [search, setSearch] = useState("");
  const [activeStatus, setActiveStatus] = useState("Все");

  const filtered = orders.filter((o) => {
    const matchSearch =
      o.customer.toLowerCase().includes(search.toLowerCase()) ||
      o.id.toLowerCase().includes(search.toLowerCase()) ||
      o.product.toLowerCase().includes(search.toLowerCase());
    const matchStatus = activeStatus === "Все" || o.status === activeStatus;
    return matchSearch && matchStatus;
  });

  return (
    <div className="flex-1 flex flex-col min-h-screen bg-[#f8f8f8]">
      <Header title="Заказы" subtitle="Управление всеми заказами магазина" />

      <main className="flex-1 p-8 space-y-6">
        {/* Stats Row */}
        <div className="grid grid-cols-5 gap-3">
          {statusStats.map((s) => (
            <div key={s.label} className="bg-white rounded-xl p-4 border border-black/5">
              <div className="flex items-center gap-2 mb-2">
                <div className={`w-2 h-2 rounded-full ${s.color}`} />
                <span className="text-xs text-black/40">{s.label}</span>
              </div>
              <p className="text-2xl text-black">{s.count}</p>
            </div>
          ))}
        </div>

        {/* Table Card */}
        <div className="bg-white rounded-2xl border border-black/5">
          {/* Toolbar */}
          <div className="flex items-center gap-3 p-5 border-b border-black/5">
            <div className="flex items-center gap-2 bg-black/5 rounded-full px-4 py-2 flex-1 max-w-xs">
              <Search className="w-3.5 h-3.5 text-black/40 shrink-0" />
              <input
                type="text"
                placeholder="Поиск заказа..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="bg-transparent text-sm text-black placeholder:text-black/40 outline-none w-full"
              />
            </div>

            <div className="flex gap-1 ml-auto">
              {statuses.map((s) => (
                <button
                  key={s}
                  onClick={() => setActiveStatus(s)}
                  className={`px-3 py-1.5 rounded-full text-xs transition-colors ${
                    activeStatus === s
                      ? "bg-black text-white"
                      : "bg-black/5 text-black/50 hover:bg-black/10"
                  }`}
                >
                  {s}
                </button>
              ))}
            </div>

            <div className="flex gap-2 ml-2">
              <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs bg-black/5 text-black/50 hover:bg-black/10 transition-colors">
                <Filter className="w-3 h-3" />
                Фильтр
              </button>
              <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs bg-black/5 text-black/50 hover:bg-black/10 transition-colors">
                <Download className="w-3 h-3" />
                Экспорт
              </button>
            </div>
          </div>

          {/* Table */}
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-black/5">
                  <th className="text-left text-xs text-black/30 font-normal px-5 py-3">
                    <div className="flex items-center gap-1">
                      ID <ChevronDown className="w-3 h-3" />
                    </div>
                  </th>
                  <th className="text-left text-xs text-black/30 font-normal px-3 py-3">Клиент</th>
                  <th className="text-left text-xs text-black/30 font-normal px-3 py-3">Товар</th>
                  <th className="text-left text-xs text-black/30 font-normal px-3 py-3">Город</th>
                  <th className="text-left text-xs text-black/30 font-normal px-3 py-3">Статус</th>
                  <th className="text-left text-xs text-black/30 font-normal px-3 py-3">Дата</th>
                  <th className="text-right text-xs text-black/30 font-normal px-5 py-3">Сумма</th>
                  <th className="text-right text-xs text-black/30 font-normal px-5 py-3"></th>
                </tr>
              </thead>
              <tbody className="divide-y divide-black/5">
                {filtered.map((order) => (
                  <tr
                    key={order.id}
                    className="hover:bg-black/[0.02] transition-colors group"
                  >
                    <td className="px-5 py-3.5">
                      <div className="flex items-center gap-2">
                        <div className="w-7 h-7 rounded-lg bg-black/5 flex items-center justify-center">
                          <Package className="w-3.5 h-3.5 text-black/30" />
                        </div>
                        <span className="text-xs text-black/50">{order.id}</span>
                      </div>
                    </td>
                    <td className="px-3 py-3.5">
                      <p className="text-sm text-black">{order.customer}</p>
                      <p className="text-xs text-black/30">{order.email}</p>
                    </td>
                    <td className="px-3 py-3.5">
                      <p className="text-sm text-black max-w-[200px] truncate">
                        {order.product}
                      </p>
                      <p className="text-xs text-black/30">{order.category}</p>
                    </td>
                    <td className="px-3 py-3.5">
                      <span className="text-sm text-black/60">{order.city}</span>
                    </td>
                    <td className="px-3 py-3.5">
                      <span
                        className={`text-xs px-2.5 py-1 rounded-full ${statusColors[order.status]}`}
                      >
                        {order.status}
                      </span>
                    </td>
                    <td className="px-3 py-3.5">
                      <span className="text-xs text-black/40">{order.date}</span>
                    </td>
                    <td className="px-5 py-3.5 text-right">
                      <span className="text-sm text-black">{order.amount}</span>
                    </td>
                    <td className="px-5 py-3.5 text-right">
                      <button className="opacity-0 group-hover:opacity-100 transition-opacity w-7 h-7 rounded-full bg-black/5 hover:bg-black/10 flex items-center justify-center ml-auto">
                        <Eye className="w-3.5 h-3.5 text-black/40" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          <div className="flex items-center justify-between px-5 py-4 border-t border-black/5">
            <span className="text-xs text-black/30">
              Показано {filtered.length} из 128 заказов
            </span>
            <div className="flex gap-1">
              {[1, 2, 3, "...", 16].map((p, i) => (
                <button
                  key={i}
                  className={`w-7 h-7 rounded-full text-xs transition-colors ${
                    p === 1
                      ? "bg-black text-white"
                      : "text-black/40 hover:bg-black/5"
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
