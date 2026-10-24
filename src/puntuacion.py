"""Paso 2: puntuación de parentesco todos-contra-todos y matriz de distancias.

Para cada componente c (nivel, huevo, mt, tutor, habilidad, tipo) y cada par A, B:

  sim_c = compartido_c / |A_c ∪ B_c|                       (Jaccard)

y para "nivel" cada movimiento compartido vale 1 + bonus * exp(-|nivel_A - nivel_B| / tau),
dividido entre (1 + bonus) para que sim_nivel siga en [0, 1].

  sim(A, B) = Σ_c w_c · sim_c · presente_c / Σ_c w_c · presente_c
  distancia = 1 - sim

presente_c = ambos tienen al menos un rasgo de c. Así, que un Pokémon evolucionado no
tenga movimientos huevo listados (solo los tiene la forma base) se trata como dato
faltante, no como diferencia.

Cada rasgo puede llevar un peso (multiplicidad). Por defecto es 1; el bootstrap
(src/bootstrap.py) remuestrea rasgos con reemplazo y pasa cuántas veces salió cada uno.

Salidas: data/processed/distancias.npy (N×N, en el orden de especies.csv) y
         data/processed/componentes.npz (sim_c y presente_c por componente, para análisis).
"""

import numpy as np
import pandas as pd

from comun import PROCESADOS, especies, params

COMPONENTES = ["nivel", "huevo", "mt", "tutor", "habilidad", "tipo"]


class Puntuacion:
    """Precalcula las matrices especie × rasgo para recalcular distancias rápido."""

    def __init__(self, genoma: pd.DataFrame, ids_especie, p: dict):
        self.n = len(ids_especie)
        self.pesos = p["pesos"]
        idx = {s: k for k, s in enumerate(ids_especie)}
        genoma = genoma[genoma.species_id.isin(idx)]
        self.X, self.nucleos = {}, []
        for comp in COMPONENTES:
            sub = genoma[genoma.componente == comp]
            rasgos = {r: k for k, r in enumerate(sub.rasgo.unique())}
            X = np.zeros((self.n, len(rasgos)))
            if len(sub):  # un componente puede quedar vacío (p. ej. tutor, D-08)
                X[sub.species_id.map(idx).to_numpy(), sub.rasgo.map(rasgos).to_numpy()] = 1
            self.X[comp] = X
            if comp == "nivel":
                # Por movimiento: qué especies lo aprenden y la matriz 1 + bonus·exp(-|Δnivel|/tau).
                b, tau = p["bonus_mismo_nivel"], p["tau_nivel"]
                self.bonus = b
                for r, g in sub.groupby("rasgo"):
                    i = g.species_id.map(idx).to_numpy()
                    lv = g.nivel.to_numpy(dtype=float)
                    self.nucleos.append((rasgos[r], i, 1 + b * np.exp(-np.abs(lv[:, None] - lv[None, :]) / tau)))

    def tamanos(self) -> dict:
        return {c: X.shape[1] for c, X in self.X.items()}

    def componente(self, comp: str, w: np.ndarray | None = None):
        X = self.X[comp]
        w = np.ones(X.shape[1]) if w is None else w
        Xw = X * w
        inter = Xw @ X.T
        tam = Xw.sum(1)
        union = tam[:, None] + tam[None, :] - inter
        # Con pesos de bootstrap, si a una especie no le tocó ningún rasgo de c, c es dato faltante.
        presente = (tam[:, None] > 0) & (tam[None, :] > 0)
        if comp == "nivel":
            compartido = np.zeros((self.n, self.n))
            for k, i, nucleo in self.nucleos:
                if w[k]:
                    compartido[np.ix_(i, i)] += w[k] * nucleo
            union = union * (1 + self.bonus)
        else:
            compartido = inter
        with np.errstate(invalid="ignore", divide="ignore"):
            sim = np.where(presente & (union > 0), compartido / union, 0.0)
        return sim, presente

    def distancias(self, pesos_rasgo: dict | None = None, guardar: dict | None = None) -> np.ndarray:
        num = np.zeros((self.n, self.n))
        den = np.zeros((self.n, self.n))
        for comp in COMPONENTES:
            sim, pres = self.componente(comp, None if pesos_rasgo is None else pesos_rasgo[comp])
            w = self.pesos[comp]
            num += w * sim * pres
            den += w * pres
            if guardar is not None:
                guardar[f"sim_{comp}"] = sim.astype(np.float32)
                guardar[f"presente_{comp}"] = pres
        sim = np.divide(num, den, out=np.zeros_like(num), where=den > 0)
        np.fill_diagonal(sim, 1.0)
        return 1.0 - sim


def main() -> None:
    sp = especies()
    genoma = pd.read_csv(PROCESADOS / "genoma.csv")
    punt = Puntuacion(genoma, sp.species_id, params()["puntuacion"])
    guardar = {}
    dist = punt.distancias(guardar=guardar)
    assert np.allclose(dist, dist.T) and dist.min() >= -1e-9

    np.save(PROCESADOS / "distancias.npy", dist)
    np.savez_compressed(PROCESADOS / "componentes.npz", **guardar)
    n = len(sp)
    fuera = dist[~np.eye(n, dtype=bool)]
    print(f"Matriz {n}×{n} · distancia fuera de la diagonal: min {fuera.min():.3f}, mediana {np.median(fuera):.3f}, max {fuera.max():.3f}")


if __name__ == "__main__":
    main()
