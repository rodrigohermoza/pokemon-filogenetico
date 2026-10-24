"""Descarga los sprites (96×96 px) de las etapas finales a data/raw/sprites/.

Del repositorio PokeAPI/sprites, fijado a un commit. Solo las especies con
etapa_final en data/processed/especies.csv (568, ~0.6 MB), que son las que dibuja el
árbol. Con --todas, las 1025 (~1.1 MB). Escribe data/raw/sprites/manifest.json.

Las imágenes son © Nintendo / Creatures / Game Freak: uso no comercial de fans.
No se versionan (data/raw/ está en .gitignore).

Uso:  .venv/bin/python scripts/descargar_sprites.py [--todas]
Solo usa la biblioteca estándar.
"""

import csv
import hashlib
import json
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

COMMIT = "97a7832d30"  # PokeAPI/sprites al 2026-10-20
BASE = f"https://raw.githubusercontent.com/PokeAPI/sprites/{COMMIT}/sprites/pokemon"

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "data" / "raw" / "sprites"


def descargar(sid: int) -> dict:
    url = f"{BASE}/{sid}.png"
    with urllib.request.urlopen(url, timeout=60) as r:
        datos = r.read()
    (DESTINO / f"{sid}.png").write_bytes(datos)
    return {"species_id": sid, "bytes": len(datos), "sha256": hashlib.sha256(datos).hexdigest()}


def main() -> int:
    todas = "--todas" in sys.argv
    with open(RAIZ / "data" / "processed" / "especies.csv") as f:
        ids = [int(r["species_id"]) for r in csv.DictReader(f) if todas or r["etapa_final"] == "True"]
    DESTINO.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(8) as ex:
        registros = list(ex.map(descargar, ids))
    total = sum(r["bytes"] for r in registros)
    (DESTINO / "manifest.json").write_text(json.dumps(
        {"fuente": "https://github.com/PokeAPI/sprites", "commit": COMMIT,
         "licencia": "© Nintendo / Creatures / Game Freak; uso no comercial de fans",
         "archivos": registros}, indent=1) + "\n")
    print(f"{len(registros)} sprites, {total / 1e6:.2f} MB -> {DESTINO.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
