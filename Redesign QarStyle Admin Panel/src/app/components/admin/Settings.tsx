import { useState } from "react";
import { Header } from "./Header";
import { Save, Globe, Bell, Shield, CreditCard, Truck, Store } from "lucide-react";

const tabs = [
  { id: "store", label: "Магазин", icon: Store },
  { id: "shipping", label: "Доставка", icon: Truck },
  { id: "payments", label: "Оплата", icon: CreditCard },
  { id: "notifications", label: "Уведомления", icon: Bell },
  { id: "security", label: "Безопасность", icon: Shield },
];

export function Settings() {
  const [activeTab, setActiveTab] = useState("store");
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="flex-1 flex flex-col min-h-screen bg-[#f8f8f8]">
      <Header title="Настройки" subtitle="Конфигурация магазина QarStyle" />

      <main className="flex-1 p-8">
        <div className="grid grid-cols-4 gap-6">
          {/* Tab sidebar */}
          <div className="bg-white rounded-2xl border border-black/5 p-3 h-fit">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-left transition-colors mb-0.5 ${
                    activeTab === tab.id
                      ? "bg-black text-white"
                      : "text-black/50 hover:bg-black/5 hover:text-black"
                  }`}
                >
                  <Icon
                    className={`w-4 h-4 shrink-0 ${activeTab === tab.id ? "text-white" : "text-black/30"}`}
                  />
                  <span className="text-sm">{tab.label}</span>
                </button>
              );
            })}
          </div>

          {/* Content */}
          <div className="col-span-3 space-y-4">
            {activeTab === "store" && (
              <>
                <div className="bg-white rounded-2xl border border-black/5 p-6">
                  <h2 className="text-black mb-6">Основная информация</h2>
                  <div className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="text-xs text-black/40 block mb-1.5">
                          Название магазина
                        </label>
                        <input
                          type="text"
                          defaultValue="QarStyle"
                          className="w-full bg-black/5 rounded-xl px-4 py-2.5 text-sm text-black outline-none focus:bg-black/[0.08] transition-colors"
                        />
                      </div>
                      <div>
                        <label className="text-xs text-black/40 block mb-1.5">Email</label>
                        <input
                          type="email"
                          defaultValue="info@qarstyle.kz"
                          className="w-full bg-black/5 rounded-xl px-4 py-2.5 text-sm text-black outline-none focus:bg-black/[0.08] transition-colors"
                        />
                      </div>
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="text-xs text-black/40 block mb-1.5">Телефон</label>
                        <input
                          type="tel"
                          defaultValue="+7 (727) 123-45-67"
                          className="w-full bg-black/5 rounded-xl px-4 py-2.5 text-sm text-black outline-none focus:bg-black/[0.08] transition-colors"
                        />
                      </div>
                      <div>
                        <label className="text-xs text-black/40 block mb-1.5">Сайт</label>
                        <input
                          type="url"
                          defaultValue="https://qarstyle.kz"
                          className="w-full bg-black/5 rounded-xl px-4 py-2.5 text-sm text-black outline-none focus:bg-black/[0.08] transition-colors"
                        />
                      </div>
                    </div>
                    <div>
                      <label className="text-xs text-black/40 block mb-1.5">Адрес</label>
                      <input
                        type="text"
                        defaultValue="г. Алматы, ул. Панфилова 98"
                        className="w-full bg-black/5 rounded-xl px-4 py-2.5 text-sm text-black outline-none focus:bg-black/[0.08] transition-colors"
                      />
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-2xl border border-black/5 p-6">
                  <div className="flex items-center gap-2 mb-6">
                    <Globe className="w-4 h-4 text-black/40" />
                    <h2 className="text-black">Локализация</h2>
                  </div>
                  <div className="grid grid-cols-3 gap-4">
                    <div>
                      <label className="text-xs text-black/40 block mb-1.5">Валюта</label>
                      <select className="w-full bg-black/5 rounded-xl px-4 py-2.5 text-sm text-black outline-none appearance-none">
                        <option>Тенге (₸)</option>
                        <option>USD ($)</option>
                        <option>RUB (₽)</option>
                      </select>
                    </div>
                    <div>
                      <label className="text-xs text-black/40 block mb-1.5">Язык</label>
                      <select className="w-full bg-black/5 rounded-xl px-4 py-2.5 text-sm text-black outline-none appearance-none">
                        <option>Русский</option>
                        <option>Қазақша</option>
                        <option>English</option>
                      </select>
                    </div>
                    <div>
                      <label className="text-xs text-black/40 block mb-1.5">Часовой пояс</label>
                      <select className="w-full bg-black/5 rounded-xl px-4 py-2.5 text-sm text-black outline-none appearance-none">
                        <option>UTC+5 (Алматы)</option>
                        <option>UTC+6 (Астана)</option>
                      </select>
                    </div>
                  </div>
                </div>
              </>
            )}

            {activeTab === "shipping" && (
              <div className="bg-white rounded-2xl border border-black/5 p-6">
                <h2 className="text-black mb-6">Условия доставки</h2>
                <div className="space-y-4">
                  {[
                    { name: "Стандартная доставка", price: "2 000 ₸", days: "3-5 дней", active: true },
                    { name: "Экспресс доставка", price: "5 000 ₸", days: "1-2 дня", active: true },
                    { name: "Самовывоз", price: "Бесплатно", days: "Сегодня", active: true },
                    { name: "Международная доставка", price: "15 000 ₸", days: "7-14 дней", active: false },
                  ].map((method) => (
                    <div
                      key={method.name}
                      className="flex items-center justify-between p-4 bg-black/[0.02] rounded-xl"
                    >
                      <div>
                        <p className="text-sm text-black">{method.name}</p>
                        <p className="text-xs text-black/40 mt-0.5">{method.days}</p>
                      </div>
                      <div className="flex items-center gap-4">
                        <span className="text-sm text-black">{method.price}</span>
                        <div
                          className={`w-10 h-5 rounded-full relative cursor-pointer transition-colors ${
                            method.active ? "bg-black" : "bg-black/20"
                          }`}
                        >
                          <div
                            className={`absolute top-0.5 w-4 h-4 bg-white rounded-full shadow transition-all ${
                              method.active ? "left-[22px]" : "left-0.5"
                            }`}
                          />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="mt-4 p-4 bg-black/[0.02] rounded-xl">
                  <p className="text-sm text-black mb-1">Бесплатная доставка от:</p>
                  <div className="flex items-center gap-3">
                    <input
                      type="number"
                      defaultValue="50000"
                      className="bg-white rounded-xl px-4 py-2 text-sm text-black outline-none border border-black/10 w-36"
                    />
                    <span className="text-sm text-black/40">₸</span>
                  </div>
                </div>
              </div>
            )}

            {activeTab === "payments" && (
              <div className="bg-white rounded-2xl border border-black/5 p-6">
                <h2 className="text-black mb-6">Способы оплаты</h2>
                <div className="space-y-3">
                  {[
                    { name: "Kaspi Pay", connected: true, icon: "💳" },
                    { name: "Visa / Mastercard", connected: true, icon: "💳" },
                    { name: "Наличными при получении", connected: true, icon: "💵" },
                    { name: "PayPal", connected: false, icon: "🌐" },
                    { name: "Halyk Bank", connected: false, icon: "🏦" },
                  ].map((pm) => (
                    <div
                      key={pm.name}
                      className="flex items-center justify-between p-4 bg-black/[0.02] rounded-xl"
                    >
                      <div className="flex items-center gap-3">
                        <span className="text-lg">{pm.icon}</span>
                        <div>
                          <p className="text-sm text-black">{pm.name}</p>
                          <p className="text-xs text-black/40">
                            {pm.connected ? "Подключено" : "Не подключено"}
                          </p>
                        </div>
                      </div>
                      <div
                        className={`w-10 h-5 rounded-full relative cursor-pointer transition-colors ${
                          pm.connected ? "bg-black" : "bg-black/20"
                        }`}
                      >
                        <div
                          className={`absolute top-0.5 w-4 h-4 bg-white rounded-full shadow transition-all ${
                            pm.connected ? "left-[22px]" : "left-0.5"
                          }`}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === "notifications" && (
              <div className="bg-white rounded-2xl border border-black/5 p-6">
                <h2 className="text-black mb-6">Настройки уведомлений</h2>
                <div className="space-y-3">
                  {[
                    { label: "Новые заказы", sub: "Мгновенные уведомления о новых заказах", active: true },
                    { label: "Изменение статуса", sub: "Уведомления об изменении статуса заказа", active: true },
                    { label: "Низкий остаток", sub: "Когда товар заканчивается на складе", active: true },
                    { label: "Новые клиенты", sub: "Регистрация нового пользователя", active: false },
                    { label: "Отменённые заказы", sub: "При отмене заказа клиентом", active: true },
                    { label: "Ежедневный отчёт", sub: "Сводка за день на email", active: false },
                  ].map((notif) => (
                    <div key={notif.label} className="flex items-center justify-between p-4 bg-black/[0.02] rounded-xl">
                      <div>
                        <p className="text-sm text-black">{notif.label}</p>
                        <p className="text-xs text-black/40 mt-0.5">{notif.sub}</p>
                      </div>
                      <div className={`w-10 h-5 rounded-full relative cursor-pointer transition-colors ${notif.active ? "bg-black" : "bg-black/20"}`}>
                        <div className={`absolute top-0.5 w-4 h-4 bg-white rounded-full shadow transition-all ${notif.active ? "left-[22px]" : "left-0.5"}`} />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === "security" && (
              <div className="bg-white rounded-2xl border border-black/5 p-6">
                <h2 className="text-black mb-6">Безопасность</h2>
                <div className="space-y-4">
                  <div>
                    <label className="text-xs text-black/40 block mb-1.5">Текущий пароль</label>
                    <input type="password" className="w-full bg-black/5 rounded-xl px-4 py-2.5 text-sm text-black outline-none focus:bg-black/[0.08] transition-colors" placeholder="••••••••" />
                  </div>
                  <div>
                    <label className="text-xs text-black/40 block mb-1.5">Новый пароль</label>
                    <input type="password" className="w-full bg-black/5 rounded-xl px-4 py-2.5 text-sm text-black outline-none focus:bg-black/[0.08] transition-colors" placeholder="••••••••" />
                  </div>
                  <div>
                    <label className="text-xs text-black/40 block mb-1.5">Подтвердите пароль</label>
                    <input type="password" className="w-full bg-black/5 rounded-xl px-4 py-2.5 text-sm text-black outline-none focus:bg-black/[0.08] transition-colors" placeholder="••••••••" />
                  </div>
                  <div className="pt-2 flex items-center justify-between p-4 bg-black/[0.02] rounded-xl">
                    <div>
                      <p className="text-sm text-black">Двухфакторная аутентификация</p>
                      <p className="text-xs text-black/40 mt-0.5">Дополнительный уровень защиты</p>
                    </div>
                    <div className="w-10 h-5 rounded-full relative cursor-pointer bg-black/20">
                      <div className="absolute top-0.5 left-0.5 w-4 h-4 bg-white rounded-full shadow" />
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Save button */}
            <div className="flex justify-end">
              <button
                onClick={handleSave}
                className={`flex items-center gap-2 px-6 py-2.5 rounded-full text-sm transition-all ${
                  saved
                    ? "bg-emerald-500 text-white"
                    : "bg-black text-white hover:bg-black/80"
                }`}
              >
                <Save className="w-4 h-4" />
                {saved ? "Сохранено!" : "Сохранить"}
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
