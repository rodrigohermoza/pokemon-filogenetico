# Problemas encontrados

Bitácora de lo que falló de verdad. Formato: síntoma, causa, resolución, lección.

---

## P-01 — No se podía leer la transcripción del video
**Fecha:** 2026-10-21 · **Estado:** resuelto

**Síntoma:** la página del video solo devuelve el título. Las URLs de subtítulos (`timedtext`) que vienen en el HTML devuelven 0 bytes.

**Causa:** YouTube exige un token adicional para las URLs de subtítulos del cliente web.

**Resolución:** pedir el reproductor por la API interna con el cliente Android (`POST https://www.youtube.com/youtubei/v1/player` con `clientName: ANDROID`). Las URLs de subtítulos que devuelve ese cliente sí funcionan. Se descargó la pista manual en inglés (en-GB, mejor que la automática), se convirtió a texto con marcas de tiempo y se usó para el resumen de `02-referencias.md` (la transcripción completa se quitó antes de publicar el repositorio). Sin instalar nada (solo `curl` + `python3`).

**Lección:** antes de instalar una herramienta, probar si el dato es alcanzable con lo que ya hay. Si este truco deja de funcionar, la alternativa es `youtube-transcript-api` (pedir aprobación).

---

## P-02 — `DataFrame.to_markdown` pide `tabulate`
**Fecha:** 2026-10-21 · **Estado:** resuelto

**Síntoma:** `ImportError: Import tabulate failed` al generar `prueba_pidgey.md`.
**Causa:** `to_markdown` de pandas depende de un paquete opcional que no se instaló.
**Resolución:** usar `to_string` dentro de un bloque de código. No vale la pena otra dependencia.
**Lección:** las funciones "de conveniencia" de pandas pueden arrastrar dependencias opcionales.

---

## P-03 — Etapas con casi ningún movimiento rompen la prueba Pidgey
**Fecha:** 2026-10-21 · **Estado:** abierto, es una limitación del método

**Síntoma:** la prueba falla en el 4.8% de los casos. Metapod y Silcoon quedan a distancia 0; Magikarp sale más cerca de Feebas que de Gyarados.
**Causa:** los capullos solo aprenden Fortaleza, Magikarp solo Salpicadura, Placaje y Azote, Abra solo Teletransporte. Con uno a tres movimientos no hay señal. Es el mismo fenómeno que puso a Ditto como primera rama en el video.
**Resolución posible:** ponderar los movimientos por rareza (que Fortaleza compartida valga menos que un movimiento raro compartido), o reportar estas especies aparte. No se ha hecho.
**Lección:** los fallos del control positivo explican el método mejor que los aciertos.

---

## P-04 — En el árbol radial, las uniones se amontonaban en el centro
**Fecha:** 2026-10-21 · **Estado:** resuelto

**Síntoma:** con el radio proporcional a la distancia desde la raíz, todas las ramas internas quedaban en un círculo diminuto en el centro y el resto eran líneas largas hasta las hojas.
**Causa:** las distancias están saturadas (mediana 0.97), así que en UPGMA casi todas las uniones ocurren a alturas parecidas y altas.
**Resolución:** radio por el **rango** de la altura de cada unión. Se conserva el orden (un ancestro siempre queda más adentro) pero el espacio se reparte. El pie del HTML lo declara.
**Lección:** la saturación de la distancia es también una pista para el método: quizá convenga una transformación (p. ej. -log de la similitud) antes de construir el árbol. Queda anotado para la sensibilidad.

---

## P-05 — El navegador integrado no abre el HTML con sprites
**Fecha:** 2026-10-23

`preview_start` con `file://` funcionó con el HTML de 0.4 MB, pero falló con el de 1.4 MB y también con una copia de 0.75 MB en el scratchpad ("couldn't open… missing, unreadable, or the user declined access"). Servirlo por HTTP necesitaría añadir una entrada a `Personal/.claude/launch.json`, que está fuera del proyecto, y no se tocó. Se comprobó que hay 568 imágenes y que todos los PNG son válidos, y la geometría se calculó a mano.

**Resuelto (2026-10-23):** Rodrigo lo abrió en su navegador y los sprites se ven bien.
