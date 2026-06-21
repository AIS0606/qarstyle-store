import { Header } from "./Header";
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
} from "recharts";

const monthlyData = [
  { month: "Янв", revenue: 4200000, orders: 89, customers: 67 },
  { month: "Фев", revenue: 3800000, orders: 72, customers: 54 },
  { month: "Мар", revenue: 5100000, orders: 104, customers: 89 },
  { month: "Апр", revenue: 4700000, orders: 96, customers: 73 },
  { month: "Май", revenue: 6200000, orders: 128, customers: 104 },
  { month: "Июн", revenue: 5800000, orders: 117, customers: 92 },
  { month: "Июл", revenue: 7100000, orders: 145, customers: 118 },
  { month: "Авг", revenue: 6600000, orders: 134, customers: 107 },
  { month: "Сен", revenue: 5900000, orders: 121, customers: 96 },
  { month: "Окт", revenue: 7800000, orders: 158, customers: 134 },
  { month: "Ноя", revenue: 9200000, orders: 187, customers: 163 },
  { month: "Дек", revenue: 8400000, orders: 171, customers: 148 },
];

const categoryPie = [
  { name: "Мужской", value: 38, color: "#000" },
  { name: "Женский", value: 29, color: "#333" },
  { name: "Детский", value: 14, color: "#666" },
  { name: "Сумки", value: 11, color: "#999" },
  { name: "Прочее", value: 8, color: "#ccc" },
];

const cityData = [
  { city: "Алматы", orders: 547, revenue: 221000000 },
  { city: "Астана", orders: 312, revenue: 128000000 },
  { city: "Шымкент", orders: 187, revenue: 72000000 },
  { city: "Актобе", orders: 124, revenue: 46000000 },
  { city: "Костанай", orders: 89, revenue: 32000000 },
  { city: "Другие", orders: 234, revenue: 87000000 },
];

const conversionData = [
  { day: "Пн", visits: 1240, orders: 42 },
  { day: "Вт", visits: 1080, orders: 36 },
  { day: "Ср", visits: 1560, orders: 58 },
  { day: "Чт", visits: 1320, orders: 48 },
  { day: "Пт", visits: 1840, orders: 72 },
  { day: "Сб", visits: 2100, orders: 89 },
  { day: "Вс", visits: 1680, orders: 64 },
];

export function Analytics() {
  return (
    <div className="flex-1 flex flex-col min-h-screen bg-[#f8f8f8]">
      <Header title="Аналитика" subtitle="Детальная статистика и отчёты" />

      <main className="flex-1 p-8 space-y-6">
        {/* Summary KPIs */}
        <div className="grid grid-cols-4 gap-3">
          {[
            { label: "Общая выручка", value: "74 800 000 ₸", change: "+23.4%" },
            { label: "Средний чек", value: "388 000 ₸", change: "+8.2%" },
            { label: "Конверсия", value: "3.8%", change: "+0.4%" },
            { label: "LTV клиента", value: "1 240 000 ₸", change: "+15.1%" },
          ].map((k) => (
            <div key={k.label} className="bg-white rounded-xl p-5 border border-black/5">
              <p className="text-xs text-black/40 mb-2">{k.label}</p>
              <p className="text-2xl text-black mb-1">{k.value}</p>
              <span className="text-xs text-emerald-600">{k.change} vs. прошлый год</span>
            </div>
          ))}
        </div>

        {/* Revenue + Orders */}
        <div className="grid grid-cols-3 gap-4">
          <div className="col-span-2 bg-white rounded-2xl p-6 border border-black/5">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-black">Выручка и заказы</h2>
                <p className="text-xs text-black/40 mt-0.5">За 2026 год</p>
              </div>
              <div className="flex items-center gap-4 text-xs text-black/40">
                <span className="flex items-center gap-1.5">
                  <span className="w-4 h-0.5 bg-black inline-block" />
                  Выручка
                </span>
                <span className="flex items-center gap-1.5">
                  <span className="w-4 h-0.5 bg-black/30 inline-block" />
                  Заказы
                </span>
              </div>
            </div>
            <ResponsiveContainer width="100%" height={220}>
              <LineChart data={monthlyData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#00000008" />
                <XAxis dataKey="month" tick={{ fontSize: 11, fill: "#00000060" }} axisLine={false} tickLine={false} />
                <YAxis yAxisId="left" tick={{ fontSize: 11, fill: "#00000060" }} axisLine={false} tickLine={false} tickFormatter={(v) => `${(v / 1000000).toFixed(0)}M`} />
                <YAxis yAxisId="right" orientation="right" tick={{ fontSize: 11, fill: "#00000060" }} axisLine={false} tickLine={false} />
                <Tooltip
                  contentStyle={{ background: "#000", border: "none", borderRadius: "8px", color: "#fff", fontSize: "12px" }}
                  labelStyle={{ color: "#ffffff80" }}
                />
                <Line yAxisId="left" type="monotone" dataKey="revenue" stroke="#000" strokeWidth={2} dot={false} />
                <Line yAxisId="right" type="monotone" dataKey="orders" stroke="#00000040" strokeWidth={2} dot={false} strokeDasharray="4 4" />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Pie */}
          <div className="bg-white rounded-2xl p-6 border border-black/5">
            <div className="mb-4">
              <h2 className="text-black">Категории</h2>
              <p className="text-xs text-black/40 mt-0.5">Доля продаж</p>
            </div>
            <ResponsiveContainer width="100%" height={160}>
              <PieChart>
                <Pie
                  data={categoryPie}
                  cx="50%"
                  cy="50%"
                  innerRadius={50}
                  outerRadius={75}
                  paddingAngle={2}
                  dataKey="value"
                >
                  {categoryPie.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  formatter={(v: number) => [`${v}%`, "Доля"]}
                  contentStyle={{ background: "#000", border: "none", borderRadius: "8px", color: "#fff", fontSize: "12px" }}
                />
              </PieChart>
            </ResponsiveContainer>
            <div className="mt-3 space-y-1.5">
              {categoryPie.map((c) => (
                <div key={c.name} className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full" style={{ backgroundColor: c.color }} />
                    <span className="text-xs text-black/60">{c.name}</span>
                  </div>
                  <span className="text-xs text-black">{c.value}%</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Cities + Conversion */}
        <div className="grid grid-cols-2 gap-4">
          {/* City breakdown */}
          <div className="bg-white rounded-2xl p-6 border border-black/5">
            <div className="mb-6">
              <h2 className="text-black">По городам</h2>
              <p className="text-xs text-black/40 mt-0.5">Заказы и выручка</p>
            </div>
            <div className="space-y-3">
              {cityData.map((city) => {
                const pct = Math.round((city.orders / 1493) * 100);
                return (
                  <div key={city.city}>
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm text-black">{city.city}</span>
                      <div className="flex items-center gap-3">
                        <span className="text-xs text-black/40">{city.orders} зак.</span>
                        <span className="text-xs text-black">{(city.revenue / 1000000).toFixed(0)} М ₸</span>
                      </div>
                    </div>
                    <div className="h-1.5 bg-black/5 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-black rounded-full transition-all duration-500"
                        style={{ width: `${pct}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Weekly conversion */}
          <div className="bg-white rounded-2xl p-6 border border-black/5">
            <div className="mb-6">
              <h2 className="text-black">Трафик и конверсия</h2>
              <p className="text-xs text-black/40 mt-0.5">Последние 7 дней</p>
            </div>
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={conversionData} barSize={16} barGap={4}>
                <CartesianGrid strokeDasharray="3 3" stroke="#00000008" />
                <XAxis dataKey="day" tick={{ fontSize: 11, fill: "#00000060" }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 11, fill: "#00000060" }} axisLine={false} tickLine={false} />
                <Tooltip
                  contentStyle={{ background: "#000", border: "none", borderRadius: "8px", color: "#fff", fontSize: "12px" }}
                  labelStyle={{ color: "#ffffff80" }}
                />
                <Bar dataKey="visits" fill="#00000015" radius={[3, 3, 0, 0]} name="Посетители" />
                <Bar dataKey="orders" fill="#000" radius={[3, 3, 0, 0]} name="Заказы" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </main>
    </div>
  );
}
