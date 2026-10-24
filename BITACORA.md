# Bitácora

## 2026-10-21 · Sesión 1: arranque e ideación
- Revisada la estructura de `Peptidos-antimicrobianos/docs` y `Maestrias y programas/` (CLAUDE.md, BITACORA, docs numerados) para replicarla. No se modificó nada fuera de esta carpeta.
- (Corregido abajo) Video de referencia: "I Spent 5+ Years Building a DNA-based Pokémon Evolutionary Tree of Life..." (The31st). Se leyó la descripción (no el video ni la transcripción): menciona inspiración en LoreKeeperToby y NickRoseYT, ayuda de "Prof. Carvalho" y un gráfico de egg groups. El método exacto (capítulo "Method", 1:53–8:08) queda por confirmar.
- Creados: `CLAUDE.md`, `BITACORA.md`, `README.md`, `docs/` (00–09).
- Propuesta de método en `docs/03-metodo-propuesto.md`: matriz de caracteres desde PokéAPI → IQ-TREE (modelo Mk para datos morfológicos) + NJ/parsimonia de comparación → validación con líneas evolutivas.
- Nada instalado ni descargado. Agentes: ninguno.
- Cómo retomar: `docs/00-retomar.md` y responder las preguntas de `docs/07-pendientes.md`.

## 2026-10-21 · Sesión 1b: transcripción y método real
- Rodrigo aclaró que el video usa habilidades, niveles y movimientos.
- Transcripción descargada sin instalar nada (API interna de YouTube con cliente Android; ver P-01) → `docs/fuentes/transcripcion-video-the31st.md`.
- Método del video documentado en `docs/02-referencias.md`: movimientos (método + nivel, más peso a los de nivel y al mismo nivel), habilidades, tipos (poco peso); sin grupos huevo ni stats; Espada/Escudo; se quitan preevoluciones; árbol con MEGA.
- `docs/03-metodo-propuesto.md` reescrito: replicar y mejorar (todos los Pokémon, pesos explícitos, normalización, bootstrap, sensibilidad, control de tipo). D-01 y D-02 en `05-decisiones.md`.
- Agentes: ninguno.

## 2026-10-21 · Sesión 1c: entorno y tamaños
- Rodrigo decidió: todos los Pokémon (D-03).
- Entorno creado con `../Información y manejo/mantenimiento.sh venv . python3.12` → `.venv` enlazado a `~/.venvs/Pokemon_Filogenetico`. Sin paquetes.
- Tamaños medidos con la API de GitHub (sin descargar): 18 CSV necesarios = 11.7 MB; paquetes propuestos ~55 MB. Tabla en `docs/00-retomar.md`.
- Agentes: ninguno.

## 2026-10-21 · Sesión 1d: paquetes y datos
- Aprobado por Rodrigo: descarga de CSV e instalación de paquetes.
- `pyproject.toml` + `uv sync` en `~/.venvs/Pokemon_Filogenetico`: numpy 2.5.4, pandas 3.0.6, scipy 1.18.1, biopython 1.88, dendropy 5.1.1, pyyaml 6.0.3 (+4 dependencias). Descarga real ~37 MB, 155 MB instalado. El enlace `.venv` sigue intacto.
- `scripts/descargar_datos.py` (solo biblioteca estándar, fijado al commit `e2710d30d1`) → 18 CSV, 11.7 MB, `data/raw/manifest.json` con `sha256`.
- Cobertura medida: ningún juego tiene las 1025 especies; SV 733, SV∪SwSh 977, +USUM 1025. Champions no tiene movimientos por nivel.
- `.gitignore` creado (venv y CSV crudos fuera).
- Agentes: ninguno.

## 2026-10-21 · Sesión 1e: genoma, puntuación, prueba Pidgey y primer árbol
- Rodrigo aprobó la cascada SV → SwSh → USUM (D-04).
- Código nuevo: `params.yaml`, `src/{comun,genoma,puntuacion,prueba_pidgey,arbol}.py` y `Makefile` (`make todo`, ~15 s).
- Genoma: 1025 especies, 66 308 rasgos. Distancias: Jaccard ponderado por componente; componente ausente = dato faltante (D-05).
- Prueba Pidgey: 95.2% vecino de la misma cadena; el caso del video se reproduce. Fallos en etapas con casi ningún movimiento (P-03).
- Árboles: NJ en numpy propio (D-06) y UPGMA de scipy. Monofilia: 93.3% / 92.4% (todos), 85% / 90% (finales). Ditto no sale basal.
- Efecto del juego de origen medido: 76.3% frente a 57.0% por azar.
- Resultados en `docs/10-resultados.md`.
- Agentes: ninguno.

## 2026-10-21 · Sesión 1f: visualización local
- Rodrigo pidió una visualización local sin subir nada. No hizo falta instalar nada.
- `src/visualizar.py` → `results/arbol_finales.html` (0.34 MB): dendrograma radial SVG del UPGMA de etapas finales. Color por tipo, búsqueda, ficha con los 3 más cercanos, zoom y arrastre, modo oscuro. Añadido a `make todo` (`make visual`).
- Primer intento con radio = distancia: todo amontonado en el centro (P-04). Resuelto con radio por el rango de las uniones.
- Revisado en el navegador integrado (archivo local): búsqueda de Ditto, ficha de Marowak, sin errores en consola.
- Agentes: ninguno.

## 2026-10-21 · Sesión 1g: bootstrap y cierre de la sesión
- `src/puntuacion.py` refactorizado a la clase `Puntuacion` (pesos por rasgo). Mismas distancias que antes (diferencia 1e-8).
- `src/bootstrap.py`: 100 réplicas remuestreando rasgos dentro de cada componente (D-07), ~11 s. Resultados (R-02):
  - finales: soporte mediano 7; ramas profundas 0;
  - todos: el 87.7% de las líneas evolutivas con soporte ≥70.
  - Tríos sólidos: Hitmon, creación, lago, Applin.
- Visualización: opacidad de cada rama = soporte; puntos ●≥95 y ○70–94. Revisada en el navegador integrado.
- `make todo` completo, ~25 s, sin errores.
- `docs/00-retomar.md` reescrito como resumen completo para retomar tras compactar.
- Agentes: ninguno.

## 2026-10-23 · Sesión 2: menos rigor, más imagen
- Rodrigo: el proyecto es por diversión, basta con la imagen → se descarta la validación pendiente (D-09).
- Sprites medidos sin descargar (API de GitHub, commit `97a7832d30` de PokeAPI/sprites): 1025 PNG de 96 px = 1.09 MB; las 568 finales ≈ 0.6 MB. `scripts/descargar_sprites.py` y `make sprites` listos, **sin ejecutar** (falta aprobación).
- Efecto del juego de origen corregido (D-08): MT solo comunes a los 3 juegos (65) y sin tutor (0 comunes). 76% → 61% (azar 57%); Pidgey 94.2%.
- `src/comparar_video.py` (`make video`) → `results/comparacion_video.md`: Ditto/Wobbuffet/Pyukumuku no basales; grupos por tipo parecidos al video en otro orden (R-03).
- Visualización en estilo pixel (paleta y fuentes del portafolio, sin cargar nada de internet), panel "¿Cómo se hizo?", soporte de sprites. Revisada en el navegador integrado, sin errores en consola.
- `make todo` ~26 s, sin errores.
- Agentes: ninguno.

## 2026-10-23 · Sesión 2b: sprites
- Rodrigo aprobó los sprites de las 568 etapas finales. `make sprites` → 568 PNG, 0.73 MB en `data/raw/sprites/` (fuera de git).
- `src/visualizar.py`: cada sprite incrustado una sola vez (de 2.42 a 1.43 MB); en las hojas a 26 unidades y en dos anillos alternos; en la ficha a 96 px pixelado.
- El navegador integrado no abrió el HTML (P-05). Se comprobó con un script: 568 imágenes, todos los PNG válidos. Falta mirarlo a ojo.
- Agentes: ninguno.
- Rodrigo lo abrió en su navegador: los sprites se ven bien.

## 2026-10-23 · Sesión 2c: git
- `git init` (rama `main`) y primer commit como Rodrigo Hermoza <rodrigo.hermoza@utec.edu.pe>, sin coautoría de Claude. Sin remoto.
- Fuera de git: `data/raw/pokeapi/`, `data/raw/sprites/`, `data/processed/` y `results/arbol_finales.html` (lleva los sprites de Nintendo). Todo se regenera con `make datos sprites todo`.
- Ojo antes de publicar: la transcripción completa del video (`docs/fuentes/`) no debería ir a un repo público.
- Agentes: ninguno.
