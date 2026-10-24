import json, html, random
random.seed(11)
E = html.escape

CATS = [
 ("berez", "Берёзовые веники", [
   ("Берёзовый классический", "Плоский, мягкий, держит лист 2–3 бани", 350, None, "in"),
   ("Берёзовый с пижмой", "Пижма даёт горьковатый полевой запах", 420, None, "order"),
   ("Берёзовый «Мягкий»", "Повислая берёза, тонкие ветви без жёстких прутьев", 480, None, "in")]),
 ("dub", "Дубовые веники", [
   ("Дубовый", "Плотный лист, хорошо нагнетает жар", 450, None, "in"),
   ("Дуб и берёза", "Плотность дуба и мягкость берёзы", 520, None, "order"),
   ("Дубовый канадский", "Крупный лист, тяжёлый веник для сильного пара", 590, None, "out")]),
 ("evk", "Эвкалиптовые веники", [
   ("Эвкалипт прутовидный", "Свежий хвойно-мятный запах, для ингаляции", 690, 790, "in"),
   ("Эвкалипт и дуб", "Аромат эвкалипта и упругость дуба", 750, None, "order")]),
 ("mozh", "Можжевеловые веники", [
   ("Можжевеловый", "Колючий, бодрит; запаривать дольше обычного", 650, None, "in"),
   ("Можжевельник и берёза", "Берёза снаружи, можжевельник внутри", 580, None, "order")]),
 ("lipa", "Липовые веники", [
   ("Липовый", "Мягкий, медовый запах, для спокойного пара", 400, None, "in"),
   ("Липа и мята", "Мята добавляет прохлады", 460, None, "out")]),
 ("travy", "Травы и сборы", [
   ("Мята перечная, 50 г", "Для пара и чая", 190, None, "in"),
   ("Чабрец, 50 г", "Тёплый пряный запах", 260, None, "in"),
   ("Банный сбор «Лесной», 100 г", "Хвоя, мята, душица, зверобой", 340, None, "in")]),
 ("chai", "Чай", [
   ("Иван-чай ферментированный, 100 г", "Мягкий, с медовой ноткой", 390, None, "in"),
   ("Таёжный сбор, 100 г", "Чабрец, смородиновый лист, шиповник", 320, None, "order")]),
 ("zap", "Запарки", [
   ("Запарка «Хвойная»", "Саше на один заход", 180, None, "in"),
   ("Запарка «Липа и ромашка»", "Для мягкого пара", 180, None, "in"),
   ("Запарка «Эвкалипт»", "Для дыхания", 210, None, "in")]),
 ("pod", "Подушки", [
   ("Подушка с можжевеловой стружкой", "Лён, 30 × 40 см", 890, None, "in"),
   ("Подушка с травами", "Мята, чабрец, хмель; лён 30 × 40 см", 790, None, "order")]),
 ("aks", "Аксессуары", [
   ("Шапка банная, войлок", "Защищает голову от жара", 650, None, "in"),
   ("Рукавица для парения", "Войлок, на любую руку", 390, None, "in"),
   ("Ковш деревянный", "Ручка не нагревается", 900, None, "out"),
   ("Шайка липовая, 5 л", "Для запаривания веника", 2400, None, "order")]),
]
ST = {"in": "В наличии", "order": "Под заказ", "out": "Нет в наличии"}

def rub(n): return f"{n:,}".replace(",", " ") + " ₽"

items_js = []
bars = []
for ci, (cid, cname, items) in enumerate(CATS):
    rows = []
    for ii, (name, desc, price, old, st) in enumerate(items):
        pid = f"{cid}{ii}"
        items_js.append(dict(id=pid, name=name, price=price, st=st, cat=cname))
        oldh = f'<s>{rub(old)}</s> ' if old else ''
        btn = (f'<button class="add" type="button" data-id="{pid}" aria-label="В корзину: {E(name)}">В корзину</button>'
               if st != "out" else '<span class="add off">Сообщить о поступлении</span>')
        rows.append(f'''<li class="it" data-st="{st}" data-q="{E((name+' '+desc+' '+cname).lower())}">
  <div class="nm"><b>{E(name)}</b><span>{E(desc)}</span><em class="st st-{st}">{ST[st]}</em></div>
  <div class="pr">{oldh}<b>{rub(price)}</b>{btn}</div>
</li>''')
    bars.append(f'''<details class="bar"{' open' if ci==0 else ''}><summary><span>{E(cname)}</span><i aria-hidden="true"></i></summary><ul>{''.join(rows)}</ul></details>''')

# leaves for the broom: a fan of birch leaves below the handle
leaves = []
greens = ["#5f8a3a", "#4c7530", "#79a24a", "#3f6428", "#8db35a"]
for i in range(86):
    t = random.random()
    ang = random.uniform(-0.55, 0.55) * (0.45 + t)
    r = 40 + t * 250
    import math
    x = 300 + math.sin(ang) * r * 0.9
    y = 170 + math.cos(ang) * r
    rot = math.degrees(-ang) + random.uniform(-40, 40)
    s = random.uniform(0.8, 1.35)
    c = random.choice(greens)
    leaves.append(f'<path d="M0 -16 C9 -10 10 6 0 16 C-10 6 -9 -10 0 -16Z" fill="{c}" transform="translate({x:.0f} {y:.0f}) rotate({rot:.0f}) scale({s:.2f})"/>')
twigs = ''.join(f'<path d="M300 170 Q{300+dx*0.4:.0f} {300} {300+dx:.0f} {430+abs(dx)*0.2:.0f}" stroke="#6b4a2b" stroke-width="2.2" fill="none"/>' for dx in [-120,-80,-40,0,40,80,120])
falling = ''.join(f'<path class="fl" style="--i:{k}" d="M0 -14 C8 -9 9 5 0 14 C-9 5 -8 -9 0 -14Z" fill="{random.choice(greens)}" transform="translate({220+k*24} {360+(k%3)*30})"/>' for k in range(8))
drops = ''.join(f'<circle class="dr" style="--i:{k}" cx="{230+k*20}" cy="{460+(k%2)*14}" r="4" fill="#cfe3ea"/>' for k in range(8))
steam = ''.join(f'<path class="sm" style="--i:{k}" d="M{200+k*50} 600 C{180+k*50} 560 {230+k*50} 530 {205+k*50} 490 C{185+k*50} 455 {225+k*50} 430 {205+k*50} 395" stroke="#f3f1ea" stroke-width="10" stroke-linecap="round" fill="none"/>' for k in range(5))

scene = f'''<svg viewBox="0 0 600 800" class="scene" role="img" aria-label="Веник запаривается в деревянной шайке">
  <rect width="600" height="800" fill="#2b3a2c"/>
  <g class="steam">{steam}</g>
  <g id="broom">
    {twigs}
    <g>{''.join(leaves)}</g>
    <rect x="282" y="40" width="36" height="150" rx="10" fill="#c79a62"/>
    <rect x="280" y="70" width="40" height="12" fill="#8a5d33"/><rect x="280" y="112" width="40" height="12" fill="#8a5d33"/><rect x="280" y="154" width="40" height="12" fill="#8a5d33"/>
  </g>
  <g class="drops">{drops}</g>
  <g class="falls">{falling}</g>
  <g class="tub">
    <path d="M120 600 L480 600 L450 770 L150 770 Z" fill="#b98a55"/>
    <rect x="128" y="640" width="344" height="16" fill="#7a5532"/><rect x="140" y="720" width="320" height="16" fill="#7a5532"/>
    <ellipse cx="300" cy="600" rx="180" ry="34" fill="#8c6238"/>
    <ellipse id="water" cx="300" cy="604" rx="160" ry="24" fill="#7fa6b4"/>
  </g>
</svg>'''

src = open('_исходники/template.html').read()
cr = json.load(open('assets/credits.json'))
items = cr if isinstance(cr, list) else cr.get('items', [])
credits = '; '.join(f'<a href="{E(it.get("page",""))}">{E(it.get("credit",""))}</a>' for it in items if any(str(it.get("file","")).endswith(f) for f in [
  'vihtoja.jpg','venik.jpg','commons-37973096.jpg','commons-4786144.jpg','making-sauna-birch-whisks.jpg','banya-oblast-de-kostroma-3.jpg','03.jpg','birch-leaves-in-contre-jour-at-mysrtigen.jpg','sauna-bucket-and-vihta-20180814.jpg','itsetehty-vihta.jpg','in-de-sauna-slaan-met-berkentakken-bestanddeelnr.jpg']))
out = (src.replace('%%BARS%%', '\n'.join(bars))
          
          .replace('%%ITEMS%%', json.dumps(items_js, ensure_ascii=False))
          .replace('%%CREDITS%%', credits))
open('index.html', 'w').write(out)
print(len(items_js), 'items')
