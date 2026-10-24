PY := .venv/bin/python

.PHONY: todo datos sprites genoma distancias pidgey arbol bootstrap visual video

todo: genoma distancias pidgey arbol bootstrap visual video

datos:
	$(PY) scripts/descargar_datos.py

sprites:
	$(PY) scripts/descargar_sprites.py

genoma:
	$(PY) src/genoma.py

distancias:
	$(PY) src/puntuacion.py

pidgey:
	$(PY) src/prueba_pidgey.py

arbol:
	$(PY) src/arbol.py

bootstrap:
	$(PY) src/bootstrap.py

visual:
	$(PY) src/visualizar.py

video:
	$(PY) src/comparar_video.py
