"""Paso 5: árbol radial interactivo en un HTML local autocontenido.

Dibuja el árbol UPGMA de etapas finales (el equivalente al del video) como un
dendrograma radial en SVG. No usa librerías externas ni internet: el HTML lleva
dentro el SVG y un poco de JavaScript para zoom, búsqueda y fichas al pasar el ratón.

Color de cada hoja = tipo principal. Una rama se colorea con un tipo solo si
todas las hojas que cuelgan de ella comparten ese tipo principal; si no, va en gris.

Soporte bootstrap (si existe results/arbol_upgma_finales_soporte.nwk, de src/bootstrap.py):
la opacidad de cada rama sigue su soporte y los nodos llevan un punto
(lleno ≥95, hueco 70–94). Al pasar el ratón por un punto se ve el valor.

Estilo pixel, con la paleta y las fuentes del portafolio (../pagina-web). La fuente
Silkscreen se usa solo si está instalada en el equipo (no se carga de internet).

Sprites (si existe data/raw/sprites/, de scripts/descargar_sprites.py): se incrustan
como PNG en base64, en la hoja y en la ficha, con image-rendering: pixelated.

Salida: results/arbol_finales.html
"""

import base64
import html
import json
import math

import dendropy
import numpy as np
import pandas as pd

from comun import CRUDOS, PROCESADOS, RESULTADOS, csv, especies

SPRITES = CRUDOS.parent / "sprites"

TIPOS = {  # id: (nombre, color)
    1: ("Normal", "#9fa19f"), 2: ("Lucha", "#ff8000"), 3: ("Volador", "#81b9ef"),
    4: ("Veneno", "#9141cb"), 5: ("Tierra", "#915121"), 6: ("Roca", "#afa981"),
    7: ("Bicho", "#91a119"), 8: ("Fantasma", "#704170"), 9: ("Acero", "#60a1b8"),
    10: ("Fuego", "#e62829"), 11: ("Agua", "#2980ef"), 12: ("Planta", "#3fa129"),
    13: ("Eléctrico", "#e6b800"), 14: ("Psíquico", "#ef4179"), 15: ("Hielo", "#3dcef3"),
    16: ("Dragón", "#5060e1"), 17: ("Siniestro", "#624d4e"), 18: ("Hada", "#ef70ef"),
}
JUEGOS = {"scarlet-violet": "Escarlata/Púrpura", "sword-shield": "Espada/Escudo",
          "ultra-sun-ultra-moon": "Ultrasol/Ultraluna"}

TAM = 2400          # lado del lienzo SVG
R_HOJAS = 900       # radio donde terminan las ramas
R_CENTRO = 40       # radio de la raíz
HUECO = math.radians(6)  # hueco angular para que el círculo no se cierre


def tipos_por_especie() -> dict:
    pk = csv("pokemon")
    pk = pk[pk.is_default == 1][["id", "species_id"]].rename(columns={"id": "pokemon_id"})
    t = csv("pokemon_types").merge(pk, on="pokemon_id").sort_values(["species_id", "slot"])
    return t.groupby("species_id").type_id.apply(list).to_dict()


def polar(r: float, a: float) -> tuple[float, float]:
    return TAM / 2 + r * math.cos(a), TAM / 2 + r * math.sin(a)


def main() -> None:
    sp = especies()
    fin = sp[sp.etapa_final].reset_index(drop=True)
    D = np.load(PROCESADOS / "distancias.npy")
    idx_global = {s: k for k, s in enumerate(sp.identifier)}
    tipos = tipos_por_especie()
    info = fin.set_index("identifier")
    sprites = {int(p.stem): "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()
               for p in SPRITES.glob("*.png")} if SPRITES.exists() else {}

    con_soporte = RESULTADOS / "arbol_upgma_finales_soporte.nwk"
    origen = con_soporte if con_soporte.exists() else RESULTADOS / "arbol_upgma_finales.nwk"
    arbol = dendropy.Tree.get(path=origen, schema="newick", preserve_underscores=True)
    arbol.calc_node_root_distances()
    hojas = list(arbol.leaf_node_iter())
    n = len(hojas)

    # Ángulo de cada hoja según su orden; el de un nodo interno es el punto medio de sus hijos.
    for k, h in enumerate(hojas):
        h.ang = HUECO / 2 + (2 * math.pi - HUECO) * k / (n - 1) - math.pi / 2
    # Radio por el orden de las uniones, no por la distancia: en UPGMA casi todas las
    # uniones ocurren a distancias altas (mediana 0.97) y se amontonarían en el centro.
    # El orden se conserva (un ancestro siempre queda más adentro que sus descendientes).
    internos = sorted((n for n in arbol.postorder_node_iter() if not n.is_leaf()),
                      key=lambda n: n.root_distance)
    for k, nodo in enumerate(internos):
        nodo.r = R_CENTRO + (R_HOJAS - 60 - R_CENTRO) * k / (len(internos) - 1)
    for nodo in arbol.postorder_node_iter():
        if nodo.is_leaf():
            nodo.r = R_HOJAS
            nodo.tipo = tipos[int(info.loc[nodo.taxon.label, "species_id"])][0]
            nodo.sop = None
        else:
            nodo.sop = int(nodo.label) if nodo.label else None
            hijos = nodo.child_nodes()
            nodo.ang = (min(c.ang for c in hijos) + max(c.ang for c in hijos)) / 2
            t = {c.tipo for c in hijos}
            nodo.tipo = t.pop() if len(t) == 1 else None

    def color(t):
        return TIPOS[t][1] if t else "var(--rama)"

    def opacidad(s):
        return 1.0 if s is None else 0.15 + 0.85 * s / 100

    ramas, puntos = [], []
    for nodo in arbol.preorder_node_iter():
        if nodo.is_leaf():
            continue
        hijos = nodo.child_nodes()
        a0, a1 = min(c.ang for c in hijos), max(c.ang for c in hijos)
        x0, y0 = polar(nodo.r, a0)
        x1, y1 = polar(nodo.r, a1)
        grande = 1 if a1 - a0 > math.pi else 0
        ramas.append(f'<path d="M{x0:.1f},{y0:.1f}A{nodo.r:.1f},{nodo.r:.1f} 0 {grande} 1 {x1:.1f},{y1:.1f}" '
                     f'stroke="{color(nodo.tipo)}" stroke-opacity="{opacidad(nodo.sop):.2f}"/>')
        for c in hijos:
            xa, ya = polar(nodo.r, c.ang)
            xb, yb = polar(c.r, c.ang)
            ramas.append(f'<path d="M{xa:.1f},{ya:.1f}L{xb:.1f},{yb:.1f}" stroke="{color(c.tipo)}" '
                         f'stroke-opacity="{opacidad(c.sop):.2f}"/>')
        if nodo.sop is not None and nodo.sop >= 70:
            x, y = polar(nodo.r, nodo.ang)
            clase = "fuerte" if nodo.sop >= 95 else "medio"
            puntos.append(f'<rect class="{clase}" width="7" height="7" x="{x - 3.5:.1f}" y="{y - 3.5:.1f}"><title>Soporte {nodo.sop}%</title></rect>')

    datos, marcas = [], []
    for k, h in enumerate(hojas):
        ide = h.taxon.label
        fila = info.loc[ide]
        ts = tipos[int(fila.species_id)]
        g = idx_global[ide]
        cerca = [j for j in np.argsort(D[g]) if j != g and sp.etapa_final[j]][:3]
        datos.append({
            "id": ide, "n": fila.nombre, "t": [TIPOS[t][0] for t in ts], "j": JUEGOS[fila.juego],
            "g": int(fila.generation_id),
            "v": [[sp.nombre[j], round(float(D[g, j]), 2)] for j in cerca],
        })
        x, y = polar(R_HOJAS + 8, h.ang)
        grados = math.degrees(h.ang)
        izq = math.cos(h.ang) < 0
        rot = grados + 180 if izq else grados
        ancla = "end" if izq else "start"
        dx = -14 if izq else 14
        segundo = (f'<rect width="4" height="4" x="{x - 2:.1f}" y="{y - 2:.1f}" fill="{TIPOS[ts[1]][1]}"/>' if len(ts) > 1 else "")
        marca = f'<rect class="m" width="10" height="10" x="{x - 5:.1f}" y="{y - 5:.1f}" fill="{TIPOS[ts[0]][1]}"/>{segundo}'
        if int(fila.species_id) in sprites:
            # Entre hojas hay ~10 unidades de arco; el sprite (96 px, la figura ocupa ~la mitad)
            # se dibuja a 26 y en dos anillos alternos para que no se pisen. El nombre, después.
            xs, ys = polar(R_HOJAS + (20 if k % 2 else 42), h.ang)
            marca += f'<image href="{sprites[int(fila.species_id)]}" width="26" height="26" x="{xs - 13:.1f}" y="{ys - 13:.1f}"/>'
            x, y = polar(R_HOJAS + 50, h.ang)
        marcas.append(
            f'<g class="hoja" data-i="{k}">{marca}'
            f'<text x="{x:.1f}" y="{y:.1f}" dx="{dx}" dy="3" text-anchor="{ancla}" '
            f'transform="rotate({rot:.2f} {x:.1f} {y:.1f})">{html.escape(fila.nombre)}</text></g>'
        )

    val = json.loads((RESULTADOS / "validacion_arbol.json").read_text())
    pid = pd.read_csv(RESULTADOS / "prueba_pidgey.csv")
    bs = RESULTADOS / "bootstrap.json"
    if origen == con_soporte and bs.exists():
        texto_bs = ""  # el soporte se ve en el dibujo; las cifras quedan en docs/10-resultados.md
        pie_bs = (" · ■ soporte ≥95 · □ soporte 70–94 · ramas tenues = poco soporte")
    else:
        texto_bs = pie_bs = ""
    leyenda = "".join(f'<span><i style="background:{c}"></i>{nom}</span>' for nom, c in TIPOS.values())

    svg = (f'<svg id="svg" viewBox="0 0 {TAM} {TAM}" xmlns="http://www.w3.org/2000/svg">'
           f'<g class="ramas">{"".join(ramas)}</g><g class="soporte">{"".join(puntos)}</g><g class="hojas">{"".join(marcas)}</g></svg>')
    pagina = PLANTILLA.format(
        svg=svg, datos=json.dumps(datos, ensure_ascii=False), leyenda=leyenda, n=n,
        pidgey=f"{pid.vecino_misma_cadena.mean():.1%}",
        mono_todos=f"{val['todos']['upgma']['proporcion']:.1%}",
        total=len(sp), tam=TAM, texto_bs=texto_bs, pie_bs=pie_bs,
    )
    salida = RESULTADOS / "arbol_finales.html"
    salida.write_text(pagina)
    print(f"{salida.relative_to(RESULTADOS.parent)} · {n} hojas · {len(pagina) / 1e6:.2f} MB")


PLANTILLA = """<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Árbol filogenético Pokémon</title>
<style>
:root {{ --bg:#0e0d14; --bg-hondo:#07060b; --panel:#16151f; --linea:#2c2a3a; --texto:#ece9f5; --tenue:#9a96ad; --rama:#4a4760; --acento:#ffd23f;
  --fuente-pixel:"Silkscreen", ui-monospace, "SF Mono", Menlo, monospace; --fuente-texto:"IBM Plex Mono", ui-monospace, "SF Mono", Menlo, monospace; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--texto); font:13px/1.5 var(--fuente-texto); height:100vh; display:flex; flex-direction:column; }}
header {{ padding:12px 16px; border-bottom:2px solid var(--linea); background:var(--bg-hondo); display:flex; flex-wrap:wrap; gap:8px 20px; align-items:center; }}
h1 {{ font:16px var(--fuente-pixel); margin:0; letter-spacing:.5px; }}
h1 span {{ color:var(--acento); }}
.cifras {{ color:var(--tenue); font-size:12px; }}
.cifras b {{ color:var(--texto); }}
input, button {{ font:inherit; padding:6px 10px; border:2px solid var(--linea); border-radius:0; background:var(--panel); color:var(--texto); }}
input {{ width:220px; }}
input:focus, button:hover {{ outline:none; border-color:var(--acento); }}
button {{ font-family:var(--fuente-pixel); cursor:pointer; box-shadow:3px 3px 0 var(--bg-hondo); }}
button:active {{ transform:translate(2px,2px); box-shadow:1px 1px 0 var(--bg-hondo); }}
#lienzo {{ flex:1; overflow:hidden; position:relative; cursor:grab; background:radial-gradient(circle at center, var(--panel), var(--bg) 70%); }}
#lienzo.arrastrando {{ cursor:grabbing; }}
svg {{ width:100%; height:100%; display:block; }}
.ramas path {{ fill:none; stroke-width:2; stroke-linecap:square; }}
.soporte rect {{ stroke:var(--texto); stroke-width:1.5; shape-rendering:crispEdges; }}
.soporte .fuerte {{ fill:var(--texto); }}
.soporte .medio {{ fill:var(--bg); }}
.atenuado .soporte {{ opacity:.15; }}
.hoja rect, .hoja image {{ shape-rendering:crispEdges; image-rendering:pixelated; }}
.hoja text {{ font:11px var(--fuente-pixel); fill:var(--texto); }}
.hoja {{ cursor:pointer; }}
.hoja:hover text, .hoja.marcada text {{ fill:var(--acento); font-size:15px; }}
.hoja.marcada .m {{ stroke:var(--acento); stroke-width:3; }}
.atenuado .hoja:not(.marcada) {{ opacity:.15; }}
#ficha {{ position:absolute; pointer-events:none; background:var(--panel); border:2px solid var(--texto); padding:10px 12px; font-size:12px; box-shadow:4px 4px 0 var(--bg-hondo); display:none; max-width:270px; }}
#ficha h2 {{ font:15px var(--fuente-pixel); margin:0 0 4px; color:var(--acento); }}
#ficha img {{ width:96px; height:96px; image-rendering:pixelated; float:right; margin:-8px -6px 0 4px; }}
#ficha .s {{ color:var(--tenue); }}
#explica {{ position:absolute; inset:16px; max-width:680px; margin:auto; overflow:auto; background:var(--panel); border:2px solid var(--texto); box-shadow:6px 6px 0 var(--bg-hondo); padding:18px 22px; display:none; cursor:auto; z-index:2; }}
#explica.abierto {{ display:block; }}
#explica h2 {{ font:15px var(--fuente-pixel); color:var(--acento); margin:18px 0 6px; }}
#explica h2:first-of-type {{ margin-top:0; }}
#explica p, #explica li {{ margin:0 0 8px; }}
#explica button {{ float:right; }}
footer {{ padding:8px 16px; border-top:2px solid var(--linea); background:var(--bg-hondo); display:flex; flex-wrap:wrap; gap:4px 14px; font-size:11px; color:var(--tenue); }}
footer i {{ display:inline-block; width:10px; height:10px; margin-right:4px; vertical-align:-1px; }}
@media (max-width:640px) {{ header {{ padding:10px 16px; }} input {{ width:100%; }} .cifras {{ display:none; }} }}
</style></head><body>
<header>
  <h1>Árbol filogenético <span>Pokémon</span> · {n} etapas finales</h1>
  <input id="buscar" type="search" placeholder="Buscar Pokémon…" autocomplete="off">
  <button id="abrir">¿Cómo se hizo?</button>
  <span class="cifras">Prueba Pidgey <b>{pidgey}</b> · líneas evolutivas que salen juntas <b>{mono_todos}</b>{texto_bs}</span>
</header>
<div id="lienzo">{svg}<div id="ficha"></div>
<div id="explica"><button id="cerrar">Cerrar</button>
<h2>La idea</h2>
<p>En la naturaleza, los parientes se reconocen por el ADN que heredan. Los Pokémon no tienen ADN, pero sí algo que se hereda: al criarlos, las crías reciben movimientos de sus padres. Así que aquí el "ADN" de cada Pokémon es la lista de movimientos que aprende (y a qué nivel), sus habilidades y sus tipos. Está inspirado en el video de The31st.</p>
<h2>Cómo se arma el árbol</h2>
<ol>
<li>Se descarga de PokéAPI qué aprende cada uno de los {total} Pokémon (de Escarlata/Púrpura; si no está, de Espada/Escudo o Ultrasol/Ultraluna).</li>
<li>Se compara cada Pokémon con todos los demás: cuantos más movimientos comparten, y a niveles más parecidos, más "parientes" son. Los movimientos por nivel pesan más; los tipos, poco.</li>
<li>Se juntan primero los dos más parecidos, luego el siguiente par, y así hasta formar un solo árbol (UPGMA). Se dibujan solo las {n} etapas finales, como en el video.</li>
</ol>
<h2>¿Funciona?</h2>
<p>La prueba del video: si el método mide parentesco, el pariente más cercano de un Pokémon debería ser de su propia línea evolutiva. Pasa con el <b>{pidgey}</b> de ellos (Pidgey queda junto a Pidgeotto y Pidgeot, no con otras aves). Los que fallan casi no aprenden movimientos: Metapod, Magikarp, Abra.</p>
<h2>Cómo leerlo</h2>
<ul>
<li>Color = tipo principal; el cuadrito pequeño, el segundo tipo. Una rama va en color si todo lo que cuelga de ella comparte tipo.</li>
<li>Las ramas cortas (Pokémon que se parecen mucho) son fiables. El orden de las ramas grandes ("qué tipo salió primero") cambia con pequeños cambios en los datos: tómalo como curiosidad, no como historia.</li>
<li>Ditto no sale en la base del árbol, a diferencia del video: con la comparación normalizada, tener un solo movimiento ya no lo vuelve "ancestral".</li>
</ul>
<p class="s">Proyecto de fans, sin fines de lucro. Pokémon © Nintendo / Creatures / Game Freak. Datos de PokéAPI.</p>
</div></div>
<footer><span>Rueda para acercar · arrastrar para mover · pasa el ratón por un Pokémon para ver sus parientes más cercanos{pie_bs}</span>{leyenda}</footer>
<script>
const D = {datos};
const svg = document.getElementById('svg'), lienzo = document.getElementById('lienzo'), ficha = document.getElementById('ficha');
let vb = [0, 0, {tam}, {tam}];
const pintar = () => svg.setAttribute('viewBox', vb.join(' '));
lienzo.addEventListener('wheel', e => {{
  e.preventDefault();
  const r = svg.getBoundingClientRect(), f = e.deltaY > 0 ? 1.15 : 1 / 1.15;
  const s = Math.max(vb[2] / r.width, vb[3] / r.height);
  const ox = (r.width * s - vb[2]) / 2, oy = (r.height * s - vb[3]) / 2;
  const px = vb[0] - ox + (e.clientX - r.left) * s, py = vb[1] - oy + (e.clientY - r.top) * s;
  vb = [px - (px - vb[0]) * f, py - (py - vb[1]) * f, vb[2] * f, vb[3] * f]; pintar();
}}, {{ passive: false }});
let ini = null;
lienzo.addEventListener('pointerdown', e => {{ ini = [e.clientX, e.clientY, vb[0], vb[1]]; lienzo.classList.add('arrastrando'); }});
addEventListener('pointerup', () => {{ ini = null; lienzo.classList.remove('arrastrando'); }});
addEventListener('pointermove', e => {{
  if (!ini) return;
  const r = svg.getBoundingClientRect(), s = Math.max(vb[2] / r.width, vb[3] / r.height);
  vb[0] = ini[2] - (e.clientX - ini[0]) * s; vb[1] = ini[3] - (e.clientY - ini[1]) * s; pintar();
}});
document.querySelectorAll('.hoja').forEach(g => {{
  const d = D[+g.dataset.i], img = g.querySelector('image');
  d.s = img ? img.getAttribute('href') : '';  // el sprite de la hoja, para no incrustarlo dos veces
  g.addEventListener('mouseenter', () => {{
    ficha.innerHTML = (d.s ? `<img src="${{d.s}}" alt="">` : '') + `<h2>${{d.n}}</h2><div class="s">${{d.t.join(' / ')}} · Gen ${{d.g}} · datos de ${{d.j}}</div>` +
      `<div style="margin-top:6px">Más cercanos:</div>` + d.v.map(([n, x]) => `<div>${{n}} <span class="s">${{x}}</span></div>`).join('');
    ficha.style.display = 'block';
  }});
  g.addEventListener('mousemove', e => {{
    const r = lienzo.getBoundingClientRect();
    ficha.style.left = Math.min(e.clientX - r.left + 14, r.width - 270) + 'px';
    ficha.style.top = Math.min(e.clientY - r.top + 14, r.height - 140) + 'px';
  }});
  g.addEventListener('mouseleave', () => ficha.style.display = 'none');
}});
const explica = document.getElementById('explica');
document.getElementById('abrir').addEventListener('click', () => explica.classList.toggle('abierto'));
document.getElementById('cerrar').addEventListener('click', () => explica.classList.remove('abierto'));
explica.addEventListener('pointerdown', e => e.stopPropagation());
explica.addEventListener('wheel', e => e.stopPropagation());
const normal = s => s.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g, '');
document.getElementById('buscar').addEventListener('input', e => {{
  const q = normal(e.target.value.trim());
  const hojas = document.querySelectorAll('.hoja');
  hojas.forEach(g => g.classList.toggle('marcada', !!q && normal(D[+g.dataset.i].n).includes(q)));
  svg.classList.toggle('atenuado', !!q);
  const m = [...document.querySelectorAll('.hoja.marcada')];
  if (m.length === 1) {{
    const c = m[0].querySelector('.m'), x = +c.getAttribute('x') + 5, y = +c.getAttribute('y') + 5;
    vb = [x - 300, y - 300, 600, 600]; pintar();
  }} else if (!q) {{ vb = [0, 0, {tam}, {tam}]; pintar(); }}
}});
</script>
</body></html>
"""

if __name__ == "__main__":
    main()
