import { useState } from "react";
import { Header } from "./Header";
import { Plus, Edit2, Trash2, ChevronRight } from "lucide-react";

const categories = [
  {
    id: 1,
    name: "Мужской",
    slug: "muzhskoy",
    products: 124,
    subcategories: ["Верхняя одежда", "Куртки", "Ветровки", "Жилеты"],
    sales: "28 400 000 ₸",
    active: true,
  },
  {
    id: 2,
    name: "Женский",
    slug: "zhenskiy",
    products: 98,
    subcategories: ["Верхняя одежда", "Куртки", "Плащи"],
    sales: "19 800 000 ₸",
    active: true,
  },
  {
    id: 3,
    name: "Детский",
    slug: "detskiy",
    products: 47,
    subcategories: ["Куртки", "Комбинезоны", "Жилеты"],
    sales: "9 200 000 ₸",
    active: true,
  },
  {
    id: 4,
    name: "Сумки и снаряжение",
    slug: "bags",
    products: 38,
    subcategories: ["Рюкзаки", "Сумки", "Аксессуары"],
    sales: "7 400 000 ₸",
    active: true,
  },
  {
    id: 5,
    name: "Распродажа",
    slug: "sale",
    products: 22,
    subcategories: ["Мужской sale", "Женский sale"],
    sales: "4 100 000 ₸",
    active: true,
  },
  {
    id: 6,
    name: "Перепродажа",
    slug: "resale",
    products: 13,
    subcategories: ["Лимитированные"],
    sales: "5 900 000 ₸",
    active: false,
  },
];

export function Categories() {
  const [selected, setSelected] = useState<number | null>(null);

  return (
    <div className="flex-1 flex flex-col min-h-screen bg-[#f8f8f8]">
      <Header title="Категории" subtitle="Управление структурой каталога" />

      <main className="flex-1 p-8 space-y-6">
        <div className="grid grid-cols-3 gap-4">
          {/* Categories list */}
          <div className="col-span-1 bg-white rounded-2xl border border-black/5">
            <div className="flex items-center justify-between p-5 border-b border-black/5">
              <h2 className="text-black">Категории</h2>
              <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs bg-black text-white hover:bg-black/80 transition-colors">
                <Plus className="w-3 h-3" />
                Добавить
              </button>
            </div>
            <div className="divide-y divide-black/5">
              {categories.map((cat) => (
                <button
                  key={cat.id}
                  onClick={() => setSelected(cat.id)}
                  className={`w-full flex items-center gap-3 px-5 py-4 text-left hover:bg-black/[0.02] transition-colors ${
                    selected === cat.id ? "bg-black/[0.02]" : ""
                  }`}
                >
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <p className="text-sm text-black">{cat.name}</p>
                      {!cat.active && (
                        <span className="text-xs px-1.5 py-0.5 rounded-full bg-black/5 text-black/30">
                          Скрыт
                        </span>
                      )}
                    </div>
                    <p className="text-xs text-black/40 mt-0.5">{cat.products} товаров</p>
                  </div>
                  <ChevronRight
                    className={`w-4 h-4 transition-colors ${
                      selected === cat.id ? "text-black" : "text-black/20"
                    }`}
                  />
                </button>
              ))}
            </div>
          </div>

          {/* Category detail */}
          <div className="col-span-2 space-y-4">
            {selected ? (
              (() => {
                const cat = categories.find((c) => c.id === selected)!;
                return (
                  <>
                    {/* Info card */}
                    <div className="bg-white rounded-2xl border border-black/5 p-6">
                      <div className="flex items-start justify-between mb-6">
                        <div>
                          <h2 className="text-black mb-1">{cat.name}</h2>
                          <p className="text-xs text-black/40">/{cat.slug}</p>
                        </div>
                        <div className="flex gap-2">
                          <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs bg-black/5 text-black/50 hover:bg-black/10 transition-colors">
                            <Edit2 className="w-3 h-3" />
                            Изменить
                          </button>
                          <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs bg-red-50 text-red-500 hover:bg-red-100 transition-colors">
                            <Trash2 className="w-3 h-3" />
                            Удалить
                          </button>
                        </div>
                      </div>

                      <div className="grid grid-cols-3 gap-4">
                        <div className="p-4 bg-black/[0.02] rounded-xl">
                          <p className="text-xs text-black/40 mb-1">Товаров</p>
                          <p className="text-2xl text-black">{cat.products}</p>
                        </div>
                        <div className="p-4 bg-black/[0.02] rounded-xl">
                          <p className="text-xs text-black/40 mb-1">Подкатегорий</p>
                          <p className="text-2xl text-black">{cat.subcategories.length}</p>
                        </div>
                        <div className="p-4 bg-black/[0.02] rounded-xl">
                          <p className="text-xs text-black/40 mb-1">Продажи</p>
                          <p className="text-lg text-black">{cat.sales}</p>
                        </div>
                      </div>

                      <div className="mt-4 flex items-center justify-between">
                        <span className="text-sm text-black/60">Видимость в каталоге</span>
                        <div
                          className={`w-10 h-5 rounded-full relative cursor-pointer transition-colors ${
                            cat.active ? "bg-black" : "bg-black/20"
                          }`}
                        >
                          <div
                            className={`absolute top-0.5 w-4 h-4 bg-white rounded-full shadow transition-all ${
                              cat.active ? "left-5.5 left-[22px]" : "left-0.5"
                            }`}
                          />
                        </div>
                      </div>
                    </div>

                    {/* Subcategories */}
                    <div className="bg-white rounded-2xl border border-black/5 p-6">
                      <div className="flex items-center justify-between mb-4">
                        <h3 className="text-black">Подкатегории</h3>
                        <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs bg-black/5 text-black/50 hover:bg-black/10 transition-colors">
                          <Plus className="w-3 h-3" />
                          Добавить
                        </button>
                      </div>
                      <div className="space-y-2">
                        {cat.subcategories.map((sub, i) => (
                          <div
                            key={i}
                            className="flex items-center justify-between px-4 py-3 bg-black/[0.02] rounded-xl hover:bg-black/[0.04] transition-colors group"
                          >
                            <span className="text-sm text-black">{sub}</span>
                            <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                              <button className="w-6 h-6 rounded-full bg-white flex items-center justify-center">
                                <Edit2 className="w-3 h-3 text-black/40" />
                              </button>
                              <button className="w-6 h-6 rounded-full bg-white flex items-center justify-center">
                                <Trash2 className="w-3 h-3 text-red-400" />
                              </button>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </>
                );
              })()
            ) : (
              <div className="bg-white rounded-2xl border border-black/5 p-12 flex flex-col items-center justify-center text-center">
                <div className="w-12 h-12 rounded-full bg-black/5 flex items-center justify-center mb-3">
                  <ChevronRight className="w-5 h-5 text-black/20" />
                </div>
                <p className="text-sm text-black/30">Выберите категорию для просмотра деталей</p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
