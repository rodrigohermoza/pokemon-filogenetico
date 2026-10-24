"""Paso 6: comparación con el árbol del video (The31st), de forma descriptiva.

El video no publica su árbol, así que se compara con lo que cuenta (transcripción,
docs/02-referencias.md):
  - Ditto, Wobbuffet y Pyukumuku son las primeras ramas;
  - después, grandes grupos por tipo (eléctrico + bicho primero, luego psíquico/hada/
    fantasma/planta, agua/hielo, veneno, volador/dragón, roca/tierra/fuego,
    siniestro/normal/lucha).

Aquí se corta el UPGMA de etapas finales en GRUPOS clados y se describe cada uno por
los tipos de sus hojas (primero o segundo tipo), y se mira dónde caen Ditto, Wobbuffet y Pyukumuku.

Salida: results/comparacion_video.md
"""

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, to_tree
from scipy.spatial.distance import squareform

from comun import PROCESADOS, RESULTADOS, especies
from visualizar import TIPOS, tipos_por_especie

GRUPOS = 12
BASALES_VIDEO = ["ditto", "wobbuffet", "pyukumuku"]
ORDEN_VIDEO = ["eléctrico + bicho", "psíquico / hada / fantasma / planta", "agua / hielo", "veneno",
               "volador / dragón", "roca / tierra / fuego", "siniestro / normal / lucha"]


def main() -> None:
    sp = especies()
    mascara = sp.etapa_final.to_numpy()
    sub = sp[mascara].reset_index(drop=True)
    D = np.load(PROCESADOS / "distancias.npy")[np.ix_(mascara, mascara)]
    raiz = to_tree(linkage(squareform(D, checks=False), method="average"))
    tipos = tipos_por_especie()
    tipos_hoja = [[TIPOS[t][0] for t in tipos[int(s)]] for s in sub.species_id]

    # Cortar desde la raíz: partir siempre el clado más grande hasta tener GRUPOS.
    grupos, orden = [raiz], []
    while len(grupos) < GRUPOS:
        grande = max(grupos, key=lambda c: c.get_count())
        grupos.remove(grande)
        grupos += [grande.left, grande.right]
    # Orden de separación: por la altura de la unión de la que cuelgan (más alta = antes).
    filas = []
    for g in grupos:
        hojas = g.pre_order()
        cuenta = pd.Series([t for k in hojas for t in tipos_hoja[k]]).value_counts()
        filas.append({
            "hojas": len(hojas),
            "tipos": " · ".join(f"{t} {n / len(hojas):.0%}" for t, n in cuenta.head(3).items()),
            "ejemplos": ", ".join(sub.nombre[k] for k in hojas[:6]),
        })
    tabla = pd.DataFrame(filas).sort_values("hojas", ascending=False)

    # Profundidad de cada especie del video: cuántas uniones hay entre la raíz y su hoja,
    # y tamaño del grupo hermano con el que se une primero.
    padres = {}
    pila = [raiz]
    while pila:
        n = pila.pop()
        if not n.is_leaf():
            for h in (n.left, n.right):
                padres[h.id] = n
                pila.append(h)
    basales = []
    for ide in BASALES_VIDEO:
        k = int(sub.index[sub.identifier == ide][0])
        prof, nodo = 0, padres[k]
        hermano = nodo.right if nodo.left.id == k else nodo.left
        while nodo.id in padres:
            prof, nodo = prof + 1, padres[nodo.id]
        cercanos = np.argsort(D[k])[1:4]
        basales.append(f"- **{sub.nombre[k]}**: {prof + 1} uniones desde la raíz (en un árbol equilibrado serían ~{int(np.log2(len(sub)))}); "
                       f"se une primero a un grupo de {hermano.get_count()} · más cercanos: "
                       + ", ".join(f"{sub.nombre[j]} ({D[k, j]:.2f})" for j in cercanos))

    md = [
        "# Comparación con el árbol del video (generado por src/comparar_video.py)",
        "",
        "## ¿Las primeras ramas son Ditto, Wobbuffet y Pyukumuku?",
        "",
        *basales,
        "",
        f"## Los {GRUPOS} grandes grupos del árbol de etapas finales",
        "",
        "% de hojas del grupo que tienen cada tipo (primero o segundo; los 3 más frecuentes).",
        "",
        "| Hojas | Tipos | Ejemplos |",
        "|---|---|---|",
        *[f"| {r.hojas} | {r.tipos} | {r.ejemplos} |" for r in tabla.itertuples()],
        "",
        "## Grupos que cuenta el video, en su orden",
        "",
        *[f"{k}. {g}" for k, g in enumerate(ORDEN_VIDEO, 1)],
    ]
    RESULTADOS.mkdir(exist_ok=True)
    (RESULTADOS / "comparacion_video.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
