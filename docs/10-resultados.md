# Resultados

Todos los números salen de `make todo` con los parámetros de `params.yaml` (pesos nivel 3, huevo 1.5, habilidad 1, MT 0.5, tutor 0.5, tipo 0.5; bonus 1, tau 5). Archivos en `results/`. **R-01 y R-02 son anteriores a D-08** (filtro de MT/tutor); los números vigentes están en R-03.

---

## R-01 — Primera corrida (2026-10-21)

### Genoma
1025 especies, 66 308 rasgos. Juego usado: Escarlata/Púrpura 733, Espada/Escudo 244, Ultrasol/Ultraluna 48.

| Componente | Filas | Especies con datos |
|---|---|---|
| nivel | 14 899 | 1025 |
| MT | 43 409 | 1014 |
| huevo | 3 212 | 563 (solo formas base) |
| tutor | 826 | 247 |
| habilidad | 2 411 | 1025 |
| tipo | 1 551 | 1025 |

### Prueba Pidgey (`results/prueba_pidgey.md`)
- 826 especies cuya cadena tiene ≥2 miembros.
- **El vecino más cercano es de su misma cadena en el 95.2%** de los casos. El video decía 100% en su subconjunto, sin publicar datos.
- El pariente de su cadena está entre los 5 más cercanos en el 97.9%.
- El caso del video se reproduce: Pidgey queda a 0.13 de Pidgeotto y a 0.18 de Pidgeot. Luego vienen Fearow (0.68), Spearow (0.69) y las otras aves; Geodude es el más lejano (0.97).

**Los fallos tienen sentido biológico (o de diseño del juego):**
- **Capullos**: Metapod, Kakuna y Silcoon solo aprenden Fortaleza. Sus genomas son casi idénticos (Metapod–Silcoon a distancia 0).
- **Magikarp y Feebas**: Magikarp solo aprende Salpicadura, Placaje y Azote.
- **Abra**: solo Teletransporte. **Cosmog**: solo Salpicadura y Teletransporte.
- **Gyarados**: su lista no tiene nada que ver con la de Magikarp; sale cerca de Salamence.
- **Eevee**: cada eeveelución es de un tipo distinto. Las 9 no forman clado, lo cual es esperable.
- **Nidoran ♀ y ♂**: PokéAPI los pone en cadenas separadas, pero son casi el mismo Pokémon. Se mezclan entre ellas, así que es un "fallo" solo de etiqueta.

Patrón general: **cuando una etapa casi no aprende movimientos (capullos, peces inútiles, bebés), el método no tiene con qué trabajar.** Es la misma razón por la que el video tenía a Ditto como primera rama.

### Efecto del juego de origen (riesgo de la cascada, D-04)
Para medirlo sin contar a la propia cadena, se busca el vecino más cercano de **fuera** de la cadena. Sale del mismo juego en el **76.3%** de los casos; por azar se esperaría el 57.0%.

| Juego propio → juego del vecino | SV | SwSh | USUM |
|---|---|---|---|
| Escarlata/Púrpura | 0.82 | 0.14 | 0.04 |
| Espada/Escudo | 0.37 | 0.61 | 0.02 |
| Ultrasol/Ultraluna | 0.27 | 0.08 | **0.65** |

El efecto es real y mayor en los 48 de Ultrasol/Ultraluna, que son el 4.7% del total pero tienen al 65% de sus vecinos ahí. Hay que tratarlo (ver pendientes).

### Árboles (`results/arbol_*.nwk`, `results/validacion_arbol.json`)
| Conjunto | Especies | Cadenas evaluables | NJ monofiléticas | UPGMA monofiléticas |
|---|---|---|---|---|
| todos | 1025 | 341 | **93.3%** | 92.4% |
| finales (como el video) | 568 | 20 (evoluciones ramificadas) | 85.0% | 90.0% |

Las cadenas que no salen como clado son las mismas de la prueba Pidgey (capullos, Magikarp, Abra, Eevee, Nidoran…). En el árbol de finales fallan Gardevoir/Gallade y Solgaleo/Lunala; en NJ, además, las eeveeluciones.

**Primeras ramas de UPGMA (finales), desde la raíz:**
1. Plantas (Hydrapple, Flapple, Shiftry, Cacturne, iniciales planta…).
2. Bichos y acero (Aegislash, Genesect, Escavalier, Durant, Galvantula, Scizor, Ninjask/Shedinja…).
3. Fuego (los monos elementales, Darmanitan, Incineroar, Arcanine…).
4. Normales, con **Ditto** dentro, junto a Persian, Slaking, Smeargle, Kecleon y Spinda.
5. Agua y dragones acuáticos.
6. Paradojas futuras (Iron-…) y legendarios.

**Diferencia con el video:** aquí Ditto **no** es la primera rama. Con la similitud normalizada (Jaccard) y "dato faltante" en lugar de "diferencia", Ditto cae con los Pokémon normales generalistas. Esto apoya la sospecha de [02-referencias.md](02-referencias.md): su Ditto basal era un artefacto de tener un solo movimiento. Tampoco aparece el grupo eléctrico + bicho como primera rama, aunque bichos y eléctricos salen como ramas tempranas en el árbol de todos.

### Visualización (`results/arbol_finales.html`, `make visual`)
Dendrograma radial del UPGMA de etapas finales, en SVG dentro de un HTML de 0.34 MB, sin librerías ni internet. Tiene búsqueda (centra el Pokémon), ficha al pasar el ratón con los 3 más cercanos, zoom con la rueda, arrastre y modo oscuro automático. Color de hoja = tipo principal (punto pequeño = segundo tipo); una rama va en color solo si todas sus hojas comparten tipo principal.

**El radio no es la distancia:** es el orden de las uniones (ver P-04).

**Aún sin hacer:** soporte de ramas (bootstrap) y sensibilidad a pesos.

---

## R-02 — Bootstrap (2026-10-21)
`src/bootstrap.py`, 100 réplicas, semilla 42 (`params.yaml`), unos 11 s en total. En cada réplica, dentro de cada componente, se sortean los rasgos con reemplazo, se recalculan las distancias y se rehace el UPGMA. Soporte = % de réplicas en que reaparece **exactamente** el mismo clado. Resumen en `results/bootstrap.json`; árboles con soporte en `results/arbol_upgma_{finales,todos}_soporte.nwk`.

| Árbol | Clados | Soporte mediano | ≥95 | ≥70 | <50 |
|---|---|---|---|---|---|
| finales (568) | 566 | 7 | 3.4% | 7.4% | 88.2% |
| todos (1025) | 1023 | 41 | 34.6% | 41.6% | 52.6% |

- **Líneas evolutivas** que forman clado en el árbol de todos: el **87.7%** de 341 tiene soporte ≥70. Son la parte sólida del árbol.
- En finales, las evoluciones ramificadas con soporte ≥70 son el 55% de 20.

**Soporte según el tamaño del clado (finales):**

| Hojas del clado | n | Soporte mediano | ≥70 |
|---|---|---|---|
| 2 | 197 | 33 | 17% |
| 3–5 | 177 | 7 | 5% |
| 6–20 | 122 | 0 | 0% |
| 21–100 | 62 | 0 | 0% |
| 101–568 | 8 | 0 | 0% |

**Las 6 ramas principales (plantas, bichos/acero, fuego, normales, agua, paradojas) tienen soporte 0.** Solo se sostienen pares y tríos. Los clados de ≥3 hojas con soporte ≥95 son estos:
- Hitmonlee, Hitmonchan y Hitmontop (98);
- Dialga, Palkia y Giratina (95);
- Azelf, Uxie y Mesprit (95);
- Flapple, Appletun e Hydrapple (96).

**Interpretación:**
1. Las relaciones cercanas (misma línea, tríos legendarios, parientes obvios) son robustas.
2. La "historia profunda" del árbol (qué tipo surgió primero, como cuenta el video) **no está respaldada por los datos**: cambia con pequeñas variaciones del genoma. Esto también vale para el árbol del video, que no reportó soporte.
3. Salvedad metodológica: el bootstrap clásico es muy estricto con clados grandes, porque basta con que un Pokémon se mueva para que el clado "no reaparezca". El *transfer bootstrap expectation* (Lemoine et al. 2018, *Nature*) mide cuánto se parece el clado en vez de exigir igualdad, y es el estándar para árboles grandes. **Pendiente** antes de concluir que las ramas profundas no valen nada.

**En la visualización:** la opacidad de cada rama sigue su soporte; ● = soporte ≥95, ○ = 70–94; al pasar el ratón por un punto se ve el valor. La cabecera muestra los porcentajes.

---

## R-03 — Filtro de MT/tutor, comparación con el video y estilo pixel (2026-10-23)

### Con D-08 (solo MT comunes, sin tutor)
| Medida | Antes (R-01/R-02) | Ahora |
|---|---|---|
| Filas MT / tutor en el genoma | 43 409 / 826 | 18 979 / 0 |
| Prueba Pidgey: vecino de la misma cadena | 95.2% | **94.2%** |
| Pariente entre los 5 más cercanos | 97.9% | 97.3% |
| Vecino fuera de la cadena del mismo juego (azar 57%) | 76.3% | **61.1%** |
| Líneas monofiléticas, todas (NJ / UPGMA) | 93.3% / 92.4% | 92.1% / 91.8% |
| Evoluciones ramificadas, finales (NJ / UPGMA, de 20) | 85% / 90% | 75% / 70% |
| Bootstrap finales: soporte mediano | 7 | 6 |
| Bootstrap todos: líneas con soporte ≥70 | 87.7% | 87.1% |

Pidgey: Pidgeotto 0.14, Pidgeot 0.19, luego Pidove, Fearow, Starly…; Geodude 0.96.

**Primeras ramas del UPGMA de finales:** plantas; agua (con Pyukumuku); **aves** (nuevo, antes no salía); fuego; paradojas futuras (Ferro-) con legendarios; **Ultraentes** juntos.

### Comparación con el video (`src/comparar_video.py` → `results/comparacion_video.md`)
- **Ditto, Wobbuffet y Pyukumuku no son basales**: están a 7, 4 y 5 uniones de la raíz. Ditto queda con Persian y Lopunny; Wobbuffet con los psíquicos (Gothitelle, Beheeyem, Musharna); Pyukumuku con los de agua (Alomomola, Milotic).
- **Grandes grupos por tipo, como en el video**, pero en otro orden y otras mezclas. Cortando en 12 grupos: psíquico + hada (el video juntaba psíquico/hada/fantasma/planta); roca/acero/tierra con Ultraentes; planta + fantasma; normales con aves; agua; veneno + siniestro; lucha con las paradojas Ferro-; dragón con paradojas antiguas; fuego; eléctrico; bicho; hielo con eeveeluciones y los caballos de Calyrex.
- El video ponía eléctrico + bicho como primer gran grupo; aquí eléctrico y bicho salen como grupos separados.

### Visualización
Estilo pixel con la paleta del portafolio (fondo oscuro, acento amarillo, Silkscreen si está instalada, si no monoespaciada), cuadros en vez de círculos, botones con sombra dura y un panel **"¿Cómo se hizo?"** con la explicación simple, cómo leer el árbol y el aviso de que el orden de las ramas grandes es curiosidad. Revisado en el navegador integrado (sin sprites).

**Sprites** (aprobados por Rodrigo, 2026-10-23): 568 PNG de 96 px, 0.73 MB. Cada uno se incrusta una vez (la ficha reutiliza el de la hoja); HTML 1.43 MB. En las hojas van a 26 unidades, en dos anillos alternos (radio +20 y +42), porque entre hojas solo hay ~10 unidades de arco; en la ficha, a 96 px con `image-rendering: pixelated`.
