"""Descarga los CSV de PokéAPI que usa el proyecto y escribe data/raw/manifest.json.

Los archivos se fijan a un commit concreto del repositorio de PokéAPI para que la
descarga sea reproducible: el mismo commit da siempre los mismos bytes. Para
actualizar los datos, cambiar COMMIT y volver a ejecutar.

Uso:  .venv/bin/python scripts/descargar_datos.py
Solo usa la biblioteca estándar.
"""

import hashlib
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

COMMIT = "e2710d30d1"  # último cambio en data/v2/csv al 2026-10-21
REPO = "PokeAPI/pokeapi"
BASE = f"https://raw.githubusercontent.com/{REPO}/{COMMIT}/data/v2/csv"

ARCHIVOS = [
    # núcleo: el "genoma"
    "pokemon_moves.csv",
    "pokemon_abilities.csv",
    "pokemon_types.csv",
    # especies, formas y evolución (validación)
    "pokemon.csv",
    "pokemon_species.csv",
    "pokemon_forms.csv",
    "pokemon_evolution.csv",
    "evolution_chains.csv",
    "pokemon_egg_groups.csv",
    # tablas de referencia
    "moves.csv",
    "abilities.csv",
    "types.csv",
    "egg_groups.csv",
    "version_groups.csv",
    "generations.csv",
    "pokemon_move_methods.csv",
    # nombres
    "pokemon_species_names.csv",
    "move_names.csv",
]

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "data" / "raw" / "pokeapi"
MANIFIESTO = RAIZ / "data" / "raw" / "manifest.json"


def descargar(nombre: str) -> dict:
    url = f"{BASE}/{nombre}"
    with urllib.request.urlopen(url, timeout=60) as r:
        datos = r.read()
    (DESTINO / nombre).write_bytes(datos)
    filas = datos.count(b"\n") - 1  # sin encabezado
    return {
        "archivo": f"pokeapi/{nombre}",
        "url": url,
        "bytes": len(datos),
        "filas": filas,
        "sha256": hashlib.sha256(datos).hexdigest(),
    }


def main() -> int:
    DESTINO.mkdir(parents=True, exist_ok=True)
    registros = []
    for nombre in ARCHIVOS:
        reg = descargar(nombre)
        print(f"{nombre:28s} {reg['bytes'] / 1e6:7.2f} MB {reg['filas']:>8d} filas")
        registros.append(reg)
    manifiesto = {
        "fuente": f"https://github.com/{REPO}",
        "commit": COMMIT,
        "descargado": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "licencia": "Código BSD-3-Clause; datos de Pokémon © Nintendo/Game Freak/The Pokémon Company, uso no comercial",
        "archivos": registros,
    }
    MANIFIESTO.write_text(json.dumps(manifiesto, indent=2, ensure_ascii=False) + "\n")
    total = sum(r["bytes"] for r in registros)
    print(f"\n{len(registros)} archivos, {total / 1e6:.1f} MB -> {DESTINO.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
