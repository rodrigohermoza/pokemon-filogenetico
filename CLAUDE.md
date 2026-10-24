# Pokemon_Filogenetico: árbol filogenético de Pokémon

Referencia esencial del proyecto. Si se hizo /clear o /compact, leer en este orden:
1. Este archivo (reglas y estructura).
2. `docs/00-retomar.md` (estado actual y próximos pasos).
3. Las últimas entradas de `BITACORA.md`.

Responder siempre en **español**.

**Al terminar cada sesión:** agregar entrada en `BITACORA.md`, actualizar `docs/00-retomar.md` y, si aplica, `docs/05-decisiones.md`, `docs/06-problemas-encontrados.md` y `docs/07-pendientes.md`.

## Objetivo
Construir un árbol filogenético de Pokémon inspirado en el video de The31st (ver `docs/02-referencias.md`). **Es por diversión: lo importante es la imagen**, no la validación estadística (D-09). Que sea reproducible y vistoso. Detalle en `docs/01-objetivos.md`.

## Estructura
| Ruta | Qué es |
|---|---|
| `docs/` | Cuaderno del proyecto. Índice en `docs/README.md`. |
| `BITACORA.md` | Log por sesión: qué se hizo y cómo retomar. |
| `data/raw/pokeapi/` | 18 CSV de PokéAPI sin tocar (fijados al commit `e2710d30d1`). No se versionan. |
| `data/raw/manifest.json` | URL, bytes, filas y `sha256` de cada CSV. |
| `scripts/descargar_datos.py` | Rehace la descarga: `.venv/bin/python scripts/descargar_datos.py`. |
| `scripts/descargar_sprites.py` | Sprites 96 px de las etapas finales → `data/raw/sprites/` (`make sprites`). No se versionan. |
| `pyproject.toml`, `uv.lock` | Dependencias. Instalar con `UV_PROJECT_ENVIRONMENT=~/.venvs/Pokemon_Filogenetico uv sync`. |
| `data/processed/` | `especies.csv`, `genoma.csv` (formato largo), `distancias.npy`, `componentes.npz`. Se regeneran; no se versionan. |
| `params.yaml` | Cascada de juegos, pesos y bonus de nivel. Cambiar aquí, no en el código. |
| `src/` | `genoma.py` → `puntuacion.py` → `prueba_pidgey.py` → `arbol.py` → `bootstrap.py` → `visualizar.py` → `comparar_video.py` (+ `comun.py`). `puntuacion.py` expone la clase `Puntuacion` (reutilizada por el bootstrap). |
| `Makefile` | `make todo` corre la tubería entera (~25 s); `make datos` rehace la descarga. |
| `results/` | `prueba_pidgey.{md,csv}`, `arbol_{nj,upgma}_{todos,finales}.nwk`, `validacion_arbol.json`, `bootstrap.json`, `arbol_upgma_*_soporte.nwk`, `arbol_finales.html` (árbol radial interactivo, estilo pixel, local, sin internet; no se versiona porque lleva los sprites), `comparacion_video.md`. |

## Reglas de Rodrigo (no negociables)
- **Todo gratis** (datos, herramientas, hosting).
- **No instalar ni descargar** sin aprobación, indicando qué es y cuánto pesa.
- Entornos fuera de iCloud: venv en `~/.venvs/Pokemon_Filogenetico` (Python 3.12, creado 2026-10-21) con `.venv` como enlace simbólico (ver `../Información y manejo/LEEME.md`).
- Si se usan agentes, reportar función, qué hizo, tokens y tiempo (`docs/08-agentes.md`).
- Commits sin coautoría de Claude.
- No modificar otros proyectos de `Personal/` (solo leer).
- Presentar el plan antes de cambios grandes.

## Proyectos relacionados (solo leer)
- `../Peptidos-antimicrobianos/` — modelo de estructura de docs, tubería reproducible (Makefile, params.yaml, uv).
- `../pagina-web/` — portafolio (Astro, estilo medio pixel art); aquí terminaría la versión interactiva del árbol.
