"""Rutas y utilidades compartidas por los pasos de la tubería."""

from pathlib import Path

import pandas as pd
import yaml

RAIZ = Path(__file__).resolve().parent.parent
CRUDOS = RAIZ / "data" / "raw" / "pokeapi"
PROCESADOS = RAIZ / "data" / "processed"
RESULTADOS = RAIZ / "results"

ES = 7  # local_language_id del español en PokéAPI


def params() -> dict:
    return yaml.safe_load((RAIZ / "params.yaml").read_text())


def csv(nombre: str) -> pd.DataFrame:
    return pd.read_csv(CRUDOS / f"{nombre}.csv")


def especies() -> pd.DataFrame:
    return pd.read_csv(PROCESADOS / "especies.csv")
