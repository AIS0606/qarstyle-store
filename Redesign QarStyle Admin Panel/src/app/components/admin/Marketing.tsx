import { Header } from "./Header";
import { Plus, Tag, Percent, Gift, Send, Users, TrendingUp } from "lucide-react";

const promos = [
  {
    code: "SUMMER26",
    type: "Процент",
    value: "15%",
    used: 47,
    limit: 100,
    expiry: "31 июля 2026",
    status: "Активен",
  },
  {
    code: "WELCOME",
    type: "Фиксированная",
    value: "5 000 ₸",
    used: 234,
    limit: 500,
    expiry: "Бессрочно",
    status: "Активен",
  },
  {
    code: "VIP2026",
    type: "Процент",
    value: "20%",
    used: 89,
    limit: 200,
    expiry: "31 декабря 2026",
    status: "Активен",
  },
  {
    code: "SPRING25",
    type: "Процент",
    value: "10%",
    used: 312,
    limit: 300,
    expiry: "30 апреля 2025",
    status: "Истёк",
  },
];

const campaigns = [
  {
    name: "Летняя коллекция 2026",
    type: "Email",
    sent: 3240,
    opened: 1247,
    clicks: 389,
    orders: 67,
    status: "Отправлено",
  },
  {
    name: "Новинки мужской",
    type: "Push",
    sent: 1840,
    opened: 892,
    clicks: 234,
    orders: 41,
    status: "Отправлено",
  },
  {
    name: "VIP предложение",
    type: "Email",
    sent: 127,
    opened: 98,
    clicks: 72,
    orders: 28,
    status: "Запланировано",
  },
];

const statusColors: Record<string, string> = {
  Активен: "bg-black text-white",
  Истёк: "bg-black/10 text-black/40",
  Запланировано: "bg-amber-50 text-amber-700",
  Отправлено: "bg-black text-white",
};

export function Marketing() {
  return (
    <div className="flex-1 flex flex-col min-h-screen bg-[#f8f8f8]">
      <Header title="Маркетинг" subtitle="Промо-коды, рассылки и кампании" />

      <main className="flex-1 p-8 space-y-6">
        {/* Stats */}
        <div className="grid grid-cols-4 gap-3">
          {[
            { icon: Tag, label: "Промо-коды", value: "12 активных", color: "bg-black" },
            { icon: Percent, label: "Использований", value: "682", color: "bg-black" },
            { icon: Send, label: "Рассылок", value: "24 отправлено", color: "bg-black" },
            { icon: Users, label: "Охват", value: "8 420 чел.", color: "bg-black" },
          ].map((s) => {
            const Icon = s.icon;
            return (
              <div key={s.label} className="bg-white rounded-xl p-5 border border-black/5">
                <div className="w-9 h-9 rounded-xl bg-black flex items-center justify-center mb-3">
                  <Icon className="w-4 h-4 text-white" />
                </div>
                <p className="text-xs text-black/40">{s.label}</p>
                <p className="text-xl text-black mt-1">{s.value}</p>
              </div>
            );
          })}
        </div>

        <div className="grid grid-cols-2 gap-4">
          {/* Promo codes */}
          <div className="bg-white rounded-2xl border border-black/5">
            <div className="flex items-center justify-between p-5 border-b border-black/5">
              <div>
                <h2 className="text-black">Промо-коды</h2>
                <p className="text-xs text-black/40 mt-0.5">Скидочные коды</p>
              </div>
              <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs bg-black text-white hover:bg-black/80 transition-colors">
                <Plus className="w-3 h-3" />
                Создать
              </button>
            </div>
            <div className="divide-y divide-black/5">
              {promos.map((promo) => (
                <div key={promo.code} className="px-5 py-4 hover:bg-black/[0.02] transition-colors">
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-sm text-black bg-black/5 px-2 py-0.5 rounded">
                        {promo.code}
                      </span>
                      <span
                        className={`text-xs px-2 py-0.5 rounded-full ${statusColors[promo.status]}`}
                      >
                        {promo.status}
                      </span>
                    </div>
                    <span className="text-sm text-black">{promo.value}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <div className="h-1 bg-black/5 rounded-full overflow-hidden w-32">
                          <div
                            className="h-full bg-black rounded-full"
                            style={{ width: `${(promo.used / promo.limit) * 100}%` }}
                          />
                        </div>
                        <span className="text-xs text-black/40">
                          {promo.used}/{promo.limit}
                        </span>
                      </div>
                      <p className="text-xs text-black/30">До: {promo.expiry}</p>
                    </div>
                    <span className="text-xs text-black/30">{promo.type}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Campaigns */}
          <div className="bg-white rounded-2xl border border-black/5">
            <div className="flex items-center justify-between p-5 border-b border-black/5">
              <div>
                <h2 className="text-black">Кампании</h2>
                <p className="text-xs text-black/40 mt-0.5">Email и Push рассылки</p>
              </div>
              <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs bg-black text-white hover:bg-black/80 transition-colors">
                <Plus className="w-3 h-3" />
                Создать
              </button>
            </div>
            <div className="divide-y divide-black/5">
              {campaigns.map((camp) => (
                <div key={camp.name} className="px-5 py-4 hover:bg-black/[0.02] transition-colors">
                  <div className="flex items-start justify-between mb-3">
                    <div>
                      <p className="text-sm text-black">{camp.name}</p>
                      <div className="flex items-center gap-2 mt-0.5">
                        <span className="text-xs text-black/40">{camp.type}</span>
                        <span
                          className={`text-xs px-2 py-0.5 rounded-full ${statusColors[camp.status]}`}
                        >
                          {camp.status}
                        </span>
                      </div>
                    </div>
                    <div className="flex items-center gap-1 text-xs text-emerald-600">
                      <TrendingUp className="w-3 h-3" />
                      <span>{camp.orders} заказов</span>
                    </div>
                  </div>
                  <div className="grid grid-cols-3 gap-2">
                    {[
                      { label: "Отправлено", value: camp.sent },
                      { label: "Открыто", value: camp.opened },
                      { label: "Переходы", value: camp.clicks },
                    ].map((m) => (
                      <div key={m.label} className="bg-black/[0.02] rounded-lg p-2 text-center">
                        <p className="text-sm text-black">{m.value.toLocaleString("ru-RU")}</p>
                        <p className="text-xs text-black/30">{m.label}</p>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Newsletter form placeholder */}
        <div className="bg-white rounded-2xl border border-black/5 p-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-black">Новая рассылка</h2>
              <p className="text-xs text-black/40 mt-0.5">Быстрое создание email-кампании</p>
            </div>
            <Gift className="w-5 h-5 text-black/20" />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-xs text-black/40 block mb-1.5">Тема письма</label>
              <input
                type="text"
                placeholder="Новая коллекция QarStyle..."
                className="w-full bg-black/5 rounded-xl px-4 py-2.5 text-sm text-black placeholder:text-black/30 outline-none focus:bg-black/[0.08] transition-colors"
              />
            </div>
            <div>
              <label className="text-xs text-black/40 block mb-1.5">Сегмент</label>
              <select className="w-full bg-black/5 rounded-xl px-4 py-2.5 text-sm text-black outline-none focus:bg-black/[0.08] transition-colors appearance-none">
                <option>Все клиенты</option>
                <option>VIP клиенты</option>
                <option>Постоянные</option>
                <option>Новые</option>
              </select>
            </div>
          </div>
          <div className="mt-3">
            <label className="text-xs text-black/40 block mb-1.5">Содержание</label>
            <textarea
              placeholder="Текст рассылки..."
              rows={3}
              className="w-full bg-black/5 rounded-xl px-4 py-2.5 text-sm text-black placeholder:text-black/30 outline-none focus:bg-black/[0.08] transition-colors resize-none"
            />
          </div>
          <div className="flex items-center justify-end gap-2 mt-3">
            <button className="px-4 py-2 rounded-full text-xs bg-black/5 text-black/50 hover:bg-black/10 transition-colors">
              Предпросмотр
            </button>
            <button className="flex items-center gap-1.5 px-4 py-2 rounded-full text-xs bg-black text-white hover:bg-black/80 transition-colors">
              <Send className="w-3 h-3" />
              Отправить
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}
