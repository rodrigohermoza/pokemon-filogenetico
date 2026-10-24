# Método propuesto (sin aprobar)

Base: **replicar el método del video de The31st** (resumen con marcas de tiempo en [02-referencias.md](02-referencias.md)) y luego mejorarlo con lo que ellos no hicieron: todos los Pokémon, datos reproducibles, pesos explícitos y soporte de ramas.

La idea del video: un Pokémon no tiene ADN visible, pero **lo que se hereda por crianza** (movimientos, habilidades) es, por definición del juego, genético. Ese es el "genoma".

```
PokéAPI (CSV) ──► "genoma" por Pokémon ──► puntuación todos-contra-todos ──► árbol ──► validación ──► web
                  movimientos+nivel+método,    matriz de similitud           NJ/UPGMA   líneas evolutivas
                  habilidades, tipos            → distancias                  (+ IQ-TREE)
```

## 1. El "genoma" de cada Pokémon
Todo sale de PokéAPI (CSV del repositorio, gratis):

| Componente | Archivo PokéAPI | Peso en el video | Nota |
|---|---|---|---|
| Movimientos por **nivel** (y el nivel exacto) | `pokemon_moves.csv` (`pokemon_move_method_id`=1, `level`) | El más alto, más aún si coincide el nivel | "Lo que aprenden de forma natural en su ciclo de vida" |
| Movimientos **huevo** | idem, método 2 | Medio (no especificado) | Son literalmente herencia por crianza |
| Movimientos por **MT/tutor** | idem, métodos 3–4 | Bajo (no especificado) | Muy correlacionados con el tipo, mucho ruido |
| Habilidades (incl. oculta) | `pokemon_abilities.csv` | Incluidas | |
| Tipos | `pokemon_types.csv` | Bajo ("no influyó mucho") | |
| Grupos huevo | `pokemon_egg_groups.csv` | **Excluidos** a propósito | Quedan como validación externa |
| Stats | — | Excluidas | |

**Juego de referencia:** el video usó Espada/Escudo (Gen 8, ~400 Pokémon por el Dexit). Nosotros podemos tomar, para cada Pokémon, el **último juego en que aparece** (`version_group_id` más reciente), con lo que entran todos. Decidir si mezclar juegos o fijar uno (ver `07-pendientes.md`).

## 2. Puntuación de parentesco
El video no publica la fórmula exacta: solo que el nivel pesa más y que coincidir el nivel pesa aún más. Propuesta explícita y parametrizable (`params.yaml`):

```
sim(A,B) = w_lvl  · Σ movimientos por nivel compartidos · bonus(|nivel_A − nivel_B|)
         + w_egg  · |huevo_A ∩ huevo_B|
         + w_mt   · |MT_A ∩ MT_B|
         + w_hab  · |hab_A ∩ hab_B|
         + w_tipo · |tipo_A ∩ tipo_B|
```
normalizada (tipo Jaccard ponderado) para que un Pokémon con muchos movimientos no salga "pariente de todos". Esto importa: en el video, Ditto (1 movimiento) salió como rama basal y Wobbuffet/Pyukumuku después, probablemente un **artefacto** de tener pocos movimientos y no una señal real. La normalización y medir eso es una mejora clara.

Distancia = `1 − sim/max`. Matriz N×N.

## 3. Árbol
- **Principal:** la matriz de distancias → **Neighbor-Joining** y **UPGMA** en Python (`scikit-bio` / `Biopython`). El video usó **MEGA** (gratis) con la tabla de puntuaciones; no dice qué algoritmo, probablemente NJ o UPGMA. El "ancestro común universal" del que hablan sugiere un árbol enraizado (UPGMA es enraizado por construcción).
- **Alternativa rigurosa:** codificar cada movimiento/habilidad como carácter binario (presente/ausente) → IQ-TREE con modelo Mk (`-st MORPH`). Pierde el matiz del nivel, pero da un árbol por máxima verosimilitud.
- **Soporte:** bootstrap remuestreando movimientos (columnas) y recalculando el árbol 100–1000 veces. El video no tiene esto.

## 4. Validación
- **Su prueba, automatizada:** para cada Pokémon, ¿su pariente más cercano está en su misma línea evolutiva? (Pidgey debe salir más cerca de Pidgeotto que de Spearow). Ellos reportan 100%; nosotros lo medimos en todos.
- **Monofilia:** % de líneas evolutivas que forman clado. Formas regionales y evoluciones ramificadas (Eevee) también deberían agruparse.
- **Grupos huevo** como validación independiente (no entran en la puntuación).
- **Sensibilidad a los pesos:** variar `w_*` y medir la distancia Robinson-Foulds entre árboles. Si el árbol cambia mucho con los pesos, sus conclusiones son frágiles.
- **Control del tipo:** el propio video sospecha que los movimientos solo reflejan el tipo. Probar quitando movimientos del mismo tipo que el Pokémon, o solo movimientos huevo.

## 5. Árbol final
Como en el video: **quitar las preevoluciones** para el árbol de presentación (dejar solo la etapa final), después de usarlas en la validación. Opción: mostrar las dos versiones.

## 6. Visualización
- Rápida: iTOL o `toytree`.
- Final: árbol radial interactivo (D3) con sprites, color por tipo, búsqueda y zoom → estilo medio pixel art de `../pagina-web/`. Poder comparar "nuestro árbol" con el del video.

## Plan por etapas
1. **Réplica Gen 8 / Espada-Escudo** con su método para ver si sale algo parecido (Ditto basal, eléctricos+bichos primero, psíquicos bípedos juntos…).
2. Prueba Pidgey automatizada en todos.
3. Todos los Pokémon + normalización + bootstrap.
4. Sensibilidad a pesos, control de tipo, alternativa IQ-TREE.
5. Visualización y documentación (explicación simple y técnica, texto para el portafolio).

## Stack propuesto
Python con `uv`, `pandas`, `numpy`, `scikit-bio` o `Biopython` (NJ/UPGMA), `dendropy` (Robinson-Foulds), opcional IQ-TREE 2 y MEGA para comparar. Makefile + `params.yaml`.
