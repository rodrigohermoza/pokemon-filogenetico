# Pendientes

## Preguntas para Rodrigo
1. ~~Alcance~~ → todos los Pokémon (D-03).
2. ~~Juego de referencia~~ → cascada SV → SwSh → USUM (D-04). Efecto del juego medido en R-01: 76% vs 57% por azar.
3. **Formas regionales, megas, legendarios, Pokémon sin evoluciones:** ¿entran? (El video casi no tuvo legendarios.)
4. ~~Pesos~~ → se quedan los propuestos; sin análisis de sensibilidad (D-09).
5. **Destino:** ¿repositorio público en GitHub + página en el portafolio, como Peptidos?
6. **Raíz:** el video habla de un ancestro común (¿Mew?). ¿Raíz con Mew, con Ditto o neutra?

## Tareas
- [x] Crear entorno (venv en `~/.venvs/Pokemon_Filogenetico`, vacío).
- [x] Instalar dependencias (uv sync; 10 paquetes, 155 MB en `~/.venvs`).
- [x] Descargar CSV de PokéAPI y crear manifiesto (11.7 MB).
- [x] Genoma, puntuación, prueba Pidgey y primeros árboles (R-01).
- [x] Visualización local: `results/arbol_finales.html` (UPGMA, 568 etapas finales).
- [x] Bootstrap clásico, 100 réplicas (R-02): ramas profundas con soporte 0; líneas evolutivas sólidas.
- ~~Transfer bootstrap, 1000 réplicas, bootstrap de NJ, sensibilidad a pesos, ponderar por rareza, −log(sim)~~ → descartados (D-09: el proyecto es por diversión).
- [x] Efecto del juego de origen: MT comunes y sin tutor (D-08), 76% → 61% (azar 57%).
- [x] Comparación con el video (`make video`, R-03).
- [x] Estilo pixel y panel "¿Cómo se hizo?" (R-03).
- [x] Sprites de las 568 etapas finales (0.73 MB), en las hojas y en la ficha.
- [x] Revisado a ojo por Rodrigo: los sprites se ven bien.
- [ ] Opcional: fuente Silkscreen incrustada (pedir aprobación con tamaño; hoy solo se usa si está instalada).
- [ ] Llevarlo al portafolio (`../pagina-web/`), si Rodrigo quiere.
- [x] `git init` + primer commit (2026-10-23, sin coautoría de Claude).
- [x] Transcripción completa del video quitada antes de publicar (2026-10-25).
