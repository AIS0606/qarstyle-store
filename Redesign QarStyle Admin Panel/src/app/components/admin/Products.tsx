import { useState } from "react";
import { Header } from "./Header";
import { Search, Plus, Edit2, Trash2, Eye, SlidersHorizontal } from "lucide-react";

import imgProduct1 from "figma:asset/c464a2e3f7f0901869f0d0893911e6309c80e890.png";
import imgProduct2 from "figma:asset/885442841d323cce8f1c64a4da2be84e7adc3cbf.png";
import imgProduct3 from "figma:asset/3f5e97f522f9668871004167ad76030b615a048a.png";
import imgProduct4 from "figma:asset/35b7a066f5247f6aad11fed6b12f4a58183354c1.png";
import imgProduct5 from "figma:asset/95870c5356cdfb39d4a4d7986756d7cbc1f69a0f.png";
import imgProduct6 from "figma:asset/36195c588e21eb7c73fee8e90dc188f2f6384f02.png";
import imgProduct7 from "figma:asset/8bffd3232dcd004a165eeb797dec838b142efb4b.png";
import imgProduct8 from "figma:asset/f5abd315713b8c39754c8910f10630b935f8bd1f.png";

const products = [
  {
    id: 1,
    name: "Rainforest Next Summer Anorak Jacket",
    sku: "QS-ANJ-001",
    category: "Мужской",
    price: "455 000 ₸",
    stock: 47,
    status: "В наличии",
    sold: 247,
    img: imgProduct1,
  },
  {
    id: 2,
    name: "Raincape Anorak Jacket Beige",
    sku: "QS-RAJ-002",
    category: "Женский",
    price: "393 000 ₸",
    stock: 31,
    status: "В наличии",
    sold: 198,
    img: imgProduct2,
  },
  {
    id: 3,
    name: "Rainforest Dune Anorak Beige",
    sku: "QS-RDA-003",
    category: "Мужской",
    price: "360 000 ₸",
    stock: 22,
    status: "Мало",
    sold: 163,
    img: imgProduct3,
  },
  {
    id: 4,
    name: "Traveler Jacket Blue Academy",
    sku: "QS-TJB-004",
    category: "Мужской",
    price: "320 000 ₸",
    stock: 0,
    status: "Нет",
    sold: 142,
    img: imgProduct4,
  },
  {
    id: 5,
    name: "Rainforest Next Summer (Brown 2)",
    sku: "QS-ANJ-005",
    category: "Унисекс",
    price: "455 000 ₸",
    stock: 19,
    status: "Мало",
    sold: 87,
    img: imgProduct5,
  },
  {
    id: 6,
    name: "Raincape Anorak Jacket Beige 2",
    sku: "QS-RAJ-006",
    category: "Женский",
    price: "393 000 ₸",
    stock: 55,
    status: "В наличии",
    sold: 76,
    img: imgProduct6,
  },
  {
    id: 7,
    name: "Rainforest Anorak Brown 3",
    sku: "QS-RAB-007",
    category: "Унисекс",
    price: "455 000 ₸",
    stock: 33,
    status: "В наличии",
    sold: 64,
    img: imgProduct7,
  },
  {
    id: 8,
    name: "Traveler Jacket Blue 2",
    sku: "QS-TJB-008",
    category: "Мужской",
    price: "320 000 ₸",
    stock: 8,
    status: "Мало",
    sold: 51,
    img: imgProduct8,
  },
];

const stockColors: Record<string, string> = {
  "В наличии": "bg-black text-white",
  Мало: "bg-amber-50 text-amber-700",
  Нет: "bg-red-50 text-red-500",
};

const categories = ["Все", "Мужской", "Женский", "Детский", "Унисекс"];
const views = ["grid", "list"] as const;

export function Products() {
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("Все");
  const [view, setView] = useState<"grid" | "list">("list");

  const filtered = products.filter((p) => {
    const matchSearch =
      p.name.toLowerCase().includes(search.toLowerCase()) ||
      p.sku.toLowerCase().includes(search.toLowerCase());
    const matchCat = category === "Все" || p.category === category;
    return matchSearch && matchCat;
  });

  return (
    <div className="flex-1 flex flex-col min-h-screen bg-[#f8f8f8]">
      <Header title="Товары" subtitle="Управление каталогом продукции" />

      <main className="flex-1 p-8 space-y-6">
        {/* Stats */}
        <div className="grid grid-cols-4 gap-3">
          {[
            { label: "Всего товаров", value: "342" },
            { label: "В наличии", value: "287" },
            { label: "Мало на складе", value: "38" },
            { label: "Нет в наличии", value: "17" },
          ].map((s) => (
            <div key={s.label} className="bg-white rounded-xl p-4 border border-black/5">
              <p className="text-xs text-black/40 mb-1">{s.label}</p>
              <p className="text-2xl text-black">{s.value}</p>
            </div>
          ))}
        </div>

        {/* Main Table */}
        <div className="bg-white rounded-2xl border border-black/5">
          {/* Toolbar */}
          <div className="flex items-center gap-3 p-5 border-b border-black/5">
            <div className="flex items-center gap-2 bg-black/5 rounded-full px-4 py-2 flex-1 max-w-xs">
              <Search className="w-3.5 h-3.5 text-black/40 shrink-0" />
              <input
                type="text"
                placeholder="Поиск товара..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="bg-transparent text-sm text-black placeholder:text-black/40 outline-none w-full"
              />
            </div>

            <div className="flex gap-1">
              {categories.map((c) => (
                <button
                  key={c}
                  onClick={() => setCategory(c)}
                  className={`px-3 py-1.5 rounded-full text-xs transition-colors ${
                    category === c
                      ? "bg-black text-white"
                      : "bg-black/5 text-black/50 hover:bg-black/10"
                  }`}
                >
                  {c}
                </button>
              ))}
            </div>

            <div className="ml-auto flex items-center gap-2">
              {/* View toggle */}
              <div className="flex rounded-full bg-black/5 p-0.5">
                {views.map((v) => (
                  <button
                    key={v}
                    onClick={() => setView(v)}
                    className={`px-3 py-1 rounded-full text-xs transition-colors ${
                      view === v ? "bg-black text-white" : "text-black/40"
                    }`}
                  >
                    {v === "grid" ? "Карточки" : "Список"}
                  </button>
                ))}
              </div>

              <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs bg-black/5 text-black/50 hover:bg-black/10 transition-colors">
                <SlidersHorizontal className="w-3 h-3" />
                Фильтры
              </button>

              <button className="flex items-center gap-1.5 px-4 py-1.5 rounded-full text-xs bg-black text-white hover:bg-black/80 transition-colors">
                <Plus className="w-3 h-3" />
                Добавить
              </button>
            </div>
          </div>

          {view === "list" ? (
            <>
              <table className="w-full">
                <thead>
                  <tr className="border-b border-black/5">
                    <th className="text-left text-xs text-black/30 font-normal px-5 py-3">Товар</th>
                    <th className="text-left text-xs text-black/30 font-normal px-3 py-3">SKU</th>
                    <th className="text-left text-xs text-black/30 font-normal px-3 py-3">Категория</th>
                    <th className="text-left text-xs text-black/30 font-normal px-3 py-3">Продано</th>
                    <th className="text-left text-xs text-black/30 font-normal px-3 py-3">Остаток</th>
                    <th className="text-left text-xs text-black/30 font-normal px-3 py-3">Статус</th>
                    <th className="text-right text-xs text-black/30 font-normal px-5 py-3">Цена</th>
                    <th className="px-5 py-3" />
                  </tr>
                </thead>
                <tbody className="divide-y divide-black/5">
                  {filtered.map((product) => (
                    <tr
                      key={product.id}
                      className="hover:bg-black/[0.02] transition-colors group"
                    >
                      <td className="px-5 py-3">
                        <div className="flex items-center gap-3">
                          <div className="w-10 h-10 rounded-lg overflow-hidden bg-[#f0f0f0] shrink-0">
                            <img
                              src={product.img}
                              alt={product.name}
                              className="w-full h-full object-cover mix-blend-multiply"
                            />
                          </div>
                          <p className="text-sm text-black max-w-[220px] truncate">
                            {product.name}
                          </p>
                        </div>
                      </td>
                      <td className="px-3 py-3">
                        <span className="text-xs text-black/40 font-mono">{product.sku}</span>
                      </td>
                      <td className="px-3 py-3">
                        <span className="text-sm text-black/60">{product.category}</span>
                      </td>
                      <td className="px-3 py-3">
                        <span className="text-sm text-black">{product.sold} шт.</span>
                      </td>
                      <td className="px-3 py-3">
                        <span
                          className={`text-sm ${
                            product.stock === 0
                              ? "text-red-500"
                              : product.stock < 20
                                ? "text-amber-600"
                                : "text-black"
                          }`}
                        >
                          {product.stock}
                        </span>
                      </td>
                      <td className="px-3 py-3">
                        <span
                          className={`text-xs px-2.5 py-1 rounded-full ${stockColors[product.status]}`}
                        >
                          {product.status}
                        </span>
                      </td>
                      <td className="px-5 py-3 text-right">
                        <span className="text-sm text-black">{product.price}</span>
                      </td>
                      <td className="px-5 py-3">
                        <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                          <button className="w-7 h-7 rounded-full bg-black/5 hover:bg-black/10 flex items-center justify-center">
                            <Eye className="w-3 h-3 text-black/40" />
                          </button>
                          <button className="w-7 h-7 rounded-full bg-black/5 hover:bg-black/10 flex items-center justify-center">
                            <Edit2 className="w-3 h-3 text-black/40" />
                          </button>
                          <button className="w-7 h-7 rounded-full bg-red-50 hover:bg-red-100 flex items-center justify-center">
                            <Trash2 className="w-3 h-3 text-red-400" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </>
          ) : (
            <div className="p-5 grid grid-cols-4 gap-4">
              {filtered.map((product) => (
                <div
                  key={product.id}
                  className="border border-black/5 rounded-xl overflow-hidden hover:border-black/20 transition-colors group"
                >
                  <div className="aspect-square bg-[#f0f0f0] overflow-hidden">
                    <img
                      src={product.img}
                      alt={product.name}
                      className="w-full h-full object-cover mix-blend-multiply group-hover:scale-105 transition-transform duration-300"
                    />
                  </div>
                  <div className="p-3">
                    <p className="text-sm text-black truncate mb-1">{product.name}</p>
                    <p className="text-xs text-black/40 mb-2">{product.sku}</p>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-black">{product.price}</span>
                      <span
                        className={`text-xs px-2 py-0.5 rounded-full ${stockColors[product.status]}`}
                      >
                        {product.status}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          <div className="flex items-center justify-between px-5 py-4 border-t border-black/5">
            <span className="text-xs text-black/30">
              Показано {filtered.length} из 342 товаров
            </span>
            <div className="flex gap-1">
              {[1, 2, 3, "...", 43].map((p, i) => (
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