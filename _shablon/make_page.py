"""Собирает страницу товара из шаблона.
Запуск:  python _shablon/make_page.py shtativ
Берёт Сайт/<папка>/tovar.json + _shablon/index.html -> пишет Сайт/<папка>/index.html.
"tugmalar": по одной кнопке на каждый магазин, где товар есть
  {"turi": "uzum" | "wb" | "ozon" (цвет), "nomi": подпись, "izoh": мелкая строка (цена), "url": ссылка}.
Две Uzum-кнопки различаются подписью: «Uzum Market — Ireezq», «Uzum Market — SelectionTime».
Список пустой -> «скоро снова в наличии».
"""
import html, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def build(folder: str) -> pathlib.Path:
    d = ROOT / folder
    t = json.loads((d / "tovar.json").read_text(encoding="utf-8"))
    e = html.escape
    imgs = "\n".join(
        f'    <img src="{e(r)}" alt="{e(t["nomi"])}" {"" if i == 0 else "loading=\"lazy\" "}width="540" height="720">'
        for i, r in enumerate(t["rasmlar"])
    )
    hint = '  <p class="hint">← Rasmlarni suring →</p>' if len(t["rasmlar"]) > 1 else ""
    facts = "\n".join(f"    <li>{e(x)}</li>" for x in t.get("afzalliklar", []))
    # Своя кнопка на каждый магазин, где товар есть. Нет товара -> убрать строку из "tugmalar".
    btns = [
        f'    <a class="btn {e(b["turi"])}" href="{e(b["url"])}" rel="nofollow">{e(b["nomi"])}'
        f'<small>{e(b.get("izoh") or "Buyurtma berish")}</small></a>'
        for b in t.get("tugmalar", []) if b.get("url")
    ]
    soon = "" if btns else '  <p class="soon">Tez orada yana sotuvda bo‘ladi</p>'
    out = (ROOT / "_shablon" / "index.html").read_text(encoding="utf-8")
    for key, val in {
        "{{NOMI}}": e(t["nomi"]), "{{QISQA}}": e(t.get("qisqa", "")),
        "{{RASM1}}": e(t["rasmlar"][0]), "{{RASMLAR}}": imgs, "{{HINT}}": hint,"{{AFZALLIKLAR}}": facts,
        "{{NARX}}": e(t.get("narx", "")), "{{ESKI_NARX}}": e(t.get("eski_narx", "")),
        "{{TUGMALAR}}": "\n".join(btns), "{{TUGADI}}": soon,
    }.items():
        out = out.replace(key, val)
    p = d / "index.html"
    p.write_text(out, encoding="utf-8")
    return p


if __name__ == "__main__":
    for f in sys.argv[1:]:
        print("OK", build(f))
