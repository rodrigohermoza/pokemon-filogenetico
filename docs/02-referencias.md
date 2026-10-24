# Referencias

## El video que inspira el proyecto
**"I Spent 5+ Years Building a DNA-based Pokémon Evolutionary Tree of Life..."** — The31st. https://youtu.be/2DUg-AXaX7w

El resumen de abajo se hizo con los subtítulos manuales en inglés del video (la transcripción completa no se versiona: es contenido del autor). Capítulos: Intro 0:00 · Method 1:53 · Phylogenetic Tree 8:08 · Analysis 28:06.

Inspirado en la serie de **LoreKeeperToby** (https://www.youtube.com/watch?v=UfkA4h9_bJ0) y en el árbol de **NickRoseYT** (https://www.youtube.com/watch?v=Fyrb-1pjW_U). La parte de código la hizo un colaborador, "Prof. Carvalho".

### Su método (de la transcripción)
- **Premisa (02:05):** solo cuenta como "genético" lo que se hereda por crianza.
- **Variables (02:19–03:37):** **movimientos** (qué aprende, por qué **método** y a qué **nivel**), **habilidades** y **tipos**. Descartaron stats ("una pesadilla") y **no** usaron grupos huevo: el gráfico de UmbreonLibris mostró que están demasiado interconectados, así que prefirieron dejarlos fuera y "ver qué pasa".
- **Puntuación (03:37, 05:37):** comparar cada Pokémon contra todos (y contra sí mismo); más puntos = más parentesco. Se priorizan los movimientos **por nivel**, y más aún si se aprenden **al mismo nivel**. El tipo terminó pesando poco (09:29). La fórmula exacta no se publica.
- **Prueba de hipótesis (03:43–04:38):** a mano, Pidgey contra su línea, contra Spearow y otras aves de la ruta 1, y contra Geodude. Su línea siempre salió más cercana; lo repitieron con otras líneas. Luego, automatizado: las líneas evolutivas fueron las más cercanas "el 100% de las veces" (07:43).
- **Datos (06:19–06:44):** Espada/Escudo (Gen 8). Por el Dexit no estaban los 893 de entonces; sin DLC y casi sin legendarios (21:29).
- **Poda (07:10):** quitaron las preevoluciones; solo quedó la etapa final.
- **Árbol (07:58):** la tabla de puntuaciones se pasó por **MEGA** (software de filogenética). No dicen el algoritmo ni dan soporte de ramas.
- **Resultados (08:08–34:38):** Ditto es la primera rama ("proto-Pokémon"), luego Wobbuffet y Pyukumuku; el primer gran grupo es eléctrico + bicho; luego psíquico/hada/fantasma/planta, agua/hielo, veneno, volador/dragón, roca/tierra/fuego, y al final siniestro/normal/lucha. Agrupa bien evoluciones ramificadas, formas regionales y planes corporales (perros, gatos, medusas, ranas).
- **Autocrítica (28:48–29:25):** no saben si agrupa por parentesco o porque Game Freak da movimientos parecidos a Pokémon parecidos (y del mismo tipo).

### Debilidades que podemos atacar
1. Incompleto (sin todos los Pokémon) → usar todos desde PokéAPI.
2. Fórmula y pesos no publicados → pesos explícitos + análisis de sensibilidad.
3. Sin soporte de ramas → bootstrap.
4. Ditto/Wobbuffet basales probablemente por tener pocos movimientos → normalizar.
5. Confusión movimiento–tipo → control quitando movimientos del propio tipo.

## Otros árboles de Pokémon (para comparar, no copiar)
- Shelomi, Richards, Li & Okido (2012). *A Phylogeny and Evolutionary History of the Pokémon*. Annals of Improbable Research. Cladística con rasgos morfológicos, Gen 1. Hilo: https://bulbagarden.net/threads/paper-published-on-pokemon-phylogenetics-with-prof-oak-as-co-author.144349/
- The Straits Times (2026, 30 aniversario): árbol interactivo de 1385 variantes con una taxonomía de 8 niveles hecha a mano desde biología y mitología. No es por ADN.

## Filogenética real (lo que usaremos)
- Lewis (2001). A likelihood approach to estimating phylogeny from discrete morphological character data (**modelo Mk**). Systematic Biology 50(6).
- IQ-TREE 2 (Minh et al. 2020) — soporta datos morfológicos (`-st MORPH`), bootstrap ultrarrápido, árboles de restricción.
- Saitou & Nei (1987) — Neighbor-Joining.
