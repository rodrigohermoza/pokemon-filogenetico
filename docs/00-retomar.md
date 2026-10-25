# Retomar el proyecto (leer primero)

Última actualización: 2026-10-25 (sesión 2d).

## Estado en una línea
**La tubería funciona de punta a punta** (`make todo`, ~26 s) y el árbol radial ya está en estilo pixel con un panel "¿Cómo se hizo?". **El proyecto es por diversión: lo que importa es la imagen** (D-09). Ya lleva los sprites de las 568 etapas finales (HTML de 1.43 MB).

## Qué está hecho
| Pieza | Dónde | Estado |
|---|---|---|
| Método del video (resumen con marcas de tiempo) | `docs/02-referencias.md` | ✔ (la transcripción completa no se publica) |
| Entorno | `.venv` → `~/.venvs/Pokemon_Filogenetico` (Python 3.12) | ✔ Reinstalar: `UV_PROJECT_ENVIRONMENT=~/.venvs/Pokemon_Filogenetico uv sync` |
| Datos | `data/raw/pokeapi/` (18 CSV, 11.7 MB) + `manifest.json` | ✔ Fijados al commit `e2710d30d1`. Rehacer: `make datos` |
| Genoma | `src/genoma.py` | ✔ Cascada SV → SwSh → USUM (D-04); MT solo comunes a los 3 juegos, sin tutor (D-08) |
| Distancias | `src/puntuacion.py` (clase `Puntuacion`) | ✔ Jaccard ponderado; componente ausente = faltante (D-05) |
| Prueba Pidgey | `src/prueba_pidgey.py` | ✔ 94.2% |
| Árboles | `src/arbol.py` | ✔ NJ propio + UPGMA |
| Bootstrap | `src/bootstrap.py` | ✔ 100 réplicas. No se amplía (D-09) |
| Visualización | `src/visualizar.py` → `results/arbol_finales.html` | ✔ Estilo pixel (paleta del portafolio), búsqueda, fichas, zoom, panel explicativo. Con sprites |
| Comparación con el video | `src/comparar_video.py` → `results/comparacion_video.md` | ✔ |
| Sprites | `scripts/descargar_sprites.py` (`make sprites`) | ✔ 568 PNG, 0.73 MB en `data/raw/sprites/` (commit `97a7832d30`) |

## Números clave (detalle en [10-resultados.md](10-resultados.md), R-03)
- Prueba Pidgey: **94.2%** de vecinos de la misma línea; Pidgey → Pidgeotto 0.14, Pidgeot 0.19; Geodude 0.96.
- Sesgo del juego de origen: 76% → **61%** (azar 57%) tras D-08.
- Ditto, Wobbuffet y Pyukumuku **no** salen basales (sí en el video).
- Grupos por tipo parecidos al video, en otro orden; aparecen juntos las aves, los Ultraentes y las paradojas.
- Ramas cortas fiables; el orden de las ramas grandes es curiosidad (bootstrap, R-02).

## Qué está flojo (aceptado, no se va a validar más)
- Especies con casi ningún movimiento (capullos, Magikarp, Abra) caen raro (P-03).
- Pesos inventados (el video no publica los suyos).

## Próximos pasos
1. ~~Mirar el árbol con sprites~~ → Rodrigo lo revisó: se ven bien. (El navegador integrado no abre el HTML, P-05: para mirarlo, `open results/arbol_finales.html`.)
2. Opcional: incrustar la fuente Silkscreen (OFL, pedir aprobación con tamaño).
3. ~~git + GitHub~~ → hecho: repositorio público https://github.com/rodrigohermoza/pokemon-filogenetico (rama `main`, autor Rodrigo Hermoza, sin coautoría de Claude). La transcripción del video se quitó del historial antes de subir.
4. Llevarlo al portafolio (`../pagina-web/`), si Rodrigo quiere. Los sprites son © Nintendo: uso de fans sin fines de lucro.

## Preguntas abiertas para Rodrigo
En [07-pendientes.md](07-pendientes.md): formas regionales y megas, si va al portafolio, raíz. (GitHub ya está resuelto.)

## Prompt para retomar (copiar en una sesión nueva)
```
Retomamos Pokemon_Filogenetico (/Users/rodrigohermoza/Desktop/Proyectos/Personal/Pokemon_Filogenetico).
Lee en orden: CLAUDE.md, docs/00-retomar.md y las últimas entradas de BITACORA.md.
Estado: es un proyecto por diversión, lo que importa es la imagen (D-09, nada de más
validación). La tubería funciona (make todo, ~26 s) y el árbol está en estilo pixel en
results/arbol_finales.html. Ya tiene sprites (revisados, se ven bien). Está en GitHub
(público: rodrigohermoza/pokemon-filogenetico, rama main, al día). Pregúntame qué
quiero hacer; la opción abierta es llevarlo al portafolio (../pagina-web/). Respeta las
reglas del CLAUDE.md (nada de instalar/descargar sin aprobación con tamaño, todo gratis,
commits sin coautoría de Claude) y al terminar actualiza BITACORA.md y docs/00-retomar.md.
```
