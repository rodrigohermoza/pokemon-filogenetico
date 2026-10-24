# Registro de decisiones

Cada entrada: qué se decidió, qué alternativas había, por qué esta, y qué haría cambiar de opinión.

---

## D-01 — El "genoma" son movimientos, habilidades y tipos, como en el video
**Fecha:** 2026-10-21 · **Estado:** decidido por Rodrigo

Rodrigo aclaró que el método de referencia usa habilidades, niveles y movimientos que aprenden; la transcripción lo confirma (más tipos con poco peso). Reemplaza la primera propuesta de esta carpeta (matriz morfológica con grupos huevo, forma, color, hábitat).

**Alternativas:** rasgos morfológicos de PokéAPI (forma, color, hábitat); grupos huevo como carácter.

**Qué lo cambiaría:** nada en la base. Rasgos extra pueden probarse como análisis aparte.

---

## D-02 — La cadena evolutiva y los grupos huevo no puntúan; sirven para validar
**Fecha:** 2026-10-21 · **Estado:** propuesta, falta visto bueno de Rodrigo

Si la cadena evolutiva entrara en la puntuación, el árbol la reproduciría por construcción. Fuera de ella, es la "respuesta conocida" (la misma prueba de Pidgey del video). El video tampoco usó grupos huevo, así que sirven como segunda validación independiente.

**Qué lo cambiaría:** nada en el principio.

---

## D-03 — Todos los Pokémon desde el inicio
**Fecha:** 2026-10-21 · **Estado:** decidido por Rodrigo

No se replica primero la versión Espada/Escudo del video; se trabaja con todas las especies que tengan datos de movimientos en PokéAPI.

**Consecuencia:** hay que elegir de qué juego salen los movimientos de cada Pokémon (pendiente 2 en `07-pendientes.md`), porque ningún juego tiene a todos.

---

## D-04 — Cascada de juegos: Escarlata/Púrpura → Espada/Escudo → Ultrasol/Ultraluna
**Fecha:** 2026-10-21 · **Estado:** decidido por Rodrigo

Cada especie usa el primero de esos juegos en que tenga movimientos por nivel. Así se cubren las 1025 especies (733 + 244 + 48).

**Alternativas:** solo Ultrasol/Ultraluna (807, sin Gen 8–9); solo Escarlata/Púrpura (733).

**Riesgo medido (R-01):** agrupación por juego de origen, 76% frente al 57% por azar. **Qué lo cambiaría:** si el efecto no se puede corregir, comparar con un árbol solo de Ultrasol/Ultraluna para Gen 1–7.

---

## D-05 — Similitud Jaccard por componente; componente ausente = dato faltante
**Fecha:** 2026-10-21

La fórmula exacta está en `src/puntuacion.py`. Cada componente se normaliza por la unión (Jaccard), para que un Pokémon con muchos movimientos no salga pariente de todos. Un componente cuenta para un par solo si **ambos** tienen datos: en los juegos recientes, los movimientos huevo solo aparecen en la forma base. Sin esta regla, Pidgey y Pidgeot "diferirían" en movimientos huevo.

**Alternativas:** puntuación cruda sin normalizar (lo más parecido al video, pero premia a quien aprende mucho); contar ausencia como diferencia.

**Qué lo cambiaría:** que la sensibilidad muestre que la normalización por sí sola es la que reordena el árbol.

---

## D-06 — Neighbor-Joining propio en numpy y UPGMA de scipy
**Fecha:** 2026-10-21

El NJ de Biopython es Python puro, O(n³) en bucles: con 1025 especies tarda demasiado. Se escribió uno vectorizado (`src/arbol.py`, ~40 líneas), que tarda unos segundos. Los Newick resultantes se validaron leyéndolos con dendropy. UPGMA da raíz por construcción, que es lo que el video llama "ancestro común universal".

**Qué lo cambiaría:** pasar a IQ-TREE o a otra herramienta establecida para la versión final, si se quiere bootstrap con modelo.

---

## D-07 — Bootstrap remuestreando rasgos dentro de cada componente, sobre UPGMA
**Fecha:** 2026-10-21

Es el análogo del bootstrap de columnas de Felsenstein (1985): cada movimiento, habilidad o tipo es una "columna". Se remuestrea **dentro** de cada componente para que los pesos de `params.yaml` no cambien de réplica a réplica. Si a una especie no le toca ningún rasgo de un componente, ese componente es dato faltante en esa réplica, igual que en D-05. Se hace sobre UPGMA, el árbol que se muestra; NJ queda sin soporte por ahora.

Para que el bootstrap fuera rápido se refactorizó `src/puntuacion.py` en la clase `Puntuacion`, con matrices precalculadas. Da las mismas distancias que antes (diferencia máxima 1e-8).

**Alternativas:** jackknife (quitar el 50% de rasgos); *transfer bootstrap* (pendiente, ver R-02).

**Qué lo cambiaría:** que el transfer bootstrap muestre soporte en ramas profundas.

---

## D-08 — MT y tutor: solo movimientos comunes a todos los juegos de la cascada
**Fecha:** 2026-10-23

Cada juego tiene su propia lista de MT y de tutores (SV 229 MT, SwSh 200, USUM 100; tutores 4, 26 y 78). Por eso los Pokémon se agrupaban por el juego del que salieron sus datos (R-01: 76% frente a 57% por azar). Ahora solo cuentan los movimientos enseñados por ese método en **los tres** juegos: quedan 65 MT y **ningún tutor**, así que el componente tutor queda vacío.

Probado antes de decidir (vecino fuera de la cadena del mismo juego / prueba Pidgey): sin MT 67.8% / 94.4%; sin MT ni tutor 62.7% / 94.6%; centrar distancias por par de juegos 71.1% / 94.7%; **MT comunes y sin tutor 61.1% / 94.2%** (elegida).

**Qué lo cambiaría:** usar un solo juego para todos (no existe uno con las 1025 especies).

---

## D-09 — Dejar la validación estadística: el objetivo es la imagen
**Fecha:** 2026-10-23

Rodrigo: el proyecto es por diversión y "no tiene base en la realidad"; con la imagen le basta. Se queda lo hecho (prueba Pidgey, monofilia, bootstrap clásico, que se calculan solos en `make todo`) y se descartan el transfer bootstrap, las 1000 réplicas, el bootstrap de NJ, la sensibilidad a pesos, la ponderación por rareza y −log(sim). Lo único que se lleva a la imagen es la lectura honesta: las ramas cortas son fiables y el orden de las grandes es curiosidad.

**Qué lo cambiaría:** que Rodrigo quiera presentarlo como algo técnico (p. ej. en el portafolio con apartado de métodos).
