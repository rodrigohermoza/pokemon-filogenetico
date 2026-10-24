# Objetivos

## Qué se busca
Reconstruir un árbol filogenético de Pokémon tratándolos como si fueran especies reales, usando el flujo de trabajo de un filogenetista: definir caracteres heredables, codificarlos, inferir el árbol con un modelo explícito y medir cuánta confianza merece cada rama.

Dos usos:
1. **Divertido / divulgación**: un árbol bonito e interactivo con sprites, para el portafolio (`../pagina-web/`).
2. **Didáctico / técnico**: demostrar que se dominan los conceptos (matriz de caracteres, homoplasia, modelos, bootstrap, enraizamiento, comparación de topologías) con un dataset que cualquiera entiende.

## Qué cuenta como éxito
- Tubería reproducible de punta a punta (`make` o un comando): datos → matriz → árbol → figura.
- **Las líneas evolutivas salen como clados** (Bulbasaur–Ivysaur–Venusaur juntos) en la gran mayoría de casos *sin forzarlo*. Es el "control positivo" del proyecto: se sabe la respuesta correcta.
- Soporte de ramas reportado (bootstrap) y comparación entre al menos dos métodos.
- Una explicación sin jerga y una técnica, como en Peptidos.
- Visualización navegable.

## Fuera de alcance (por ahora)
- Afirmar que el árbol es "la verdad": los Pokémon no tienen ADN, es un ejercicio de método.
- Rasgos tomados del lore/Pokédex a mano para los ~1000 Pokémon (demasiado trabajo manual; quizás para un subconjunto).
