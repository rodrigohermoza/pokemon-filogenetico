"""Paso 1: el "genoma" de cada especie.

Para cada especie (su forma por defecto) se elige el primer juego de la cascada de
params.yaml en el que tenga movimientos por nivel, y de ese juego se toman sus
movimientos por nivel (con el nivel más bajo si aparece varias veces), huevo, MT y
tutor. Se añaden habilidades y tipos, que en PokéAPI no dependen del juego.

MT y tutor solo cuentan los movimientos que se enseñan por ese método en todos los
juegos de la cascada (D-08): cada juego tiene su propia lista de MT y de tutores, y
sin este filtro los Pokémon se agrupaban por el juego del que salieron sus datos.
Con la cascada actual quedan 65 MT y ningún tutor.

Salidas:
  data/processed/especies.csv  una fila por especie: nombres, juego usado, cadena evolutiva
  data/processed/genoma.csv    formato largo: especie, componente, rasgo, nivel
"""

import pandas as pd

from comun import CRUDOS, ES, PROCESADOS, csv, params

METODOS = {1: "nivel", 2: "huevo", 3: "tutor", 4: "mt"}


def main() -> None:
    juegos = params()["genoma"]["juegos"]
    vg = csv("version_groups").set_index("identifier")["id"]
    ids_juego = [int(vg[j]) for j in juegos]

    pokemon = csv("pokemon")
    por_defecto = pokemon[pokemon.is_default == 1][["id", "species_id"]].rename(columns={"id": "pokemon_id"})

    mov = csv("pokemon_moves").drop(columns=["order", "mastery"])
    mov = mov[mov.pokemon_move_method_id.isin(METODOS)].merge(por_defecto, on="pokemon_id")

    # Juego elegido: el primero de la cascada con al menos un movimiento por nivel.
    con_nivel = mov[(mov.pokemon_move_method_id == 1) & mov.version_group_id.isin(ids_juego)]
    juego_de = {}
    for vid in reversed(ids_juego):  # el primero de la lista sobrescribe a los demás
        for sp in con_nivel.loc[con_nivel.version_group_id == vid, "species_id"].unique():
            juego_de[sp] = vid
    elegido = pd.Series(juego_de, name="version_group_id").rename_axis("species_id").reset_index()
    mov = mov.merge(elegido, on=["species_id", "version_group_id"])

    # MT y tutor: solo los movimientos enseñados por ese método en todos los juegos (D-08).
    todos = csv("pokemon_moves")
    for metodo in (3, 4):
        comunes = set.intersection(*(
            set(todos.loc[(todos.pokemon_move_method_id == metodo) & (todos.version_group_id == v), "move_id"])
            for v in ids_juego))
        mov = mov[(mov.pokemon_move_method_id != metodo) | mov.move_id.isin(comunes)]

    mov["componente"] = mov.pokemon_move_method_id.map(METODOS)
    mov = (
        mov.groupby(["species_id", "componente", "move_id"], as_index=False)["level"].min()
        .rename(columns={"move_id": "rasgo", "level": "nivel"})
    )
    mov.loc[mov.componente != "nivel", "nivel"] = pd.NA

    hab = csv("pokemon_abilities").merge(por_defecto, on="pokemon_id")
    hab = hab[["species_id", "ability_id"]].drop_duplicates().rename(columns={"ability_id": "rasgo"})
    hab["componente"] = "habilidad"

    tip = csv("pokemon_types").merge(por_defecto, on="pokemon_id")
    tip = tip[["species_id", "type_id"]].rename(columns={"type_id": "rasgo"})
    tip["componente"] = "tipo"

    genoma = pd.concat([mov, hab, tip], ignore_index=True)[["species_id", "componente", "rasgo", "nivel"]]
    genoma = genoma.sort_values(["species_id", "componente", "rasgo"])

    sp = csv("pokemon_species")[
        ["id", "identifier", "generation_id", "evolves_from_species_id", "evolution_chain_id", "is_baby", "is_legendary", "is_mythical"]
    ].rename(columns={"id": "species_id"})
    nombres = csv("pokemon_species_names")
    nombres = nombres[nombres.local_language_id == ES][["pokemon_species_id", "name"]]
    sp = sp.merge(nombres.rename(columns={"pokemon_species_id": "species_id", "name": "nombre"}), on="species_id", how="left")
    sp = sp.merge(elegido, on="species_id", how="left")
    sp["juego"] = sp.version_group_id.map({v: k for k, v in vg.items()})
    # Etapa final = ninguna especie evoluciona desde ella.
    sp["etapa_final"] = ~sp.species_id.isin(sp.evolves_from_species_id.dropna().astype(int))
    sp = sp.drop(columns="version_group_id")

    sin_juego = sp.juego.isna().sum()
    if sin_juego:
        raise SystemExit(f"{sin_juego} especies sin movimientos por nivel en la cascada {juegos}")

    PROCESADOS.mkdir(parents=True, exist_ok=True)
    sp.to_csv(PROCESADOS / "especies.csv", index=False)
    genoma.to_csv(PROCESADOS / "genoma.csv", index=False)

    print(f"{len(sp)} especies · {len(genoma)} rasgos")
    print(sp.juego.value_counts().to_string())
    print(genoma.groupby("componente").species_id.agg(["size", "nunique"]).rename(columns={"size": "filas", "nunique": "especies"}).to_string())


if __name__ == "__main__":
    main()
