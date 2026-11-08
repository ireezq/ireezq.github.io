"""Собирает страницу товара из шаблона.
Запуск:  py -3 _shablon/make_page.py shtativ massajyor ...
Берёт Сайт/<папка>/tovar.json + _shablon/index.html -> пишет Сайт/<папка>/index.html.

Цены на странице НЕ показываем (решение пользователя: в магазинах цена со скидкой меняется).
tovar.json:
  "nomi"        — название (узбекский, коротко)
  "qisqa"       — одно предложение для описания ссылки
  "rasmlar"     — фото (первое — главное)
  "afzalliklar" — 3 коротких пункта
  "tugmalar"    — по одной кнопке на каждый магазин, где товар есть:
                  {"nomi": "Uzum Market — Ireezq", "url": "..."}
                  Первая кнопка — залитая (главная), остальные — контурные.
                  Две Uzum-кнопки различаются подписью. Товара нет -> убрать кнопку.
                  Список пустой -> «скоро снова в продаже».
"""
import html, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def build(folder: str) -> pathlib.Path:
    d = ROOT / folder
    t = json.loads((d / "tovar.json").read_text(encoding="utf-8"))
    e = html.escape
    imgs = "\n".join(
        f'    <img src="{e(r)}" alt="{e(t["nomi"])}"{"" if i == 0 else " loading=\"lazy\""} width="540" height="720">'
        for i, r in enumerate(t["rasmlar"])
    )
    n = len(t["rasmlar"])
    dots = ('  <div class="dots">' + "".join('<i class="on"></i>' if i == 0 else "<i></i>" for i in range(n)) + "</div>") if n > 1 else ""
    facts = "\n".join(f"    <li>{e(x)}</li>" for x in t.get("afzalliklar", [])[:3])
    links = [b for b in t.get("tugmalar", []) if b.get("url")]
    if links:
        btns = "\n".join(
            f'    <a class="btn{" main" if i == 0 else ""}" href="{e(b["url"])}" rel="nofollow">{e(b["nomi"])}</a>'
            for i, b in enumerate(links)
        )
        buttons = f'  <p class="label">Qayerdan buyurtma berish</p>\n  <div class="buttons">\n{btns}\n  </div>'
    else:
        buttons = '  <p class="soon">Tez orada yana sotuvda bo‘ladi</p>'
    out = (ROOT / "_shablon" / "index.html").read_text(encoding="utf-8")
    for key, val in {
        "{{NOMI}}": e(t["nomi"]), "{{QISQA}}": e(t.get("qisqa", "")),
        "{{RASM1}}": e(t["rasmlar"][0]), "{{RASMLAR}}": imgs, "{{DOTS}}": dots,
        "{{AFZALLIKLAR}}": facts, "{{TUGMALAR}}": buttons,
    }.items():
        out = out.replace(key, val)
    p = d / "index.html"
    p.write_text(out, encoding="utf-8")
    return p


if __name__ == "__main__":
    for f in sys.argv[1:]:
        print("OK", build(f))
