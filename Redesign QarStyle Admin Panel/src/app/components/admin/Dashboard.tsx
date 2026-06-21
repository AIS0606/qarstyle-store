import { useState } from "react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
} from "recharts";
import {
  TrendingUp,
  TrendingDown,
  ShoppingBag,
  Users,
  Package,
  DollarSign,
  ArrowRight,
} from "lucide-react";
import { Header } from "./Header";
import { Link } from "react-router";

import imgProduct1 from "figma:asset/c464a2e3f7f0901869f0d0893911e6309c80e890.png";
import imgProduct2 from "figma:asset/885442841d323cce8f1c64a4da2be84e7adc3cbf.png";
import imgProduct3 from "figma:asset/3f5e97f522f9668871004167ad76030b615a048a.png";
import imgProduct4 from "figma:asset/35b7a066f5247f6aad11fed6b12f4a58183354c1.png";

const revenueData = [
  { month: "Янв", revenue: 4200000, orders: 89 },
  { month: "Фев", revenue: 3800000, orders: 72 },
  { month: "Мар", revenue: 5100000, orders: 104 },
  { month: "Апр", revenue: 4700000, orders: 96 },
  { month: "Май", revenue: 6200000, orders: 128 },
  { month: "Июн", revenue: 5800000, orders: 117 },
  { month: "Июл", revenue: 7100000, orders: 145 },
  { month: "Авг", revenue: 6600000, orders: 134 },
  { month: "Сен", revenue: 5900000, orders: 121 },
  { month: "Окт", revenue: 7800000, orders: 158 },
  { month: "Ноя", revenue: 9200000, orders: 187 },
  { month: "Дек", revenue: 8400000, orders: 171 },
];

const categoryData = [
  { name: "Мужской", value: 38 },
  { name: "Женский", value: 29 },
  { name: "Детский", value: 14 },
  { name: "Сумки", value: 11 },
  { name: "Прочее", value: 8 },
];

const recentOrders = [
  {
    id: "QS-2847",
    customer: "Айгерим Бекова",
    product: "Rainforest Anorak Jacket",
    status: "Доставлен",
    amount: "455 000 ₸",
    date: "11 мая",
  },
  {
    id: "QS-2846",
    customer: "Данияр Сейтов",
    product: "Traveler Jacket Blue",
    status: "В пути",
    amount: "320 000 ₸",
    date: "11 мая",
  },
  {
    id: "QS-2845",
    customer: "Мадина Жакупова",
    product: "Raincape Anorak Jacket",
    status: "Обработка",
    amount: "393 000 ₸",
    date: "10 мая",
  },
  {
    id: "QS-2844",
    customer: "Арман Нуров",
    product: "Rainforest Dune Anorak",
    status: "Доставлен",
    amount: "360 000 ₸",
    date: "10 мая",
  },
  {
    id: "QS-2843",
    customer: "Зарина Абдрахман",
    product: "Rainforest Next Summer",
    status: "Отменён",
    amount: "455 000 ₸",
    date: "9 мая",
  },
];

const topProducts = [
  {
    name: "Rainforest Next Summer Anorak",
    img: imgProduct1,
    sold: 247,
    revenue: "112 485 000 ₸",
    trend: "up",
  },
  {
    name: "Raincape Anorak Jacket",
    img: imgProduct2,
    sold: 198,
    revenue: "77 814 000 ₸",
    trend: "up",
  },
  {
    name: "Rainforest Dune Anorak",
    img: imgProduct3,
    sold: 163,
    revenue: "58 680 000 ₸",
    trend: "down",
  },
  {
    name: "Traveler Jacket Blue",
    img: imgProduct4,
    sold: 142,
    revenue: "45 440 000 ₸",
    trend: "up",
  },
];

const statusColors: Record<string, string> = {
  Доставлен: "bg-black text-white",
  "В пути": "bg-black/10 text-black",
  Обработка: "bg-black/5 text-black/60",
  Отменён: "bg-red-50 text-red-600",
};

const kpiCards = [
  {
    label: "Выручка (май)",
    value: "6 200 000 ₸",
    change: "+18.4%",
    trend: "up",
    icon: DollarSign,
    sub: "vs апрель",
  },
  {
    label: "Заказы",
    value: "128",
    change: "+12.1%",
    trend: "up",
    icon: ShoppingBag,
    sub: "в этом месяце",
  },
  {
    label: "Клиенты",
    value: "1 847",
    change: "+5.3%",
    trend: "up",
    icon: Users,
    sub: "всего активных",
  },
  {
    label: "Товаров",
    value: "342",
    change: "-3",
    trend: "down",
    icon: Package,
    sub: "в наличии",
  },
];

export function Dashboard() {
  const [period, setPeriod] = useState<"year" | "quarter" | "month">("year");

  const displayData =
    period === "year"
      ? revenueData
      : period === "quarter"
        ? revenueData.slice(9, 12)
        : revenueData.slice(11, 12);

  return (
    <div className="flex-1 flex flex-col min-h-screen bg-[#f8f8f8]">
      <Header title="Обзор" subtitle="Добро пожаловать в панель управления QarStyle" />

      <main className="flex-1 p-8 space-y-6">
        {/* KPI Cards */}
        <div className="grid grid-cols-4 gap-4">
          {kpiCards.map((card) => {
            const Icon = card.icon;
            return (
              <div
                key={card.label}
                className="bg-white rounded-2xl p-6 border border-black/5 hover:border-black/10 transition-colors"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="w-10 h-10 rounded-xl bg-black flex items-center justify-center">
                    <Icon className="w-4 h-4 text-white" />
                  </div>
                  <span
                    className={`flex items-center gap-1 text-xs px-2 py-1 rounded-full ${
                      card.trend === "up"
                        ? "bg-emerald-50 text-emerald-600"
                        : "bg-red-50 text-red-500"
                    }`}
                  >
                    {card.trend === "up" ? (
                      <TrendingUp className="w-3 h-3" />
                    ) : (
                      <TrendingDown className="w-3 h-3" />
                    )}
                    {card.change}
                  </span>
                </div>
                <p className="text-2xl text-black mb-1">{card.value}</p>
                <p className="text-xs text-black/40">{card.label}</p>
                <p className="text-xs text-black/30 mt-0.5">{card.sub}</p>
              </div>
            );
          })}
        </div>

        {/* Charts Row */}
        <div className="grid grid-cols-3 gap-4">
          {/* Revenue Chart */}
          <div className="col-span-2 bg-white rounded-2xl p-6 border border-black/5">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-black">Выручка</h2>
                <p className="text-xs text-black/40 mt-0.5">Динамика продаж</p>
              </div>
              <div className="flex gap-1">
                {(["year", "quarter", "month"] as const).map((p) => (
                  <button
                    key={p}
                    onClick={() => setPeriod(p)}
                    className={`px-3 py-1.5 rounded-full text-xs transition-colors ${
                      period === p
                        ? "bg-black text-white"
                        : "bg-black/5 text-black/50 hover:bg-black/10"
                    }`}
                  >
                    {p === "year" ? "Год" : p === "quarter" ? "Квартал" : "Месяц"}
                  </button>
                ))}
              </div>
            </div>
            <ResponsiveContainer width="100%" height={220}>
              <AreaChart data={displayData}>
                <defs>
                  <linearGradient id="revenueGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#000" stopOpacity={0.08} />
                    <stop offset="95%" stopColor="#000" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#00000008" />
                <XAxis
                  dataKey="month"
                  tick={{ fontSize: 11, fill: "#00000060" }}
                  axisLine={false}
                  tickLine={false}
                />
                <YAxis
                  tick={{ fontSize: 11, fill: "#00000060" }}
                  axisLine={false}
                  tickLine={false}
                  tickFormatter={(v) => `${(v / 1000000).toFixed(1)}M`}
                />
                <Tooltip
                  formatter={(v: number) => [`${v.toLocaleString("ru-RU")} ₸`, "Выручка"]}
                  contentStyle={{
                    background: "#000",
                    border: "none",
                    borderRadius: "8px",
                    color: "#fff",
                    fontSize: "12px",
                  }}
                  labelStyle={{ color: "#ffffff80" }}
                />
                <Area
                  type="monotone"
                  dataKey="revenue"
                  stroke="#000"
                  strokeWidth={2}
                  fill="url(#revenueGrad)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>

          {/* Category Chart */}
          <div className="bg-white rounded-2xl p-6 border border-black/5">
            <div className="mb-6">
              <h2 className="text-black">По категориям</h2>
              <p className="text-xs text-black/40 mt-0.5">Доля продаж, %</p>
            </div>
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={categoryData} layout="vertical" barSize={6}>
                <XAxis type="number" hide />
                <YAxis
                  type="category"
                  dataKey="name"
                  width={60}
                  tick={{ fontSize: 11, fill: "#00000060" }}
                  axisLine={false}
                  tickLine={false}
                />
                <Tooltip
                  formatter={(v: number) => [`${v}%`, "Доля"]}
                  contentStyle={{
                    background: "#000",
                    border: "none",
                    borderRadius: "8px",
                    color: "#fff",
                    fontSize: "12px",
                  }}
                />
                <Bar dataKey="value" fill="#000" radius={[0, 3, 3, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Bottom Row */}
        <div className="grid grid-cols-3 gap-4">
          {/* Recent Orders */}
          <div className="col-span-2 bg-white rounded-2xl border border-black/5">
            <div className="flex items-center justify-between p-6 border-b border-black/5">
              <div>
                <h2 className="text-black">Последние заказы</h2>
                <p className="text-xs text-black/40 mt-0.5">5 из 128 заказов</p>
              </div>
              <Link
                to="/orders"
                className="flex items-center gap-1 text-xs text-black/50 hover:text-black transition-colors"
              >
                Все заказы <ArrowRight className="w-3 h-3" />
              </Link>
            </div>
            <div className="divide-y divide-black/5">
              {recentOrders.map((order) => (
                <div
                  key={order.id}
                  className="flex items-center gap-4 px-6 py-3.5 hover:bg-black/[0.02] transition-colors"
                >
                  <span className="text-xs text-black/40 w-16 shrink-0">{order.id}</span>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-black truncate">{order.customer}</p>
                    <p className="text-xs text-black/40 truncate">{order.product}</p>
                  </div>
                  <span
                    className={`text-xs px-2.5 py-1 rounded-full shrink-0 ${statusColors[order.status]}`}
                  >
                    {order.status}
                  </span>
                  <span className="text-sm text-black shrink-0 w-28 text-right">
                    {order.amount}
                  </span>
                  <span className="text-xs text-black/30 w-14 text-right shrink-0">
                    {order.date}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Top Products */}
          <div className="bg-white rounded-2xl border border-black/5">
            <div className="flex items-center justify-between p-6 border-b border-black/5">
              <div>
                <h2 className="text-black">Топ товары</h2>
                <p className="text-xs text-black/40 mt-0.5">По продажам</p>
              </div>
              <Link
                to="/products"
                className="flex items-center gap-1 text-xs text-black/50 hover:text-black transition-colors"
              >
                Все <ArrowRight className="w-3 h-3" />
              </Link>
            </div>
            <div className="divide-y divide-black/5">
              {topProducts.map((product, i) => (
                <div
                  key={product.name}
                  className="flex items-center gap-3 px-4 py-3 hover:bg-black/[0.02] transition-colors"
                >
                  <span className="text-xs text-black/20 w-4 shrink-0">{i + 1}</span>
                  <div className="w-10 h-10 rounded-lg overflow-hidden bg-[#f0f0f0] shrink-0">
                    <img
                      src={product.img}
                      alt={product.name}
                      className="w-full h-full object-cover mix-blend-multiply"
                    />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs text-black truncate">{product.name}</p>
                    <p className="text-xs text-black/40">{product.sold} шт.</p>
                  </div>
                  {product.trend === "up" ? (
                    <TrendingUp className="w-3.5 h-3.5 text-emerald-500 shrink-0" />
                  ) : (
                    <TrendingDown className="w-3.5 h-3.5 text-red-400 shrink-0" />
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}