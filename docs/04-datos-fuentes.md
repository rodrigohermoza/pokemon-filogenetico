# Datos y fuentes

Cada fuente: URL, licencia, fecha de descarga, tamaño y conteos.

| Fuente | URL | Licencia | Descargado | Notas |
|---|---|---|---|---|
| PokéAPI | https://pokeapi.co · https://github.com/PokeAPI/pokeapi (CSV en `data/v2/csv`) | Código BSD-3; los datos son de Pokémon/Nintendo, uso no comercial y educativo | 2026-10-21 | Preferir el repositorio CSV a miles de llamadas a la API (es la petición de su política de uso justo) |
| Transcripción del video | https://youtu.be/2DUg-AXaX7w (pista en-GB) | Derechos del autor; solo estudio | 2026-10-21 | No se versiona (contenido del autor); resumen con marcas de tiempo en `02-referencias.md` |
| Sprites | https://github.com/PokeAPI/sprites | Propiedad de Nintendo/Game Freak; uso de fan sin fines comerciales | — | Solo para la visualización |

## Tamaños medidos (2026-10-21, metadatos de GitHub, sin descargar)
Último cambio en `data/v2/csv`: 2026-10-20 (commit `e2710d30d1`). La carpeta completa: 187 archivos, 41.7 MB.

| Archivo | MB | Para qué |
|---|---|---|
| `pokemon_moves.csv` | 10.73 | Movimientos por Pokémon, juego, método y nivel (el núcleo) |
| `pokemon_species_names.csv` | 0.40 | Nombres (en español también) |
| `move_names.csv` | 0.20 | Nombres de movimientos |
| `pokemon_forms.csv`, `pokemon_species.csv`, `pokemon.csv` | 0.17 | Especies, formas, variedades |
| `moves.csv`, `pokemon_evolution.csv`, `pokemon_abilities.csv`, `pokemon_types.csv`, `pokemon_egg_groups.csv`, `abilities.csv` | 0.16 | Tipo de cada movimiento, evoluciones, habilidades, tipos, grupos huevo |
| `evolution_chains.csv`, `version_groups.csv`, `types.csv`, `generations.csv`, `pokemon_move_methods.csv`, `egg_groups.csv` | <0.01 | Tablas de referencia |
| **Subtotal (18 archivos)** | **11.7** | |

## Descarga hecha (2026-10-21)
`scripts/descargar_datos.py` → `data/raw/pokeapi/` (18 archivos, 11.7 MB) y `data/raw/manifest.json` (URL fijada al commit, bytes, filas, `sha256`).

Conteos clave: `pokemon_moves.csv` 638 321 filas · `pokemon_species.csv` 1025 especies · `pokemon.csv` 1351 variedades (326 formas no por defecto) · `moves.csv` 937 movimientos · `evolution_chains.csv` 540 cadenas · 32 grupos de versión (juegos).

## Cobertura de movimientos por nivel (forma por defecto de cada especie)
Ningún juego tiene a las 1025 especies:

| Juego | Especies con movimientos por nivel |
|---|---|
| Escarlata/Púrpura (+DLC) | 733 |
| Espada/Escudo (+DLC) | 664 |
| Diamante Brillante/Perla Reluciente | 488 |
| Ultrasol/Ultraluna | 807 |
| Champions | 207, **sin movimientos por nivel** (no sirve) |

- Escarlata/Púrpura ∪ Espada/Escudo = 977; + Ultrasol/Ultraluna = **1025 (todas)**.
- Último juego principal de cada especie: Escarlata/Púrpura 733, Espada/Escudo 143, DBPR 140, USUL 9.
- En Escarlata/Púrpura, cada especie aprende de mediana 15 movimientos por nivel (mín. 1, máx. 33).
- Spin-offs (Let's Go, Leyendas Arceus, Leyendas Z-A, Colosseum/XD, Champions) tienen otros sistemas de movimientos: excluidos.
