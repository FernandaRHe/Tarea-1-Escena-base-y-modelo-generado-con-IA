# Verificación de copia portable

Fecha: 6 de octubre de 2026. Godot 4.7.2 stable en Windows, OpenGL Compatibility.

Se empaquetó el proyecto sin `.godot`, `.git`, archivos `.import` ni intermediarios AVI. Se extrajo en `tmp/clean-copy`, se importó con `--headless --editor --quit` y se ejecutó `tests/acceptance.gd -- --capture` con renderizado real. Ambos procesos finalizaron con código 0; 14/14 comprobaciones aprobadas. Las capturas de la copia se generaron de nuevo y los recursos actuales no presentaron errores de carga.

La verificación cubre escenas, scripts y materiales procedurales incluidos. No cubre un modelo IA final, que aún no existe en el proyecto. La copia y sus cachés son temporales y no forman parte del ZIP.
