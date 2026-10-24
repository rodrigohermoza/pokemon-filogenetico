"""Paso 4: árboles a partir de la matriz de distancias y su validación.

Dos métodos:
  - Neighbor-Joining (Saitou y Nei 1987), implementado aquí con numpy porque el de
    Biopython es Python puro y con ~1000 especies tarda demasiado. Árbol sin raíz;
    se escribe con la raíz en la última unión.
  - UPGMA (promedio, scipy). Enraizado por construcción: el equivalente al
    "ancestro común universal" del video.

Dos conjuntos:
  - todos: las 1025 especies (para validar con las líneas evolutivas).
  - finales: solo etapas finales, como hizo el video al quitar las preevoluciones.

Validación: % de cadenas evolutivas que forman un clado (en NJ, una bipartición,
porque no tiene raíz). En "finales" solo cuentan las cadenas con ≥2 etapas
finales (evoluciones ramificadas: Eevee, Tyrogue, Wurmple…).

Salidas: results/arbol_{nj,upgma}_{todos,finales}.nwk, results/validacion_arbol.json
"""

import json

import numpy as np
from scipy.cluster.hierarchy import linkage, to_tree
from scipy.spatial.distance import squareform

from comun import PROCESADOS, RESULTADOS, especies


def neighbor_joining(D: np.ndarray, nombres: list[str]):
    """Devuelve (newick, clados) con clados = lista de frozensets de índices de hojas."""
    D = D.astype(float).copy()
    nodos = list(nombres)
    hojas = [frozenset([k]) for k in range(len(nombres))]
    clados = []
    while len(nodos) > 2:
        n = len(nodos)
        r = D.sum(1)
        Q = (n - 2) * D - r[:, None] - r[None, :]
        np.fill_diagonal(Q, np.inf)
        i, j = np.unravel_index(np.argmin(Q), Q.shape)
        if i > j:
            i, j = j, i
        dij = D[i, j]
        li = max(0.0, 0.5 * dij + (r[i] - r[j]) / (2 * (n - 2)))
        lj = max(0.0, dij - li)
        nuevo = f"({nodos[i]}:{li:.5f},{nodos[j]}:{lj:.5f})"
        du = 0.5 * (D[i] + D[j] - dij)
        D[i] = du
        D[:, i] = du
        D[i, i] = 0.0
        D = np.delete(np.delete(D, j, 0), j, 1)
        nodos[i] = nuevo
        hojas[i] = hojas[i] | hojas[j]
        clados.append(hojas[i])
        del nodos[j], hojas[j]
    d = D[0, 1] / 2
    return f"({nodos[0]}:{d:.5f},{nodos[1]}:{d:.5f});", clados + hojas


def upgma(D: np.ndarray, nombres: list[str]):
    Z = linkage(squareform(D, checks=False), method="average")
    raiz = to_tree(Z)
    clados = []

    def nwk(nodo, altura_padre):
        largo = altura_padre - nodo.dist / 2
        if nodo.is_leaf():
            clados.append(frozenset([nodo.id]))
            return f"{nombres[nodo.id]}:{largo:.5f}"
        texto = f"({nwk(nodo.left, nodo.dist / 2)},{nwk(nodo.right, nodo.dist / 2)}):{largo:.5f}"
        clados.append(frozenset(nodo.pre_order()))
        return texto

    texto = nwk(raiz, raiz.dist / 2)
    return texto.rsplit(":", 1)[0] + ";", clados, raiz


def monofilia(grupos: dict, clados: list, n: int, sin_raiz: bool) -> dict:
    conjuntos = set(clados)
    if sin_raiz:
        todo = frozenset(range(n))
        conjuntos |= {todo - c for c in clados}
    ok = {k: (frozenset(v) in conjuntos) for k, v in grupos.items()}
    return {"cadenas": len(ok), "monofileticas": sum(ok.values()),
            "proporcion": round(sum(ok.values()) / max(1, len(ok)), 4),
            "fallan": sorted(k for k, v in ok.items() if not v)}


def main() -> None:
    sp = especies()
    D = np.load(PROCESADOS / "distancias.npy")
    RESULTADOS.mkdir(exist_ok=True)
    informe = {}

    for conjunto, mascara in [("todos", np.ones(len(sp), bool)), ("finales", sp.etapa_final.to_numpy())]:
        sub = sp[mascara].reset_index(drop=True)
        Ds = D[np.ix_(mascara, mascara)]
        nombres = sub.identifier.tolist()
        n = len(sub)
        grupos = {
            str(sub.identifier[g.index[0]]) + f" ({len(g)})": g.index.tolist()
            for _, g in sub.groupby("evolution_chain_id") if len(g) >= 2
        }

        nwk_nj, clados_nj = neighbor_joining(Ds, nombres)
        nwk_up, clados_up, raiz = upgma(Ds, nombres)
        (RESULTADOS / f"arbol_nj_{conjunto}.nwk").write_text(nwk_nj + "\n")
        (RESULTADOS / f"arbol_upgma_{conjunto}.nwk").write_text(nwk_up + "\n")

        # Primeras ramas de UPGMA desde la raíz: cuál es el grupo más pequeño que se separa.
        primeras, nodo = [], raiz
        for _ in range(6):
            if nodo.is_leaf():
                break
            a, b = sorted([nodo.left, nodo.right], key=lambda x: x.get_count())
            primeras.append([nombres[k] for k in a.pre_order()][:12] + (["…"] if a.get_count() > 12 else []))
            nodo = b

        informe[conjunto] = {
            "especies": n,
            "nj": monofilia(grupos, clados_nj, n, sin_raiz=True),
            "upgma": monofilia(grupos, clados_up, n, sin_raiz=False),
            "upgma_primeras_ramas": primeras,
        }
        print(f"[{conjunto}] {n} especies · {len(grupos)} cadenas con ≥2 · "
              f"NJ {informe[conjunto]['nj']['proporcion']:.1%} · UPGMA {informe[conjunto]['upgma']['proporcion']:.1%} monofiléticas")
        for k, r in enumerate(primeras, 1):
            print(f"   UPGMA rama {k} que se separa: {r}")

    (RESULTADOS / "validacion_arbol.json").write_text(json.dumps(informe, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
