"""Paso 3: la prueba de Pidgey del video, automatizada para todas las especies.

Hipótesis (video, 03:43): si la puntuación captura parentesco, el pariente más
cercano de un Pokémon debería ser de su misma línea evolutiva, antes que Pokémon
parecidos pero no emparentados.

Para cada especie cuya cadena evolutiva tenga al menos 2 especies:
  - ¿su vecino más cercano es de la misma cadena?
  - rango del primer miembro de su cadena entre sus vecinos (1 = el más cercano).
Además se mide el efecto del juego de origen: ¿cuántos vecinos más cercanos salen
del mismo juego, frente a lo esperado por azar?

Salidas: results/prueba_pidgey.csv, results/prueba_pidgey.md
"""

import numpy as np
import pandas as pd

from comun import PROCESADOS, RESULTADOS, especies

# El caso del video: Pidgey contra su línea, aves de la ruta 1 de otras regiones y Geodude.
CASO_PIDGEY = ["pidgeotto", "pidgeot", "spearow", "fearow", "hoothoot", "taillow", "starly",
               "pidove", "fletchling", "pikipek", "rookidee", "wattrel", "geodude"]


def main() -> None:
    sp = especies()
    D = np.load(PROCESADOS / "distancias.npy")
    n = len(sp)
    cadena = sp.evolution_chain_id.to_numpy()
    tam_cadena = sp.groupby("evolution_chain_id").species_id.transform("size").to_numpy()

    Dx = D.copy()
    np.fill_diagonal(Dx, np.inf)
    orden = np.argsort(Dx, axis=1, kind="stable")
    vecino = orden[:, 0]

    filas = []
    for i in range(n):
        if tam_cadena[i] < 2:
            continue
        misma = cadena[orden[i]] == cadena[i]
        filas.append({
            "especie": sp.identifier[i],
            "nombre": sp.nombre[i],
            "juego": sp.juego[i],
            "vecino": sp.identifier[vecino[i]],
            "dist_vecino": round(float(D[i, vecino[i]]), 4),
            "vecino_misma_cadena": bool(misma[0]),
            "rango_pariente": int(np.argmax(misma)) + 1,
        })
    res = pd.DataFrame(filas)

    acierto = res.vecino_misma_cadena.mean()
    mediana_rango = res.rango_pariente.median()
    top5 = (res.rango_pariente <= 5).mean()

    # Efecto del juego: vecino más cercano del mismo juego vs proporción esperada por azar.
    juego = sp.juego.to_numpy()
    mismo_juego = (juego[vecino] == juego).mean()
    # Sin contar a la propia cadena, que casi siempre sale del mismo juego y lo infla.
    Dy = np.where(cadena[:, None] == cadena[None, :], np.inf, D)
    vecino_fuera = Dy.argmin(1)
    mismo_juego_fuera = (juego[vecino_fuera] == juego).mean()
    frec = sp.juego.value_counts(normalize=True)
    azar = float((frec ** 2).sum())

    i = sp.index[sp.identifier == "pidgey"][0]
    caso = pd.DataFrame({
        "especie": CASO_PIDGEY,
        "distancia": [round(float(D[i, sp.index[sp.identifier == e][0]]), 4) for e in CASO_PIDGEY],
    }).sort_values("distancia")

    RESULTADOS.mkdir(exist_ok=True)
    res.to_csv(RESULTADOS / "prueba_pidgey.csv", index=False)
    fallos = res[~res.vecino_misma_cadena].sort_values("rango_pariente", ascending=False)
    md = [
        "# Prueba Pidgey (generado por src/prueba_pidgey.py)",
        "",
        f"- Especies evaluadas (cadena con ≥2 especies): **{len(res)}**",
        f"- Vecino más cercano de la misma cadena: **{acierto:.1%}** (el video reporta 100% en su subconjunto)",
        f"- Pariente de su cadena entre los 5 más cercanos: **{top5:.1%}** · rango mediano: {mediana_rango:.0f}",
        f"- Vecino más cercano del mismo juego de origen: {mismo_juego:.1%}; "
        f"fuera de su cadena: **{mismo_juego_fuera:.1%}** (azar: {azar:.1%})",
        "",
        "## El caso del video: distancias desde Pidgey",
        "",
        "```",
        caso.to_string(index=False),
        "```",
        "",
        "## Peores fallos (pariente más lejano en el ranking)",
        "",
        "```",
        fallos.head(25)[["especie", "juego", "vecino", "dist_vecino", "rango_pariente"]].to_string(index=False),
        "```",
    ]
    (RESULTADOS / "prueba_pidgey.md").write_text("\n".join(md) + "\n")
    print("\n".join(md[2:6]))
    print(caso.to_string(index=False))


if __name__ == "__main__":
    main()
