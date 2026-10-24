"""Paso 4b: soporte de ramas por bootstrap (Felsenstein 1985, adaptado a rasgos).

En cada réplica, dentro de cada componente (nivel, huevo, MT, tutor, habilidad, tipo)
se sortean tantos rasgos como hay, con reemplazo: un movimiento puede salir 0, 1, 2…
veces y cuenta con ese peso. Con ese "genoma remuestreado" se recalculan las
distancias y el árbol UPGMA. El soporte de un clado del árbol de referencia es el %
de réplicas en que reaparece exactamente ese clado.

Lectura habitual: ≥95 muy sólido, 70–95 razonable, <70 no fiarse de esa rama.

Se hace sobre el árbol que se muestra (UPGMA de etapas finales) y sobre el de
todas las especies (para el soporte de las líneas evolutivas).

Salidas: results/arbol_upgma_{finales,todos}_soporte.nwk (soporte como etiqueta de
nodo interno) y results/bootstrap.json (resumen).
"""

import json
import time

import dendropy
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, to_tree
from scipy.spatial.distance import squareform

from comun import PROCESADOS, RESULTADOS, especies, params
from puntuacion import COMPONENTES, Puntuacion


def clados_upgma(D: np.ndarray) -> list[frozenset]:
    raiz = to_tree(linkage(squareform(D, checks=False), method="average"))
    clados, pila = [], [raiz]
    while pila:
        nodo = pila.pop()
        if not nodo.is_leaf():
            clados.append(frozenset(nodo.pre_order()))
            pila += [nodo.left, nodo.right]
    return clados


def main() -> None:
    p = params()
    rep = p["bootstrap"]["replicas"]
    rng = np.random.default_rng(p["bootstrap"]["semilla"])
    sp = especies()
    genoma = pd.read_csv(PROCESADOS / "genoma.csv")
    resumen = {"replicas": rep, "semilla": p["bootstrap"]["semilla"]}

    for conjunto, mascara in [("finales", sp.etapa_final.to_numpy()), ("todos", np.ones(len(sp), bool))]:
        sub = sp[mascara].reset_index(drop=True)
        nombres = sub.identifier.tolist()
        punt = Puntuacion(genoma, sub.species_id, p["puntuacion"])
        tam = punt.tamanos()

        referencia = clados_upgma(punt.distancias())
        cuenta = dict.fromkeys(referencia, 0)
        t0 = time.time()
        for r in range(rep):
            pesos = {c: np.bincount(rng.integers(0, max(tam[c], 1), tam[c]), minlength=tam[c]).astype(float)
                     for c in COMPONENTES}
            for c in clados_upgma(punt.distancias(pesos)):
                if c in cuenta:
                    cuenta[c] += 1
        soporte = {c: round(100 * k / rep) for c, k in cuenta.items()}

        # Escribir el árbol de referencia con el soporte en cada nodo interno.
        arbol = dendropy.Tree.get(path=RESULTADOS / f"arbol_upgma_{conjunto}.nwk", schema="newick",
                                  preserve_underscores=True)
        pos = {nm: k for k, nm in enumerate(nombres)}
        for nodo in arbol.postorder_node_iter():
            if nodo.is_leaf():
                nodo.hojas = frozenset([pos[nodo.taxon.label]])
            else:
                nodo.hojas = frozenset().union(*(c.hojas for c in nodo.child_nodes()))
                if len(nodo.hojas) < len(nombres):
                    nodo.label = str(soporte[nodo.hojas])
        arbol.write(path=RESULTADOS / f"arbol_upgma_{conjunto}_soporte.nwk", schema="newick",
                    suppress_rooting=True, unquoted_underscores=True)

        valores = np.array([soporte[c] for c in referencia if len(c) < len(nombres)])
        cadenas = {
            str(sub.identifier[g.index[0]]): frozenset(g.index) for _, g in sub.groupby("evolution_chain_id") if len(g) >= 2
        }
        sop_cadenas = {k: soporte.get(v, 0) for k, v in cadenas.items()}
        resumen[conjunto] = {
            "especies": len(nombres),
            "clados": len(valores),
            "soporte_mediano": float(np.median(valores)),
            "pct_clados_ge95": round(float((valores >= 95).mean()), 4),
            "pct_clados_ge70": round(float((valores >= 70).mean()), 4),
            "pct_clados_lt50": round(float((valores < 50).mean()), 4),
            "cadenas_evaluadas": len(cadenas),
            "cadenas_soporte_ge70": round(float(np.mean([v >= 70 for v in sop_cadenas.values()])), 4) if cadenas else None,
            "segundos": round(time.time() - t0, 1),
        }
        print(f"[{conjunto}] {rep} réplicas en {resumen[conjunto]['segundos']} s · {len(valores)} clados · "
              f"mediana {resumen[conjunto]['soporte_mediano']:.0f} · ≥95: {resumen[conjunto]['pct_clados_ge95']:.1%} · "
              f"≥70: {resumen[conjunto]['pct_clados_ge70']:.1%} · <50: {resumen[conjunto]['pct_clados_lt50']:.1%}")
        if cadenas:
            print(f"   líneas evolutivas (clado en la referencia) con soporte ≥70: {resumen[conjunto]['cadenas_soporte_ge70']:.1%} de {len(cadenas)}")

    (RESULTADOS / "bootstrap.json").write_text(json.dumps(resumen, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
